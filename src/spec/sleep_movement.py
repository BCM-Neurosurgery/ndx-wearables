from pynwb.spec import NWBGroupSpec
from pynwb import register_class
from ndx_wearables import WearableTimeSeries

@register_class('SleepMovementSeries', 'ndx-wearables')
class SleepMovementSeries(WearableTimeSeries):
    """Movement intensity or frequency during sleep stored as a wearable time series"""
    pass

def make_sleep_movement_stage():
    sleep_movement_series = NWBGroupSpec(
        doc='Captures movement intensity or frequency during sleep.',
        neurodata_type_def='SleepMovementSeries',
        neurodata_type_inc='WearableTimeSeries'
    )
    return sleep_movement_series
