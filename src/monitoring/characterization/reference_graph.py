"""
Step 10D backend capability reference graph (protocol §4 P4, §5.4, §5.5).

A deterministic, tiny graph used only to check that a runtime/backend can load a graph, execute it, produce a
valid probability vector and apply the requested delegate. It has no trained weights and is never a candidate model.

Structure (same function in every artifact):

    input [1, 8, 8, 3]  (TFLite NHWC; ONNX NCHW [1, 3, 8, 8])
    -> CONV 3x3, 3 -> 4 channels, stride 1, SAME padding, bias, no activation
    -> DEPTHWISE CONV 3x3, 4 channels, multiplier 1, stride 1, SAME padding, bias, no activation
    -> AVERAGE POOL 2x2, stride 2                                    -> [1, 4, 4, 4]
    -> FULLY CONNECTED 64 -> 4, bias  (ONNX: Flatten + Gemm)
    -> SOFTMAX (beta 1)                                              -> output [1, 4]

Variants (protocol §5.5):
- fp32: float32 weights and activations.
- fp16: float16 weight storage, DEQUANTIZE (TFLite) / Cast (ONNX) to float32 before use. Every weight is a multiple
  of 1/64 or 1/256 with magnitude below 1, so it is exactly representable in float16: the function is unchanged.
- int8: per-tensor int8 weights, int32 biases, int8 activations (TFLite QUANTIZE/DEQUANTIZE at the float32
  interface; ONNX QuantizeLinear/DequantizeLinear pairs). The softmax output uses scale 1/256, zero point -128.

Weights and the test input are generated from fixed integer formulas (no randomness, no download), so the artifact
bytes, their SHA-256 and the expected output are reproducible. Serialisation uses only the standard library
(hand-written FlatBuffers / Protocol Buffers encoders), so no TensorFlow or ONNX tooling is required.

The expected output is computed here in float64 from the exact weight values. The host compares an app-reported
output against it with the tolerances in configs/device_characterization.yaml (inference_backend_check).
"""

import hashlib
import json
import math
import struct
from typing import Any, Dict, List, Sequence, Tuple

GRAPH_ID = "pocketinspect_step10d_reference_graph_v1"

H = W = 8
C_IN = 3
C1 = 4
K = 3
POOL = 2
CLASSES = 4
HP = WP = H // POOL
FC_IN = HP * WP * C1

INPUT_SHAPE_NHWC = [1, H, W, C_IN]
INPUT_SHAPE_NCHW = [1, C_IN, H, W]
OUTPUT_SHAPE = [1, CLASSES]

OPERATORS = ("CONV_2D", "DEPTHWISE_CONV_2D", "AVERAGE_POOL_2D", "FULLY_CONNECTED", "SOFTMAX")
VARIANTS = ("fp32", "fp16", "int8")
FORMATS = ("tflite", "onnx")

# int8 softmax output quantization (TFLite requirement for int8 SOFTMAX).
SOFTMAX_OUT_SCALE = 1.0 / 256.0
SOFTMAX_OUT_ZERO_POINT = -128


# ---------------------------------------------------------------------------------------------------------------
# Deterministic parameters
# ---------------------------------------------------------------------------------------------------------------

def _det(n: int, a: int, b: int, denom: int, m: int = 61, center: int = 30) -> List[float]:
    """n values ((i*a + b) mod m - center) / denom: exact binary fractions, no randomness."""
    return [((i * a + b) % m - center) / denom for i in range(n)]


def parameters() -> Dict[str, Any]:
    """Canonical (NHWC-ordered) weights and test input. Every value is exactly representable in float16."""
    conv_w = _det(C1 * K * K * C_IN, 37, 11, 64)     # [o][kh][kw][i]
    conv_b = _det(C1, 7, 3, 256)
    dw_w = _det(K * K * C1, 23, 5, 64)                # [kh][kw][c]
    dw_b = _det(C1, 13, 9, 256)
    fc_w = _det(CLASSES * FC_IN, 29, 17, 256)         # [cls][h][w][c]
    fc_b = _det(CLASSES, 11, 21, 64)
    x = _det(H * W * C_IN, 13, 5, 32, m=41, center=20)  # [h][w][c]
    return {"conv_w": conv_w, "conv_b": conv_b, "dw_w": dw_w, "dw_b": dw_b, "fc_w": fc_w, "fc_b": fc_b, "x": x}


# ---------------------------------------------------------------------------------------------------------------
# Float64 reference forward pass (NHWC)
# ---------------------------------------------------------------------------------------------------------------

