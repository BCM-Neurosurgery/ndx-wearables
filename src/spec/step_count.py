from pynwb.spec import NWBGroupSpec
from pynwb import register_class
from ndx_wearables import WearableTimeSeries

class StepCountSeries(WearableTimeSeries):
    """Step count data stored as a wearable time series"""
    pass

def make_step_count_stage():
    step_count_series = NWBGroupSpec(
        doc='Stores number of steps recorded by wearable device.',
        neurodata_type_def='StepCountSeries',
        neurodata_type_inc='WearableTimeSeries'
    )
    return step_count_series
