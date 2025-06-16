from pynwb.spec import NWBGroupSpec
from pynwb import register_class
from ndx_wearables import WearableTimeSeries

def make_blood_oxygen_stage():
    blood_oxygen_series = NWBGroupSpec(
        doc='Stores blood oxygen saturation levels over time.',
        neurodata_type_def='BloodOxygenSeries',
        neurodata_type_inc='WearableTimeSeries'
    )
    return blood_oxygen_series