def _conv(x: List[float], w: List[float], b: List[float]) -> List[float]:
    out = [0.0] * (H * W * C1)
    for oh in range(H):
        for ow in range(W):
            for o in range(C1):
                acc = b[o]
                for kh in range(K):
                    ih = oh + kh - 1
                    if not 0 <= ih < H:
                        continue
                    for kw in range(K):
                        iw = ow + kw - 1
                        if not 0 <= iw < W:
                            continue
                        for i in range(C_IN):
                            acc += x[(ih * W + iw) * C_IN + i] * w[((o * K + kh) * K + kw) * C_IN + i]
                out[(oh * W + ow) * C1 + o] = acc
    return out


def _depthwise(x: List[float], w: List[float], b: List[float]) -> List[float]:
    out = [0.0] * (H * W * C1)
    for oh in range(H):
        for ow in range(W):
            for c in range(C1):
                acc = b[c]
                for kh in range(K):
                    ih = oh + kh - 1
                    if not 0 <= ih < H:
                        continue
                    for kw in range(K):
                        iw = ow + kw - 1
                        if not 0 <= iw < W:
                            continue
                        acc += x[(ih * W + iw) * C1 + c] * w[(kh * K + kw) * C1 + c]
                out[(oh * W + ow) * C1 + c] = acc
    return out


def _avgpool(x: List[float]) -> List[float]:
    out = [0.0] * (HP * WP * C1)
    for oh in range(HP):
        for ow in range(WP):
            for c in range(C1):
                s = sum(x[((oh * POOL + dh) * W + (ow * POOL + dw)) * C1 + c] for dh in range(POOL) for dw in range(POOL))
                out[(oh * WP + ow) * C1 + c] = s / (POOL * POOL)
    return out


def _fc(x: List[float], w: List[float], b: List[float]) -> List[float]:
    return [b[o] + sum(x[k] * w[o * FC_IN + k] for k in range(FC_IN)) for o in range(CLASSES)]


def _softmax(z: List[float]) -> List[float]:
    m = max(z)
    e = [math.exp(v - m) for v in z]
    s = sum(e)
    return [v / s for v in e]


def forward(p: Dict[str, Any] = None) -> Dict[str, List[float]]:
    """Every intermediate activation of the float64 reference (NHWC)."""
    p = p or parameters()
    conv = _conv(p["x"], p["conv_w"], p["conv_b"])
    dw = _depthwise(conv, p["dw_w"], p["dw_b"])
    pool = _avgpool(dw)
    logits = _fc(pool, p["fc_w"], p["fc_b"])
    return {"input": p["x"], "conv": conv, "dw": dw, "pool": pool, "logits": logits, "probs": _softmax(logits)}


def expected_output() -> List[float]:
    """Deterministic expected probability vector (float64)."""
    return forward()["probs"]


# ---------------------------------------------------------------------------------------------------------------
# int8 quantization parameters (per tensor; calibrated on the deterministic test input)
# ---------------------------------------------------------------------------------------------------------------

def _act_qparams(values: Sequence[float]) -> Tuple[float, int]:
    lo, hi = min(min(values), 0.0), max(max(values), 0.0)
    scale = (hi - lo) / 255.0
    zp = int(round(-128 - lo / scale))
    return _f32(scale), max(-128, min(127, zp))


def _w_scale(values: Sequence[float]) -> float:
    return _f32(max(abs(v) for v in values) / 127.0)


def _f32(v: float) -> float:
    return struct.unpack("<f", struct.pack("<f", v))[0]


def _quant(values: Sequence[float], scale: float, zp: int, lo: int = -128, hi: int = 127) -> List[int]:
    return [max(lo, min(hi, int(round(v / scale)) + zp)) for v in values]


def int8_qparams() -> Dict[str, Any]:
    p = parameters()
    f = forward(p)
    q: Dict[str, Any] = {}
    q["input"] = _act_qparams(f["input"])
    q["conv"] = _act_qparams(f["conv"])
    q["dw"] = _act_qparams(f["dw"])
    q["pool"] = q["dw"]  # TFLite int8 AVERAGE_POOL_2D requires equal input/output quantization
    q["logits"] = _act_qparams(f["logits"])
    q["probs"] = (SOFTMAX_OUT_SCALE, SOFTMAX_OUT_ZERO_POINT)
    q["conv_w"] = _w_scale(p["conv_w"])
    q["dw_w"] = _w_scale(p["dw_w"])
    q["fc_w"] = _w_scale(p["fc_w"])
    return q


# ---------------------------------------------------------------------------------------------------------------
# Minimal FlatBuffers writer (forward layout: children follow their parent, every uoffset is positive)
# ---------------------------------------------------------------------------------------------------------------

_SCALAR = {"bool": ("<B", 1), "u8": ("<B", 1), "i8": ("<b", 1), "i16": ("<h", 2), "u16": ("<H", 2),
           "i32": ("<i", 4), "u32": ("<I", 4), "i64": ("<q", 8), "f32": ("<f", 4)}


class _Table:
    def __init__(self, fields: List[Tuple[int, str, Any]]):
        self.fields = fields  # (field_index, kind, value); kind is a scalar kind or "off"


