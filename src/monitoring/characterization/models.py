"""
Data models for Step 10D device characterization.

Enforces strict null-value rules and status/value separation:
- If state is not AVAILABLE, value MUST be None (no fake zeros).
- If verified is True, state MUST be AVAILABLE and report_status MUST be VERIFIED.
"""

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Dict, List, Optional


class RuntimeState(str, Enum):
    AVAILABLE = "AVAILABLE"
    UNAVAILABLE = "UNAVAILABLE"
    PERMISSION_REQUIRED = "PERMISSION_REQUIRED"
    API_UNSUPPORTED = "API_UNSUPPORTED"
    EXTERNAL_REQUIRED = "EXTERNAL_REQUIRED"
    NOT_TESTED = "NOT_TESTED"
    ERROR = "ERROR"


class ReportStatus(str, Enum):
    VERIFIED = "VERIFIED"
    AVAILABLE = "AVAILABLE"
    CONDITIONALLY_AVAILABLE = "CONDITIONALLY AVAILABLE"
    UNAVAILABLE = "UNAVAILABLE"
    REQUIRES_EXTERNAL_INSTRUMENTATION = "REQUIRES EXTERNAL INSTRUMENTATION"
    REQUIRES_PILOT_VALIDATION = "REQUIRES PILOT VALIDATION"
    NOT_YET_VERIFIED = "NOT YET VERIFIED"


def map_runtime_state_to_report_status(
    state: RuntimeState,
    verified: bool = False,
    condition: Optional[str] = None,
    pilot_validation: bool = False,
) -> ReportStatus:
    """Maps a collector runtime state to the schema report_status enum per protocol §3.

    - VERIFIED only for an unconditional AVAILABLE observation whose semantics were checked.
    - AVAILABLE through a condition (host ADB, shell-only path, permission) is CONDITIONALLY AVAILABLE,
      never VERIFIED: a condition-gated value is not an app-verified device fact.
    - AVAILABLE whose interface was demonstrated but whose accuracy/semantics need E0 is
      REQUIRES PILOT VALIDATION. It is never used for a state other than AVAILABLE, so a check that
      never ran cannot become REQUIRES PILOT VALIDATION.
    """
    state = RuntimeState(state)
    if verified:
        if state != RuntimeState.AVAILABLE:
            raise ValueError(f"verified=True requires state AVAILABLE (got {state.value}).")
        if condition:
            raise ValueError("A condition-gated observation is CONDITIONALLY AVAILABLE and cannot be VERIFIED.")
        if pilot_validation:
            raise ValueError("An observation that requires pilot validation cannot be VERIFIED.")
        return ReportStatus.VERIFIED
    if state == RuntimeState.AVAILABLE:
        if condition:
            return ReportStatus.CONDITIONALLY_AVAILABLE
        if pilot_validation:
            return ReportStatus.REQUIRES_PILOT_VALIDATION
        return ReportStatus.AVAILABLE
    if state in (RuntimeState.UNAVAILABLE, RuntimeState.API_UNSUPPORTED):
        return ReportStatus.UNAVAILABLE
    if state == RuntimeState.EXTERNAL_REQUIRED:
        return ReportStatus.REQUIRES_EXTERNAL_INSTRUMENTATION
    if state == RuntimeState.PERMISSION_REQUIRED:
        if condition:
            return ReportStatus.CONDITIONALLY_AVAILABLE
        return ReportStatus.UNAVAILABLE
    return ReportStatus.NOT_YET_VERIFIED


@dataclass
class CapabilityResult:
    metric: str
    state: str
    report_status: str
    value: Optional[Any] = None
    unit: Optional[str] = None
    source: str = "unknown"
    min_api: Optional[int] = None
    condition: Optional[str] = None
    verified: bool = False
    verification_method: str = "unverified"
    evidence_ref: Optional[str] = None
    observed_at: Optional[str] = None
    error_message: Optional[str] = None
    notes: Optional[str] = None

    def __post_init__(self):
        # Enforce no fake zeros rule
        if self.state != RuntimeState.AVAILABLE.value:
            if self.value is not None:
                raise ValueError(
                    f"Metric '{self.metric}' has state '{self.state}' but non-null value '{self.value}'. "
                    "Non-available states MUST have value=null (no fake zeros)."
                )
            if self.verified:
                raise ValueError(
                    f"Metric '{self.metric}' has state '{self.state}' but verified is True. "
                    "Only AVAILABLE state can be verified."
                )
        if self.verified:
            if self.state != RuntimeState.AVAILABLE.value:
                raise ValueError(f"Verified metric '{self.metric}' must have state AVAILABLE.")
            if self.report_status != ReportStatus.VERIFIED.value:
                raise ValueError(f"Verified metric '{self.metric}' must have report_status VERIFIED.")
            if not self.evidence_ref:
                raise ValueError(f"Verified metric '{self.metric}' requires non-null evidence_ref.")
            if not self.observed_at:
                raise ValueError(f"Verified metric '{self.metric}' requires non-null observed_at.")
            if self.condition:
                raise ValueError(
                    f"Verified metric '{self.metric}' has condition '{self.condition}': a condition-gated "
                    "observation is CONDITIONALLY AVAILABLE, not VERIFIED."
                )
        if self.report_status == ReportStatus.REQUIRES_PILOT_VALIDATION.value and self.state != RuntimeState.AVAILABLE.value:
            raise ValueError(
                f"Metric '{self.metric}' is REQUIRES PILOT VALIDATION with state '{self.state}': pilot validation "
                "applies only to an interface already demonstrated (state AVAILABLE)."
            )
        if self.report_status == ReportStatus.CONDITIONALLY_AVAILABLE.value and not self.condition:
            raise ValueError(f"Metric '{self.metric}' is CONDITIONALLY AVAILABLE without a recorded condition.")

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        return d


