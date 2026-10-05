# Measurement and Experimental Hardware — GC-03

_Step 10B, 2026-10-05, Claude Code. Research design only. Nothing was measured, and no instrument is claimed to be available or validated._

Device requirements and the telemetry classification are in [`device_requirements.md`](device_requirements.md) §3. Variables are defined in [`variables_and_factors.md`](../research_questions/variables_and_factors.md).

## 1. Telemetry, Resource Condition and Adaptation Decision

These three layers are kept separate (Step 10A, `variables_and_factors.md` §1.1).

| Layer | Content | Role | How obtained |
| :-- | :-- | :-- | :-- |
| **A. Measured telemetry** | Battery percentage; battery current and voltage if available; CPU utilisation; GPU utilisation if available; RAM; CPU/SoC temperature; device temperature; inference latency; FPS; model load time | Measurement variables: covariates, manipulation checks and DVs | In-app logging, ADB/Perfetto, external instruments |
| **B. Experimental resource condition** | R0 nominal, R1 moderate, R2 high, R3 critical | The manipulated factor, induced by the pressure protocol; at runtime the policy classifies telemetry into R | Pressure protocol plus classification thresholds (TO BE CALIBRATED DURING EXPERIMENT DESIGN) |
| **C. Adaptation decision** | C1–C4 | Decision variable: forced in E1, chosen by the policy in E2 | Policy log |

The telemetry availability per signal (AVAILABLE, CONDITIONALLY_AVAILABLE, UNAVAILABLE, REQUIRES_EXTERNAL_INSTRUMENTATION) is in [`device_requirements.md`](device_requirements.md) §3.

## 2. Energy Measurement

Energy (per inference, per inspected item, per verified item; average power; peak power where measurable) is a primary DV for H3 and H5.

### 2.1 Options

| Option | What it gives | Limitation | Defensible for absolute energy? |
| :-- | :-- | :-- | :-- |
| **1. Android battery APIs** (`BATTERY_PROPERTY_CHARGE_COUNTER`, `ENERGY_COUNTER`, capacity) | Charge or energy drawn from the battery over an interval | Fuel-gauge estimates; coarse resolution; `ENERGY_COUNTER` often unsupported; update intervals vendor-defined | **No** on their own. Usable for long intervals only after validation. |
| **2. Power/current telemetry** (`CURRENT_NOW` × voltage; Perfetto power rails where supported) | Instantaneous current and power estimates; per-rail energy on devices with on-device power monitors | Sign, units and refresh vary by vendor; low sampling rate misses short inferences; rails cover subsystems, not necessarily the whole device | **Not without validation.** Per-rail data are useful for attribution if present. |
| **3. External USB power meter** | Power drawn through the USB port | When the phone is powered over USB it also charges the battery, so the reading mixes charging and consumption. It does not measure battery-powered operation, and charging changes battery state and temperature, which confounds R0–R3. | **No** for battery-powered runs. Usable only for a pass-through or bypass configuration that has itself been validated. |
| **4. External power analyzer with battery bypass** (a source-measure unit or dedicated phone power monitor replacing the battery) | High-rate measurement of whole-device power from a regulated supply | Needs battery-terminal access, which is often impractical on sealed modern phones. The battery-state factor can then only be emulated (the device reports the supply). It changes thermal behaviour (no battery heat). | **Yes for absolute energy**, if the bypass is achievable on the chosen device. |

### 2.2 Strategy (PROVISIONAL)

**EXTERNAL-METER VALIDATION REQUIRED.** Android software telemetry is not, on its own, a defensible measure of absolute energy. No energy accuracy is claimed until validation has been done.

1. **Reference.** Use an external instrument (option 4, or a validated pass-through version of option 3) as the energy reference on the chosen device. If none is achievable, absolute energy is not reported; only relative, within-device comparisons from validated software counters are reported, and this is stated as a limitation.
2. **Validation of software counters.**
   - Run identical scripted workloads with the reference and the software counters recorded at the same time.
   - Estimate agreement (bias, limits of agreement) and the shortest interval over which software counters are usable.
   - Acceptance criteria: TO BE PRE-REGISTERED.
3. **Unit of analysis.**
   - Energy is integrated over intervals long enough for the validated resolution, e.g. a batch of items, then divided by the item count.
   - Per-single-inference energy is reported only if the reference has adequate time resolution.
