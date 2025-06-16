from pynwb.spec import NWBGroupSpec
from pynwb import register_class
from ndx_wearables import EnumTimeSeries

def make_sleep_phase_stage():
    sleep_phase_series = NWBGroupSpec(
        doc='Stores sleep phase categories (e.g., REM, deep) over time.',
        neurodata_type_def='SleepPhaseSeries',
        neurodata_type_inc='EnumTimeSeries'
    )
    return sleep_phase_series