@dataclass
class KnownSpecification:
    manufacturer: str = "OPPO"
    model: str = "OPPO A5 2020"
    ram_variant: str = "3 GB"
    excluded_variants: List[str] = field(default_factory=lambda: ["4 GB", "6 GB"])
    source: str = "researcher-provided manufacturer specification"
    storage: Optional[str] = "64 GB"
    soc: Optional[str] = "Qualcomm Snapdragon 665"
    gpu: Optional[str] = "Adreno 610"
    android_launch_version: Optional[str] = "Android 9 / ColorOS"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class DeviceIdentity:
    device_unit_id: str
    known_specification: KnownSpecification
    observed: List[CapabilityResult]
    variant_check: CapabilityResult
    identity_match_status: str = "UNKNOWN"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "device_unit_id": self.device_unit_id,
            "known_specification": self.known_specification.to_dict(),
            "observed": [r.to_dict() for r in self.observed],
            "variant_check": self.variant_check.to_dict(),
            "identity_match_status": self.identity_match_status,
        }


@dataclass
class TelemetryCapability:
    dimension: str
    results: List[CapabilityResult]
    resource_state_input: bool
    reliability: str = "NOT YET VERIFIED"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "dimension": self.dimension,
            "results": [r.to_dict() for r in self.results],
            "resource_state_input": self.resource_state_input,
            "reliability": self.reliability,
        }


@dataclass
class CameraCapability:
    camera_id: str
    results: List[CapabilityResult]
    manual_control_honoured: CapabilityResult
    lens_facing: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "camera_id": self.camera_id,
            "lens_facing": self.lens_facing,
            "results": [r.to_dict() for r in self.results],
            "manual_control_honoured": self.manual_control_honoured.to_dict(),
        }


@dataclass
class BackendCapability:
    backend: str
    availability: CapabilityResult
    delegation: CapabilityResult
    probability_output: CapabilityResult
    quantization_support: List[CapabilityResult] = field(default_factory=list)
    runtime_version: Optional[str] = None
    reference_graph_hash: Optional[str] = None
    known_limitations: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "backend": self.backend,
            "runtime_version": self.runtime_version,
            "availability": self.availability.to_dict(),
            "delegation": self.delegation.to_dict(),
            "quantization_support": [r.to_dict() for r in self.quantization_support],
            "probability_output": self.probability_output.to_dict(),
            "reference_graph_hash": self.reference_graph_hash,
            "known_limitations": self.known_limitations,
        }


@dataclass
class ThermalCapability:
    thermal_status_api: CapabilityResult
    temperature_sources: List[CapabilityResult]
    frequency_capping_observable: CapabilityResult
    external_surface_probe: CapabilityResult
    thermal_headroom_api: Optional[CapabilityResult] = None
    selected_thermal_source: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        res = {
            "thermal_status_api": self.thermal_status_api.to_dict(),
            "temperature_sources": [r.to_dict() for r in self.temperature_sources],
            "frequency_capping_observable": self.frequency_capping_observable.to_dict(),
            "external_surface_probe": self.external_surface_probe.to_dict(),
            "selected_thermal_source": self.selected_thermal_source,
        }
        if self.thermal_headroom_api:
            res["thermal_headroom_api"] = self.thermal_headroom_api.to_dict()
        return res


@dataclass
class EnergyCapability:
    E1_battery_side_reference: CapabilityResult
    E2_supply_powered_session: CapabilityResult
    E3_software_counters: CapabilityResult
    selected_level: Optional[str] = None
    absolute_energy_claimed: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "E1_battery_side_reference": self.E1_battery_side_reference.to_dict(),
            "E2_supply_powered_session": self.E2_supply_powered_session.to_dict(),
            "E3_software_counters": self.E3_software_counters.to_dict(),
            "selected_level": self.selected_level,
            "absolute_energy_claimed": False,
        }


@dataclass
class CharacterizationRun:
    run_id: str
    started_at: str
    app_version: str
    git_commit: str
    device_identity: DeviceIdentity
    telemetry: List[TelemetryCapability]
    camera: List[CameraCapability]
    backends: List[BackendCapability]
    profiling: List[CapabilityResult]
    thermal: ThermalCapability
    energy: EnergyCapability
    conditions: Dict[str, Any]
    repeat_index: int = 1
    host_tool_versions: Dict[str, Any] = field(default_factory=dict)
    performance_results: Optional[Any] = None
    app_output_status: Optional[str] = None
    manifest_sha256: Optional[str] = None
    run_status: str = "COMPLETE"

    def to_dict(self) -> Dict[str, Any]:
        d = {
            "run_id": self.run_id,
            "started_at": self.started_at,
            "repeat_index": self.repeat_index,
            "app_version": self.app_version,
            "git_commit": self.git_commit,
            "host_tool_versions": self.host_tool_versions,
            "device_identity": self.device_identity.to_dict(),
            "telemetry": [t.to_dict() for t in self.telemetry],
            "camera": [c.to_dict() for c in self.camera],
            "backends": [b.to_dict() for b in self.backends],
            "profiling": [p.to_dict() for p in self.profiling],
            "thermal": self.thermal.to_dict(),
            "energy": self.energy.to_dict(),
            "conditions": self.conditions,
            "performance_results": None,
            "run_status": self.run_status,
        }
        if self.app_output_status:
            d["app_output_status"] = self.app_output_status
        if self.manifest_sha256:
            d["manifest_sha256"] = self.manifest_sha256
        return d