class _Vector:
    def __init__(self, kind: str, values: Sequence[Any], align: int = 4):
        self.kind, self.values, self.align = kind, list(values), align


class _String:
    def __init__(self, s: str):
        self.s = s


class _FlatBufferWriter:
    def __init__(self):
        self.b = bytearray()

    def _pad_to(self, align: int, extra: int = 0) -> None:
        while (len(self.b) + extra) % align:
            self.b.append(0)

    def _patch(self, at: int, target: int) -> None:
        struct.pack_into("<I", self.b, at, target - at)

    def emit(self, obj: Any) -> int:
        if isinstance(obj, _Table):
            return self._table(obj)
        if isinstance(obj, _Vector):
            return self._vector(obj)
        if isinstance(obj, _String):
            self._pad_to(4)
            pos = len(self.b)
            data = obj.s.encode("utf-8")
            self.b += struct.pack("<I", len(data)) + data + b"\x00"
            return pos
        raise TypeError(type(obj))

    def _table(self, t: _Table) -> int:
        fields = sorted(t.fields, key=lambda f: -(_SCALAR[f[1]][1] if f[1] != "off" else 4))
        layout: List[Tuple[int, str, Any, int]] = []
        off = 4
        max_align = 4
        for idx, kind, value in fields:
            size = _SCALAR[kind][1] if kind != "off" else 4
            max_align = max(max_align, size)
            off = (off + size - 1) // size * size
            layout.append((idx, kind, value, off))
            off += size
        table_size = off
        n_slots = (max(f[0] for f in fields) + 1) if fields else 0
        slots = [0] * n_slots
        for idx, _, _, o in layout:
            slots[idx] = o
        self._pad_to(2)
        vt_pos = len(self.b)
        self.b += struct.pack("<HH", 4 + 2 * n_slots, table_size) + b"".join(struct.pack("<H", s) for s in slots)
        self._pad_to(max_align)
        t_pos = len(self.b)
        self.b += b"\x00" * table_size
        struct.pack_into("<i", self.b, t_pos, t_pos - vt_pos)
        children = []
        for idx, kind, value, o in layout:
            if kind == "off":
                children.append((t_pos + o, value))
            else:
                struct.pack_into(_SCALAR[kind][0], self.b, t_pos + o, value)
        for at, child in children:
            self._patch(at, self.emit(child))
        return t_pos

    def _vector(self, v: _Vector) -> int:
        size = _SCALAR[v.kind][1] if v.kind != "off" else 4
        self._pad_to(max(4, size, v.align), extra=4)
        pos = len(self.b)
        self.b += struct.pack("<I", len(v.values))
        if v.kind == "off":
            slots = []
            for child in v.values:
                slots.append((len(self.b), child))
                self.b += b"\x00\x00\x00\x00"
            for at, child in slots:
                self._patch(at, self.emit(child))
        else:
            fmt = _SCALAR[v.kind][0]
            for value in v.values:
                self.b += struct.pack(fmt, value)
        return pos

    def finish(self, root: _Table, ident: bytes) -> bytes:
        self.b += b"\x00\x00\x00\x00" + ident
        self._patch(0, self.emit(root))
        self._pad_to(16)
        return bytes(self.b)


# TFLite schema constants (tensorflow/lite/schema/schema.fbs).
_TT_FLOAT32, _TT_FLOAT16, _TT_INT32, _TT_INT8 = 0, 1, 2, 9
_OP = {"AVERAGE_POOL_2D": 1, "CONV_2D": 3, "DEPTHWISE_CONV_2D": 4, "DEQUANTIZE": 6, "FULLY_CONNECTED": 9,
       "SOFTMAX": 25, "QUANTIZE": 114}
_OPT_CONV, _OPT_DW, _OPT_POOL, _OPT_FC, _OPT_SOFTMAX = 1, 2, 5, 8, 9
_PAD_SAME, _PAD_VALID = 0, 1


def _pack(fmt: str, values: Sequence[Any]) -> bytes:
    return b"".join(struct.pack(fmt, v) for v in values)


def _f16_bytes(values: Sequence[float]) -> bytes:
    out = b""
    for v in values:
        packed = struct.pack("<e", v)
        if struct.unpack("<e", packed)[0] != v:
            raise ValueError(f"{v} is not exactly representable in float16")
        out += packed
    return out


