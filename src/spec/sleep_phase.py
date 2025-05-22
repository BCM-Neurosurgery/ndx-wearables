from pynwb.spec import NWBGroupSpec
from pynwb import register_class
from ndx_wearables import WearableTimeSeries

@register_class('SleepPhaseSeries', 'ndx-wearables')
class SleepPhaseSeries(WearableTimeSeries):
    """Sleep phase classification stored as a wearable time series"""
    pass

def make_sleep_phase_series():
    sleep_phase_series = NWBGroupSpec(
        doc='Stores sleep phase categories (e.g., REM, deep) over time.',
        neurodata_type_def='SleepPhaseSeries',
        neurodata_type_inc='WearableTimeSeries'
    )
    return sleep_phase_series
