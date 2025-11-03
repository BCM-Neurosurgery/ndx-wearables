# src/pynwb/ndx_wearables/__init__.py
import os
import pathlib
from pynwb import load_namespaces, get_class, available_namespaces

try:
    from importlib.resources import files
except ImportError:
    from importlib_resources import files

print(f'Initial namespaces: {available_namespaces()}')

# Load the spec for NDX-Events first
import ndx_events
_events_spec = getattr(ndx_events, "__spec_path", None)
if _events_spec is not None:
    load_namespaces(str(_events_spec))
print(f'After events: {available_namespaces()}')

# Load this repo's ndx-wearables namespace (repo_root/spec/…)
_pkg_files = files(__name__)
_spec_path = _pkg_files / "spec" / "ndx-wearables.namespace.yaml"
if not os.path.exists(os.fspath(_spec_path)):
    _spec_path = pathlib.Path(__file__).resolve().parents[3] / "spec" / "ndx-wearables.namespace.yaml"

print("Loading namespace from:", _spec_path)
load_namespaces(str(_spec_path))

# Export classes 
WearableTimeSeries = get_class("WearableTimeSeries", "ndx-wearables")
WearableDevice = get_class("WearableDevice", "ndx-wearables")
WearableEnumSeries  = get_class("WearableEnumSeries", "ndx-wearables")
PhysiologicalMeasure = get_class("PhysiologicalMeasure", "ndx-wearables")
BloodOxygenSeries  = WearableTimeSeries
HRVSeries = WearableTimeSeries
MetSeries = WearableTimeSeries
SleepMovementSeries = WearableTimeSeries
VO2MaxSeries = WearableTimeSeries
StepCountSeries = WearableTimeSeries

# Confirm if this is the correct logic
SleepPhaseSeries = WearableTimeSeries
ActivityClassSeries = WearableTimeSeries

# convenience wrapper lives in code (not YAML), so import directly
from .wearables_classes import CategoricalSeries
# meanings-table builders
from .categorical_enums import build_sleep_phase_meanings, build_activity_class_meanings

__all__ = ["WearableTimeSeries", "WearableDevice", "WearableEnumSeries","CategoricalSeries","BloodOxygenSeries", "HRVSeries", "MetSeries", "SleepMovementSeries", "VO2MaxSeries", "StepCountSeries","SleepPhaseSeries", "ActivityClassSeries"]
print(f'Final namespaces: {available_namespaces()}')
del load_namespaces, get_class