class _TFLiteGraph:
    def __init__(self):
        self.buffers: List[bytes] = [b""]  # buffer 0 is the empty sentinel
        self.tensors: List[_Table] = []
        self.ops: List[Tuple[str, int, List[int], List[int], Any]] = []
        self.opcodes: List[Tuple[str, int]] = []

    def tensor(self, name: str, shape: List[int], ttype: int, data: bytes = None,
               quant: Tuple[List[float], List[int], int] = None) -> int:
        buf = 0
        if data is not None:
            self.buffers.append(data)
            buf = len(self.buffers) - 1
        fields: List[Tuple[int, str, Any]] = [
            (0, "off", _Vector("i32", shape)), (1, "i8", ttype), (2, "u32", buf), (3, "off", _String(name))]
        if quant is not None:
            scales, zps, qdim = quant
            fields.append((4, "off", _Table([(2, "off", _Vector("f32", scales)), (3, "off", _Vector("i64", zps)),
                                             (6, "i32", qdim)])))
        self.tensors.append(_Table(fields))
        return len(self.tensors) - 1

    def op(self, name: str, version: int, inputs: List[int], outputs: List[int], options: Any = None) -> None:
        key = (name, version)
        if key not in self.opcodes:
            self.opcodes.append(key)
        self.ops.append((name, self.opcodes.index(key), inputs, outputs, options))

    def serialize(self, inputs: List[int], outputs: List[int], description: str) -> Tuple[bytes, int]:
        operators = []
        for name, idx, ins, outs, options in self.ops:
            fields = [(0, "u32", idx), (1, "off", _Vector("i32", ins)), (2, "off", _Vector("i32", outs))]
            if options is not None:
                opt_type, opt_fields = options
                fields += [(3, "u8", opt_type), (4, "off", _Table(opt_fields))]
            operators.append(_Table(fields))
        subgraph = _Table([(0, "off", _Vector("off", self.tensors)), (1, "off", _Vector("i32", inputs)),
                           (2, "off", _Vector("i32", outputs)), (3, "off", _Vector("off", operators)),
                           (4, "off", _String("main"))])
        opcodes = [_Table([(0, "i8", _OP[n]), (2, "i32", v), (3, "i32", _OP[n])]) for n, v in self.opcodes]
        buffers = [_Table([(0, "off", _Vector("u8", list(d), align=16))]) if d else _Table([]) for d in self.buffers]
        model = _Table([(0, "u32", 3), (1, "off", _Vector("off", opcodes)), (2, "off", _Vector("off", [subgraph])),
                        (3, "off", _String(description)), (4, "off", _Vector("off", buffers))])
        return _FlatBufferWriter().finish(model, b"TFL3"), len(self.ops)


def _conv_opts():
    return (_OPT_CONV, [(0, "i8", _PAD_SAME), (1, "i32", 1), (2, "i32", 1), (3, "i8", 0), (4, "i32", 1), (5, "i32", 1)])


def _dw_opts():
    return (_OPT_DW, [(0, "i8", _PAD_SAME), (1, "i32", 1), (2, "i32", 1), (3, "i32", 1), (4, "i8", 0),
                      (5, "i32", 1), (6, "i32", 1)])


def _pool_opts():
    return (_OPT_POOL, [(0, "i8", _PAD_VALID), (1, "i32", POOL), (2, "i32", POOL), (3, "i32", POOL),
                        (4, "i32", POOL), (5, "i8", 0)])


def _fc_opts():
    return (_OPT_FC, [(0, "i8", 0)])


def _softmax_opts():
    return (_OPT_SOFTMAX, [(0, "f32", 1.0)])


def build_tflite(variant: str) -> bytes:
    return _build_tflite(variant)[0]


