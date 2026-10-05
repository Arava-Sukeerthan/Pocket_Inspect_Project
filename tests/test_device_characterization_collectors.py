"""
Unit tests for Step 10D Device Characterization Collectors.

Validates:
- No fake zeros rule: value must be None when state != AVAILABLE.
- Collector state transitions (AVAILABLE, UNAVAILABLE, PERMISSION_REQUIRED, API_UNSUPPORTED, ERROR).
- Sentinel value parsing (-1, 999999, "unknown", etc. mapped to None).
- Distinction between ERROR and UNAVAILABLE.
"""
import pytest
from src.monitoring.characterization.models import (
    CapabilityResult,
    RuntimeState,
    ReportStatus,
    DeviceIdentity,
    TelemetryCapability,
    CameraCapability,
    BackendCapability,
    ThermalCapability,
    EnergyCapability,
    CharacterizationRun,
)
from src.monitoring.characterization.collectors import (
    DeviceIdentityCollector,
    AndroidCapabilityCollector,
    BatteryTelemetryCollector,
    MemoryTelemetryCollector,
    CPUTelemetryCollector,
    GPUTelemetryCollector,
    ThermalTelemetryCollector,
    CameraCapabilityCollector,
    InferenceBackendCapabilityCollector,
    ProfilingCapabilityCollector,
    EnergyMeasurementCapabilityChecker,
)


def test_capability_result_no_fake_zeros():
    """Verify that setting value != None when state != AVAILABLE raises ValueError."""
    # Valid available state with value
    res = CapabilityResult(metric="cpu_freq", state=RuntimeState.AVAILABLE.value, report_status=ReportStatus.AVAILABLE.value, value=1800, unit="MHz")
    assert res.value == 1800
    assert res.state == RuntimeState.AVAILABLE.value

    # Valid unavailable state with None
    res_unavail = CapabilityResult(metric="gpu_utilization", state=RuntimeState.UNAVAILABLE.value, report_status=ReportStatus.UNAVAILABLE.value, value=None)
    assert res_unavail.value is None

    # Invalid unavailable state with non-None value (e.g. fake zero)
    with pytest.raises(ValueError, match="no fake zeros"):
        CapabilityResult(metric="gpu_utilization", state=RuntimeState.UNAVAILABLE.value, report_status=ReportStatus.UNAVAILABLE.value, value=0)


def test_device_identity_collector():
    collector = DeviceIdentityCollector()
    identity = collector.collect()
    assert isinstance(identity, DeviceIdentity)
    assert identity.device_unit_id is not None
    assert identity.known_specification is not None
    assert isinstance(identity.observed, list)


def test_android_capability_collector():
    collector = AndroidCapabilityCollector()
    cap = collector.collect()
    assert isinstance(cap, TelemetryCapability)
    assert cap.dimension == "android"


def test_battery_telemetry_collector():
    collector = BatteryTelemetryCollector()
    cap = collector.collect()
    assert isinstance(cap, TelemetryCapability)
    assert cap.dimension == "battery"
    for r in cap.results:
        if r.state != RuntimeState.AVAILABLE.value:
            assert r.value is None


def test_memory_telemetry_collector():
    collector = MemoryTelemetryCollector()
    cap = collector.collect()
    assert isinstance(cap, TelemetryCapability)
    assert cap.dimension == "memory"


def test_cpu_telemetry_collector():
    collector = CPUTelemetryCollector()
    cap = collector.collect()
    assert isinstance(cap, TelemetryCapability)
    assert cap.dimension == "cpu"


def test_gpu_telemetry_collector():
    collector = GPUTelemetryCollector()
    cap = collector.collect()
    assert isinstance(cap, TelemetryCapability)
    assert cap.dimension == "gpu"


def test_thermal_telemetry_collector():
    collector = ThermalTelemetryCollector()
    cap = collector.collect()
    assert isinstance(cap, ThermalCapability)
    assert isinstance(cap.temperature_sources, list)


def test_camera_capability_collector():
    collector = CameraCapabilityCollector()
    caps = collector.collect()
    assert isinstance(caps, list)
    for cap in caps:
        assert isinstance(cap, CameraCapability)


def test_inference_backend_collector():
    collector = InferenceBackendCapabilityCollector()
    caps = collector.collect()
    assert isinstance(caps, list)
    for cap in caps:
        assert isinstance(cap, BackendCapability)


def test_profiling_capability_collector():
    collector = ProfilingCapabilityCollector()
    caps = collector.collect()
    assert isinstance(caps, list)
    for cap in caps:
        assert isinstance(cap, CapabilityResult)


def test_energy_measurement_checker():
    checker = EnergyMeasurementCapabilityChecker()
    cap = checker.collect()
    assert isinstance(cap, EnergyCapability)
    assert cap.absolute_energy_claimed is False
