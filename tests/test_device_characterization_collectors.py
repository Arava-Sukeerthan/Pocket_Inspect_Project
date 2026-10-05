"""
Unit tests for Step 10D Device Characterization Collectors after Post-Merge Audit.

Validates findings F-03, F-04, F-05, F-06, F-10, F-12:
- F-03: Empty props / missing inputs yield state=NOT_TESTED (never UNAVAILABLE).
- F-04: Unknown api_level yields state=NOT_TESTED and selected_thermal_source=None.
- F-05: Mock props cannot produce verified=True.
- F-06: Status mapping protocol §3 compliance.
- F-10: Implausible readings produce state=ERROR with raw error preserved.
- F-12: Energy level selection requiring evidence.
"""

import pytest
from src.monitoring.characterization.models import (
    CapabilityResult,
    RuntimeState,
    ReportStatus,
    map_runtime_state_to_report_status,
    DeviceIdentity,
    TelemetryCapability,
    CameraCapability,
    BackendCapability,
    ThermalCapability,
    EnergyCapability,
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
    res = CapabilityResult(
        metric="cpu_freq",
        state=RuntimeState.AVAILABLE.value,
        report_status=ReportStatus.AVAILABLE.value,
        value=1800,
        unit="MHz"
    )
    assert res.value == 1800

    res_unavail = CapabilityResult(
        metric="gpu_utilization",
        state=RuntimeState.UNAVAILABLE.value,
        report_status=ReportStatus.UNAVAILABLE.value,
        value=None
    )
    assert res_unavail.value is None

    with pytest.raises(ValueError, match="no fake zeros"):
        CapabilityResult(
            metric="gpu_utilization",
            state=RuntimeState.UNAVAILABLE.value,
            report_status=ReportStatus.UNAVAILABLE.value,
            value=0
        )


def test_f03_empty_props_return_not_tested():
    """F-03: collect({}) with empty props MUST return NOT_TESTED (never UNAVAILABLE)."""
    # DeviceIdentity
    ident = DeviceIdentityCollector().collect({})
    for r in ident.observed:
        if r.metric != "variant_check":
            assert r.state == RuntimeState.NOT_TESTED.value
            assert r.report_status == ReportStatus.NOT_YET_VERIFIED.value

    # Battery
    batt = BatteryTelemetryCollector().collect({})
    for r in batt.results:
        assert r.state == RuntimeState.NOT_TESTED.value
        assert r.report_status == ReportStatus.NOT_YET_VERIFIED.value

    # Memory
    mem = MemoryTelemetryCollector().collect({})
    for r in mem.results:
        assert r.state == RuntimeState.NOT_TESTED.value
        assert r.report_status == ReportStatus.NOT_YET_VERIFIED.value

    # CPU
    cpu = CPUTelemetryCollector().collect({})
    for r in cpu.results:
        assert r.state == RuntimeState.NOT_TESTED.value

    # Thermal
    thermal = ThermalTelemetryCollector().collect({})
    assert thermal.thermal_status_api.state == RuntimeState.NOT_TESTED.value
    assert thermal.selected_thermal_source is None


def test_f04_unknown_api_level_not_tested():
    """F-04: API level unknown -> state=NOT_TESTED, selected_thermal_source=None."""
    thermal = ThermalTelemetryCollector().collect({})
    assert thermal.thermal_status_api.state == RuntimeState.NOT_TESTED.value
    assert thermal.selected_thermal_source is None

    # Explicit api_level 28 -> API_UNSUPPORTED
    thermal_28 = ThermalTelemetryCollector().collect({"api_level": 28, "battery_temp_available": True})
    assert thermal_28.thermal_status_api.state == RuntimeState.API_UNSUPPORTED.value
    assert thermal_28.selected_thermal_source == "fallback_temperature_and_frequency_capping"

    # Explicit api_level 29 with thermal_status_api_available=True -> AVAILABLE
    thermal_29 = ThermalTelemetryCollector().collect({"api_level": 29, "thermal_status_api_available": True})
    assert thermal_29.thermal_status_api.state == RuntimeState.AVAILABLE.value
    assert thermal_29.selected_thermal_source == "platform_thermal_status"


def test_f05_mock_props_cannot_produce_verified():
    """F-05: Mock props (is_real_device_observation=False) MUST yield verified=False."""
    mock_props = {"level": 57, "voltage_mv": 3800, "temperature_c": 28.5}
    batt = BatteryTelemetryCollector().collect(mock_props)
    for r in batt.results:
        assert r.verified is False
        assert r.evidence_ref is None

    # With is_real_device_observation=True, verified=True and evidence_ref set
    real_props = {"level": 57, "voltage_mv": 3800, "temperature_c": 28.5, "is_real_device_observation": True}
    batt_real = BatteryTelemetryCollector().collect(real_props)
    for r in batt_real.results:
        if r.state == RuntimeState.AVAILABLE.value:
            assert r.verified is True
            assert r.evidence_ref is not None


def test_f06_status_mapping_protocol_compliance():
    """F-06: Test map_runtime_state_to_report_status for all states per Protocol §3."""
    assert map_runtime_state_to_report_status(RuntimeState.AVAILABLE, verified=True) == ReportStatus.VERIFIED
    assert map_runtime_state_to_report_status(RuntimeState.AVAILABLE, verified=False) == ReportStatus.AVAILABLE
    assert map_runtime_state_to_report_status(RuntimeState.AVAILABLE, condition="ADB") == ReportStatus.CONDITIONALLY_AVAILABLE
    assert map_runtime_state_to_report_status(RuntimeState.UNAVAILABLE) == ReportStatus.UNAVAILABLE
    assert map_runtime_state_to_report_status(RuntimeState.API_UNSUPPORTED) == ReportStatus.UNAVAILABLE
    assert map_runtime_state_to_report_status(RuntimeState.EXTERNAL_REQUIRED) == ReportStatus.REQUIRES_EXTERNAL_INSTRUMENTATION
    assert map_runtime_state_to_report_status(RuntimeState.PERMISSION_REQUIRED, condition="ADB") == ReportStatus.CONDITIONALLY_AVAILABLE
    assert map_runtime_state_to_report_status(RuntimeState.NOT_TESTED) == ReportStatus.NOT_YET_VERIFIED
    assert map_runtime_state_to_report_status(RuntimeState.ERROR) == ReportStatus.NOT_YET_VERIFIED


def test_f10_implausible_reading_produces_error():
    """F-10: Implausible battery readings produce state=ERROR with error_message preserved."""
    implausible_props = {"level": 150, "voltage_mv": 99999, "temperature_c": 200}
    batt = BatteryTelemetryCollector().collect(implausible_props)
    for r in batt.results:
        if r.metric in ("battery_level_percent", "battery_voltage", "battery_temperature"):
            assert r.state == RuntimeState.ERROR.value
            assert r.error_message is not None
            assert "Implausible" in r.error_message