def _build_tflite(variant: str) -> Tuple[bytes, int]:
    """(artifact bytes, operator count)."""
    p = parameters()
    g = _TFLiteGraph()
    act = [1, H, W, C1]
    pooled = [1, HP, WP, C1]
    conv_shape, dw_shape, fc_shape = [C1, K, K, C_IN], [1, K, K, C1], [CLASSES, FC_IN]
    desc = f"{GRAPH_ID} {variant}"
    if variant in ("fp32", "fp16"):
        x = g.tensor("input", INPUT_SHAPE_NHWC, _TT_FLOAT32)

        def weight(name: str, shape: List[int], values: List[float]) -> int:
            if variant == "fp32":
                return g.tensor(name, shape, _TT_FLOAT32, _pack("<f", values))
            half = g.tensor(name + "_fp16", shape, _TT_FLOAT16, _f16_bytes(values))
            full = g.tensor(name, shape, _TT_FLOAT32)
            g.op("DEQUANTIZE", 3, [half], [full])
            return full

        cw, cb = weight("conv_w", conv_shape, p["conv_w"]), weight("conv_b", [C1], p["conv_b"])
        dw, db = weight("dw_w", dw_shape, p["dw_w"]), weight("dw_b", [C1], p["dw_b"])
        fw, fb = weight("fc_w", fc_shape, p["fc_w"]), weight("fc_b", [CLASSES], p["fc_b"])
        t_conv = g.tensor("conv", act, _TT_FLOAT32)
        t_dw = g.tensor("depthwise", act, _TT_FLOAT32)
        t_pool = g.tensor("pool", pooled, _TT_FLOAT32)
        t_logits = g.tensor("logits", OUTPUT_SHAPE, _TT_FLOAT32)
        y = g.tensor("probabilities", OUTPUT_SHAPE, _TT_FLOAT32)
        g.op("CONV_2D", 1, [x, cw, cb], [t_conv], _conv_opts())
        g.op("DEPTHWISE_CONV_2D", 1, [t_conv, dw, db], [t_dw], _dw_opts())
        g.op("AVERAGE_POOL_2D", 1, [t_dw], [t_pool], _pool_opts())
        g.op("FULLY_CONNECTED", 1, [t_pool, fw, fb], [t_logits], _fc_opts())
        g.op("SOFTMAX", 1, [t_logits], [y], _softmax_opts())
        return g.serialize([x], [y], desc)

    if variant != "int8":
        raise ValueError(variant)
    q = int8_qparams()

    def aq(key: str) -> Tuple[List[float], List[int], int]:
        s, z = q[key]
        return ([s], [z], 0)

    def wq(values: List[float], scale: float) -> bytes:
        return _pack("<b", _quant(values, scale, 0, -127, 127))

    def bq(values: List[float], scale: float) -> bytes:
        return _pack("<i", [int(round(v / scale)) for v in values])

    s_in, s_conv, s_dw = q["input"][0], q["conv"][0], q["dw"][0]
    x = g.tensor("input", INPUT_SHAPE_NHWC, _TT_FLOAT32)
    xq = g.tensor("input_int8", INPUT_SHAPE_NHWC, _TT_INT8, quant=aq("input"))
    cw = g.tensor("conv_w", conv_shape, _TT_INT8, wq(p["conv_w"], q["conv_w"]), ([q["conv_w"]], [0], 0))
    cb = g.tensor("conv_b", [C1], _TT_INT32, bq(p["conv_b"], s_in * q["conv_w"]), ([_f32(s_in * q["conv_w"])], [0], 0))
    dw = g.tensor("dw_w", dw_shape, _TT_INT8, wq(p["dw_w"], q["dw_w"]), ([q["dw_w"]], [0], 0))
    db = g.tensor("dw_b", [C1], _TT_INT32, bq(p["dw_b"], s_conv * q["dw_w"]), ([_f32(s_conv * q["dw_w"])], [0], 0))
    fw = g.tensor("fc_w", fc_shape, _TT_INT8, wq(p["fc_w"], q["fc_w"]), ([q["fc_w"]], [0], 0))
    fb = g.tensor("fc_b", [CLASSES], _TT_INT32, bq(p["fc_b"], s_dw * q["fc_w"]), ([_f32(s_dw * q["fc_w"])], [0], 0))
    t_conv = g.tensor("conv", act, _TT_INT8, quant=aq("conv"))
    t_dw = g.tensor("depthwise", act, _TT_INT8, quant=aq("dw"))
    t_pool = g.tensor("pool", pooled, _TT_INT8, quant=aq("pool"))
    t_logits = g.tensor("logits", OUTPUT_SHAPE, _TT_INT8, quant=aq("logits"))
    t_probs = g.tensor("probabilities_int8", OUTPUT_SHAPE, _TT_INT8, quant=aq("probs"))
    y = g.tensor("probabilities", OUTPUT_SHAPE, _TT_FLOAT32)
    g.op("QUANTIZE", 2, [x], [xq])
    g.op("CONV_2D", 3, [xq, cw, cb], [t_conv], _conv_opts())
    g.op("DEPTHWISE_CONV_2D", 3, [t_conv, dw, db], [t_dw], _dw_opts())
    g.op("AVERAGE_POOL_2D", 2, [t_dw], [t_pool], _pool_opts())
    g.op("FULLY_CONNECTED", 4, [t_pool, fw, fb], [t_logits], _fc_opts())
    g.op("SOFTMAX", 2, [t_logits], [t_probs], _softmax_opts())
    g.op("DEQUANTIZE", 2, [t_probs], [y])
    return g.serialize([x], [y], desc)


# ---------------------------------------------------------------------------------------------------------------
# Minimal Protocol Buffers writer for ONNX (onnx.proto field numbers)
# ---------------------------------------------------------------------------------------------------------------

def _varint(n: int) -> bytes:
    if n < 0:
        n += 1 << 64
    out = bytearray()
    while True:
        byte = n & 0x7F
        n >>= 7
        if n:
            out.append(byte | 0x80)
        else:
            out.append(byte)
            return bytes(out)


def _key(field: int, wire: int) -> bytes:
    return _varint((field << 3) | wire)


def _pb_int(field: int, v: int) -> bytes:
    return _key(field, 0) + _varint(v)


def _pb_bytes(field: int, data: bytes) -> bytes:
    return _key(field, 2) + _varint(len(data)) + data


