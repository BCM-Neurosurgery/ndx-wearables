from pynwb.spec import NWBGroupSpec
from pynwb import register_class
from ndx_wearables import WearableTimeSeries

@register_class('ActivityClassSeries', 'ndx-wearables')
class ActivityClassSeries(WearableTimeSeries):
    """Activity classification labels stored as a wearable time series"""
    pass

def make_activity_class_series():
    activity_class_series = NWBGroupSpec(
        doc='Stores categorical labels for physical activity class over time.',
        neurodata_type_def='ActivityClassSeries',
        neurodata_type_inc='WearableTimeSeries'
    )
    return activity_class_series
