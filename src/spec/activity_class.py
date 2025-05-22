from pynwb.spec import NWBGroupSpec
from pynwb import register_class
from ndx_wearables import EnumTimeSeries

@register_class('ActivityClassSeries', 'ndx-wearables')
class ActivityClassSeries(EnumTimeSeries):
    """Activity classification labels stored as a wearable time series"""
    pass

def make_activity_class_stage():
    activity_class_series = NWBGroupSpec(
        doc='Stores categorical labels for physical activity class over time.',
        neurodata_type_def='ActivityClassSeries',
        neurodata_type_inc='EnumTimeSeries'
    )
    return activity_class_series