def _pb_str(field: int, s: str) -> bytes:
    return _pb_bytes(field, s.encode("utf-8"))


def _pb_float(field: int, v: float) -> bytes:
    return _key(field, 5) + struct.pack("<f", v)


_ONNX_FLOAT, _ONNX_INT8, _ONNX_INT32, _ONNX_FLOAT16 = 1, 3, 6, 10
_ATTR_FLOAT, _ATTR_INT, _ATTR_INTS = 1, 2, 7


def _attr_int(name: str, v: int) -> bytes:
    return _pb_str(1, name) + _pb_int(3, v) + _pb_int(20, _ATTR_INT)


def _attr_ints(name: str, vs: Sequence[int]) -> bytes:
    return _pb_str(1, name) + b"".join(_pb_int(8, v) for v in vs) + _pb_int(20, _ATTR_INTS)


def _attr_float(name: str, v: float) -> bytes:
    return _pb_str(1, name) + _pb_float(2, v) + _pb_int(20, _ATTR_FLOAT)


def _node(op: str, inputs: List[str], outputs: List[str], name: str, attrs: List[bytes] = ()) -> bytes:
    body = b"".join(_pb_str(1, i) for i in inputs) + b"".join(_pb_str(2, o) for o in outputs)
    body += _pb_str(3, name) + _pb_str(4, op) + b"".join(_pb_bytes(5, a) for a in attrs)
    return body


def _tensor(name: str, dims: List[int], dtype: int, raw: bytes) -> bytes:
    return b"".join(_pb_int(1, d) for d in dims) + _pb_int(2, dtype) + _pb_str(8, name) + _pb_bytes(9, raw)


def _value_info(name: str, dtype: int, dims: List[int]) -> bytes:
    shape = b"".join(_pb_bytes(1, _pb_int(1, d)) for d in dims)
    tensor_type = _pb_int(1, dtype) + _pb_bytes(2, shape)
    return _pb_str(1, name) + _pb_bytes(2, _pb_bytes(1, tensor_type))


def _nhwc_conv_to_oihw(w: List[float]) -> List[float]:
    return [w[((o * K + kh) * K + kw) * C_IN + i] for o in range(C1) for i in range(C_IN) for kh in range(K) for kw in range(K)]


def _dw_to_c1hw(w: List[float]) -> List[float]:
    return [w[(kh * K + kw) * C1 + c] for c in range(C1) for kh in range(K) for kw in range(K)]


def _fc_hwc_to_chw(w: List[float]) -> List[float]:
    return [w[o * FC_IN + (h * WP + ww) * C1 + c] for o in range(CLASSES) for c in range(C1) for h in range(HP) for ww in range(WP)]


def nhwc_to_nchw(x: List[float]) -> List[float]:
    return [x[(h * W + w) * C_IN + c] for c in range(C_IN) for h in range(H) for w in range(W)]


def build_onnx(variant: str) -> bytes:
    return _build_onnx(variant)[0]


