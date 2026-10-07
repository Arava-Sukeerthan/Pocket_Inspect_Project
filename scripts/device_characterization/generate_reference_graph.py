"""
Generates (or checks) the Step 10D backend reference-graph artifacts.

The artifacts are produced deterministically by src/monitoring/characterization/reference_graph.py (standard
library only; no download, no TensorFlow/ONNX tooling). They are NOT committed: binary model files are not tracked
in this repository (AGENTS.md; tests/test_dataset_device_model.py). The Android build runs this script
(Gradle task `generateReferenceGraph`) and packages the output as APK assets under `reference_graph/`.
The SHA-256 of every artifact is pinned in configs/device_characterization.yaml
(`inference_backend_check.reference_graph.artifacts`); the app reports the SHA-256 of the bytes it loaded and the
host compares the two.

Usage:
    python scripts/device_characterization/generate_reference_graph.py --out DIR   # write the artifacts into DIR
    python scripts/device_characterization/generate_reference_graph.py --check     # generator == pinned hashes
    python scripts/device_characterization/generate_reference_graph.py             # print name, sha256, size
"""

import argparse
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.monitoring.characterization.reference_graph import build_artifacts  # noqa: E402

CONFIG = ROOT / "configs" / "device_characterization.yaml"


def pinned_hashes(config_path: Path = CONFIG) -> dict:
    import yaml  # only needed for --check
    cfg = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    return dict(cfg["inference_backend_check"]["reference_graph"]["artifacts"])


def check(config_path: Path = CONFIG, artifact_dir: Path = None) -> list:
    """Problems (empty = OK): generator output vs pinned SHA-256, and vs the files in `artifact_dir` if given."""
    pinned = pinned_hashes(config_path)
    built = build_artifacts()
    problems = []
    if set(pinned) != set(built):
        problems.append(f"pinned artifacts {sorted(pinned)} differ from generated {sorted(built)}")
    for name, data in built.items():
        digest = hashlib.sha256(data).hexdigest()
        if pinned.get(name) != digest:
            problems.append(f"{name}: pinned sha256 {pinned.get(name)} != generated {digest}")
        if artifact_dir is not None:
            path = artifact_dir / name
            if not path.exists():
                problems.append(f"{name}: missing from {artifact_dir}")
            elif path.read_bytes() != data:
                problems.append(f"{name}: file in {artifact_dir} differs from the generator output")
    return problems


def write(out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    for name, data in build_artifacts().items():
        (out_dir / name).write_bytes(data)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out", type=Path, help="directory to write the artifacts into")
    parser.add_argument("--check", action="store_true", help="verify the generator output against the pinned SHA-256")
    parser.add_argument("--config", type=Path, default=CONFIG)
    args = parser.parse_args()
    if args.check:
        problems = check(args.config, args.out)
        for p in problems:
            print(f"MISMATCH: {p}")
        print("OK" if not problems else f"{len(problems)} problem(s)")
        return 1 if problems else 0
    if args.out:
        write(args.out)
    for name, data in build_artifacts().items():
        print(f"{name}  {hashlib.sha256(data).hexdigest()}  {len(data)} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
