from pynwb.spec import NWBGroupSpec
from pynwb import register_class
from ndx_wearables import WearableTimeSeries

def make_step_count_stage():
    step_count_series = NWBGroupSpec(
        doc='Stores number of steps recorded by wearable device.',
        neurodata_type_def='StepCountSeries',
        neurodata_type_inc='WearableTimeSeries'
    )
    return step_count_series
