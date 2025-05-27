from pynwb.spec import NWBGroupSpec
from pynwb import register_class
from ndx_wearables import WearableTimeSeries

def make_heart_rate_stage():
    heart_rate_series = NWBGroupSpec(
        doc='Stores heart rate.',
        neurodata_type_def='HeartRateSeries',
        neurodata_type_inc='WearableTimeSeries'
    )
    return heart_rate_series