4. **Conflict with the battery factor.**
   - Battery-state conditions (part of R0–R3) need a battery-powered phone.
   - Bypass measurement needs a supply instead of the battery.
   - **Proposed resolution:** run battery-condition episodes on the battery with software counters (validated), and run energy-reference sessions separately to calibrate those counters. This is a stated design limitation.

**Candidate quantities.** Energy per inference; energy per inspected item; energy per verified item; average power; peak power (only with a reference of adequate time resolution). Sampling rates: **not chosen** (TO BE DETERMINED during experiment design).

## 3. Thermal Measurement

**Temperature measurement vs thermal state.**
- **Temperature measurement:** a value in degrees from a sensor.
- **Thermal state / throttling:** the platform's discrete status (`getCurrentThermalStatus()`) and forecast headroom (`getThermalHeadroom()`), plus observed frequency capping.

The two are logged separately. Neither is inferred from the other.

| Quantity | Source | Status |
| :-- | :-- | :-- |
| SoC / CPU temperature | Thermal zones via ADB / Perfetto; `HardwarePropertiesManager` (device owner or VR service only) | CONDITIONALLY_AVAILABLE: zone naming and meaning are vendor-specific and must be mapped per device |
| Battery temperature | `ACTION_BATTERY_CHANGED` `EXTRA_TEMPERATURE` | AVAILABLE |
| Skin / device temperature | `HardwarePropertiesManager` (`DEVICE_TEMPERATURE_SKIN`) where accessible; otherwise an **external surface probe** (thermocouple) at a fixed, documented location | CONDITIONALLY_AVAILABLE / REQUIRES_EXTERNAL_INSTRUMENTATION |
| Ambient temperature | External thermometer near the device | REQUIRES_EXTERNAL_INSTRUMENTATION |
| Thermal throttling state | Thermal status and headroom (API 29/30) | AVAILABLE (API-level dependent) |
| Sustained-performance degradation | Derived: latency and CPU/GPU frequency over time at a fixed configuration (E1) | AVAILABLE (derived from logs) |

**Limitations.**
- No Android API is assumed to expose every required temperature.
- Third-party apps may be denied thermal-zone access.
- Battery temperature lags SoC temperature.
- Thermal state depends on vendor policy.
- Ambient temperature, phone case and mounting change heat dissipation. These are controlled or logged; `variables_and_factors.md` §4 lists them as controls.

## 4. Conceptual Hardware Setup

```
 [Controlled enclosure / room: ambient thermometer]
   ├── Smartphone (fixed mount, case removed or fixed, flight mode)
   │     ├── Rear camera ──> inspection object on indexed jig/turntable (Stage 2)
   │     │                   or replayed dataset images (Stage 1)
   │     ├── In-app logger: telemetry, R-state, configuration, action, outputs
   │     └── Optional: battery bypass to external power analyzer
   ├── Fixed rig lighting (Stage 2)
   ├── Surface temperature probe on the device back (fixed location)
   └── Host computer: ADB / Perfetto session, external-meter logger, clock reference
```

| What | Where measured | Logged by |
| :-- | :-- | :-- |
| Inference latency, model load time, FPS, outputs, confidence, R-state, configuration, action | On the phone (locally) | In-app logger |
| Battery level, voltage, current, battery temperature, thermal status and headroom, RAM, power-save mode | On the phone (locally) | In-app logger |
| Device-wide CPU utilisation and frequency, GPU counters, thermal zones, power rails (if supported) | On the phone, read by the host | ADB / Perfetto on the host |
| Whole-device power and energy | Externally | External meter logger |
| Surface and ambient temperature | Externally | Thermometer logger |
| Camera metadata (exposure, focus, ISO, white balance) | On the phone | In-app logger (Stage 2) |

**Timestamp synchronisation.**
- The phone uses a monotonic clock (`SystemClock.elapsedRealtimeNanos()`). Each external logger uses its own clock.
- Required: a shared synchronisation event at the start and end of every run, visible to all streams. For example, a scripted burst of load visible as a power step and in the app log, or a host-issued ADB marker recorded by both the host and the app.
- Clock offset and drift are estimated from the two events, and the residual misalignment is reported.
- The required alignment precision depends on the energy unit of analysis: TO BE DETERMINED.

## 5. Status

| Item | Status |
| :-- | :-- |
| Energy strategy | PROVISIONAL; EXTERNAL-METER VALIDATION REQUIRED |
| External meter or analyzer | Not available as far as the repository shows (REQUIRES_VERIFICATION) |
| Thermal strategy | PROVISIONAL |
| Sampling rates | Not chosen |
| Hardware setup | Conceptual only |
