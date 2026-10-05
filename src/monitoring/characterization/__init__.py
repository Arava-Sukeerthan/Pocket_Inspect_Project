"""
Step 10D: Device characterization package.

Provides data models, state-to-report status mappings, schema validators,
individual capability collectors, and CharacterizationReportGenerator for
evaluating the physical experimental platform (OPPO A5 2020, 3 GB RAM).
"""

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
from src.monitoring.characterization.report_generator import (
    CharacterizationReportGenerator,
    validate_characterization_record,
)

__all__ = [
    "CapabilityResult",
    "RuntimeState",
    "ReportStatus",
    "DeviceIdentity",
    "TelemetryCapability",
    "CameraCapability",
    "BackendCapability",
    "ThermalCapability",
    "EnergyCapability",
    "CharacterizationRun",
    "DeviceIdentityCollector",
    "AndroidCapabilityCollector",
    "BatteryTelemetryCollector",
    "MemoryTelemetryCollector",
    "CPUTelemetryCollector",
    "GPUTelemetryCollector",
    "ThermalTelemetryCollector",
    "CameraCapabilityCollector",
    "InferenceBackendCapabilityCollector",
    "ProfilingCapabilityCollector",
    "EnergyMeasurementCapabilityChecker",
    "CharacterizationReportGenerator",
    "validate_characterization_record",
]