def _build_onnx(variant: str) -> Tuple[bytes, int]:
    """(artifact bytes, node count)."""
    p = parameters()
    conv_w, dw_w, fc_w = _nhwc_conv_to_oihw(p["conv_w"]), _dw_to_c1hw(p["dw_w"]), _fc_hwc_to_chw(p["fc_w"])
    shapes = {"conv_w": [C1, C_IN, K, K], "conv_b": [C1], "dw_w": [C1, 1, K, K], "dw_b": [C1],
              "fc_w": [CLASSES, FC_IN], "fc_b": [CLASSES]}
    values = {"conv_w": conv_w, "conv_b": p["conv_b"], "dw_w": dw_w, "dw_b": p["dw_b"], "fc_w": fc_w, "fc_b": p["fc_b"]}
    nodes: List[bytes] = []
    inits: List[bytes] = []
    conv_attrs = [_attr_ints("kernel_shape", [K, K]), _attr_ints("pads", [1, 1, 1, 1]), _attr_ints("strides", [1, 1])]
    names = {k: k for k in values}

    if variant == "fp32":
        for k, v in values.items():
            inits.append(_tensor(k, shapes[k], _ONNX_FLOAT, _pack("<f", v)))
    elif variant == "fp16":
        for k, v in values.items():
            inits.append(_tensor(k + "_fp16", shapes[k], _ONNX_FLOAT16, _f16_bytes(v)))
            nodes.append(_node("Cast", [k + "_fp16"], [k], f"cast_{k}", [_attr_int("to", _ONNX_FLOAT)]))
    elif variant != "int8":
        raise ValueError(variant)

    def qdq(src: str, key: str, q: Dict[str, Any]) -> str:
        s, z = q[key]
        inits.append(_tensor(f"{key}_scale", [], _ONNX_FLOAT, _pack("<f", [s])))
        inits.append(_tensor(f"{key}_zp", [], _ONNX_INT8, _pack("<b", [z])))
        nodes.append(_node("QuantizeLinear", [src, f"{key}_scale", f"{key}_zp"], [f"{src}_q"], f"quantize_{src}"))
        nodes.append(_node("DequantizeLinear", [f"{src}_q", f"{key}_scale", f"{key}_zp"], [f"{src}_dq"],
                           f"dequantize_{src}"))
        return f"{src}_dq"

    x_name = "input"
    if variant == "int8":
        q = int8_qparams()
        s_in, s_conv, s_dw = q["input"][0], q["conv"][0], q["dw"][0]
        for k, in_scale in (("conv", s_in), ("dw", s_conv), ("fc", s_dw)):
            w_scale = q[f"{k}_w"]
            inits.append(_tensor(f"{k}_w_q", shapes[f"{k}_w"], _ONNX_INT8, _pack("<b", _quant(values[f"{k}_w"], w_scale, 0, -127, 127))))
            inits.append(_tensor(f"{k}_w_scale", [], _ONNX_FLOAT, _pack("<f", [w_scale])))
            inits.append(_tensor(f"{k}_w_zp", [], _ONNX_INT8, _pack("<b", [0])))
            nodes.append(_node("DequantizeLinear", [f"{k}_w_q", f"{k}_w_scale", f"{k}_w_zp"], [f"{k}_w"], f"dequantize_{k}_w"))
            b_scale = _f32(in_scale * w_scale)
            inits.append(_tensor(f"{k}_b_q", shapes[f"{k}_b"], _ONNX_INT32,
                                 _pack("<i", [int(round(v / b_scale)) for v in values[f"{k}_b"]])))
            inits.append(_tensor(f"{k}_b_scale", [], _ONNX_FLOAT, _pack("<f", [b_scale])))
            inits.append(_tensor(f"{k}_b_zp", [], _ONNX_INT32, _pack("<i", [0])))
            nodes.append(_node("DequantizeLinear", [f"{k}_b_q", f"{k}_b_scale", f"{k}_b_zp"], [f"{k}_b"], f"dequantize_{k}_b"))
        x_name = qdq("input", "input", q)

    nodes.append(_node("Conv", [x_name, names["conv_w"], names["conv_b"]], ["conv"], "conv", conv_attrs))
    t = qdq("conv", "conv", q) if variant == "int8" else "conv"
    nodes.append(_node("Conv", [t, names["dw_w"], names["dw_b"]], ["depthwise"], "depthwise",
                       conv_attrs + [_attr_int("group", C1)]))
    t = qdq("depthwise", "dw", q) if variant == "int8" else "depthwise"
    nodes.append(_node("AveragePool", [t], ["pool"], "pool",
                       [_attr_ints("kernel_shape", [POOL, POOL]), _attr_ints("strides", [POOL, POOL])]))
    t = qdq("pool", "pool", q) if variant == "int8" else "pool"
    nodes.append(_node("Flatten", [t], ["flat"], "flatten", [_attr_int("axis", 1)]))
    nodes.append(_node("Gemm", ["flat", names["fc_w"], names["fc_b"]], ["logits"], "fully_connected",
                       [_attr_int("transB", 1), _attr_float("alpha", 1.0), _attr_float("beta", 1.0)]))
    t = qdq("logits", "logits", q) if variant == "int8" else "logits"
    if variant == "int8":
        nodes.append(_node("Softmax", [t], ["probs_float"], "softmax", [_attr_int("axis", -1)]))
        t = qdq("probs_float", "probs", q)
        nodes.append(_node("Identity", [t], ["probabilities"], "output"))
    else:
        nodes.append(_node("Softmax", [t], ["probabilities"], "softmax", [_attr_int("axis", -1)]))

    graph = b"".join(_pb_bytes(1, n) for n in nodes) + _pb_str(2, f"{GRAPH_ID}_{variant}")
    graph += b"".join(_pb_bytes(5, i) for i in inits)
    graph += _pb_bytes(11, _value_info("input", _ONNX_FLOAT, INPUT_SHAPE_NCHW))
    graph += _pb_bytes(12, _value_info("probabilities", _ONNX_FLOAT, OUTPUT_SHAPE))
    model = _pb_int(1, 7)  # ir_version 7
    model += _pb_str(2, "pocketinspect-reference-graph") + _pb_str(3, "1")
    model += _pb_bytes(7, graph)
    model += _pb_bytes(8, _pb_str(1, "") + _pb_int(2, 13))  # default domain, opset 13
    return model, len(nodes)


# ---------------------------------------------------------------------------------------------------------------
# Artifacts and manifest
# ---------------------------------------------------------------------------------------------------------------

def artifact_name(fmt: str, variant: str) -> str:
    return f"reference_graph_{variant}.{fmt}"


def build_artifacts() -> Dict[str, bytes]:
    """All artifact bytes, keyed by file name (including the manifest)."""
    out: Dict[str, bytes] = {}
    for variant in VARIANTS:
        out[artifact_name("tflite", variant)] = build_tflite(variant)
        out[artifact_name("onnx", variant)] = build_onnx(variant)
    out[MANIFEST_NAME] = manifest_bytes({k: hashlib.sha256(v).hexdigest() for k, v in out.items()})
    return out


MANIFEST_NAME = "reference_graph_manifest.json"


def manifest(hashes: Dict[str, str]) -> Dict[str, Any]:
    """App-readable description: the deterministic input per layout, shapes and the expected output."""
    p = parameters()
    q = int8_qparams()
    return {
        "graph_id": GRAPH_ID,
        "operators": list(OPERATORS),
        "variants": list(VARIANTS),
        "input_name": "input",
        "output_name": "probabilities",
        "input_shape": {"tflite": INPUT_SHAPE_NHWC, "onnx": INPUT_SHAPE_NCHW},
        "output_shape": OUTPUT_SHAPE,
        "input": {"tflite": p["x"], "onnx": nhwc_to_nchw(p["x"])},
        "expected_output": expected_output(),
        "int8_output_quantization": {"scale": q["probs"][0], "zero_point": q["probs"][1]},
        "graph_node_count": graph_node_counts(),
        "artifacts": {name: {"sha256": digest} for name, digest in sorted(hashes.items())},
    }


def graph_node_counts() -> Dict[str, Dict[str, int]]:
    """Nodes in each artifact as serialised (TFLite operators / ONNX nodes), before any runtime optimisation."""
    return {"tflite": {v: _build_tflite(v)[1] for v in VARIANTS}, "onnx": {v: _build_onnx(v)[1] for v in VARIANTS}}


def manifest_bytes(hashes: Dict[str, str]) -> bytes:
    return (json.dumps(manifest(hashes), indent=2, sort_keys=True) + "\n").encode("utf-8")


def artifact_hashes() -> Dict[str, str]:
    return {name: hashlib.sha256(data).hexdigest() for name, data in build_artifacts().items()}


# ---------------------------------------------------------------------------------------------------------------
# Output-validity rule (tolerances from configs/device_characterization.yaml inference_backend_check.output_validation)
# ---------------------------------------------------------------------------------------------------------------

def validate_output(output: Any, variant: str, rules: Dict[str, Any],
                    expected: Sequence[float] = None) -> Tuple[bool, List[str], Dict[str, Any]]:
    """Applies the single output-validity rule to an app-reported output {"shape", "values"}.

    Checks: output present; shape == OUTPUT_SHAPE; every value a finite number in [0, 1];
    abs(sum - 1) <= sum tolerance; max abs error against the float64 reference <= max abs error.
    float variants (fp32, fp16) use rules["float"]; int8 uses rules["int8"], expressed in output quantization steps
    (LSB = rules["int8"]["output_scale"]). Returns (valid, problems, measured).
    """
    expected = list(expected) if expected is not None else expected_output()
    if variant == "int8":
        r = rules["int8"]
        scale = float(r["output_scale"])
        max_err, sum_tol = r["max_abs_error_lsb"] * scale, r["probability_sum_tolerance_lsb"] * scale
        basis = f"int8 rule: {r['max_abs_error_lsb']} LSB / sum {r['probability_sum_tolerance_lsb']} LSB (LSB {scale})"
    else:
        r = rules["float"]
        max_err, sum_tol = float(r["max_abs_error"]), float(r["probability_sum_tolerance"])
        basis = f"float rule: max abs error {max_err} / sum tolerance {sum_tol}"
    measured: Dict[str, Any] = {"rule": basis, "max_abs_error_tolerance": max_err, "probability_sum_tolerance": sum_tol}
    if not isinstance(output, dict) or output.get("values") is None:
        return False, ["output missing"], measured
    problems: List[str] = []
    shape, values = output.get("shape"), output.get("values")
    if list(shape or []) != OUTPUT_SHAPE:
        problems.append(f"shape {shape} != {OUTPUT_SHAPE}")
    if not isinstance(values, list) or len(values) != len(expected):
        return False, problems + [f"expected {len(expected)} values, got {values!r}"], measured
    if not all(isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v) for v in values):
        return False, problems + ["non-finite or non-numeric value"], measured
    if any(v < 0.0 or v > 1.0 for v in values):
        problems.append("value outside [0, 1]")
    total = float(sum(values))
    err = max(abs(v - e) for v, e in zip(values, expected))
    measured.update(probability_sum=total, max_abs_error=err)
    if abs(total - 1.0) > sum_tol:
        problems.append(f"probability sum {total} deviates from 1 by more than {sum_tol}")
    if err > max_err:
        problems.append(f"max abs error {err} vs reference exceeds {max_err}")
    return not problems, problems, measured
