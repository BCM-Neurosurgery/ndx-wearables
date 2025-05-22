from pynwb.spec import NWBGroupSpec
from pynwb import register_class
from ndx_wearables import WearableTimeSeries

@register_class('MetSeries', 'ndx-wearables')
class MetSeries(WearableTimeSeries):
    """Metabolic equivalent (MET) values stored as a wearable time series"""
    pass

def make_met_series():
    met_series = NWBGroupSpec(
        doc='Stores metabolic equivalent (MET) values over time.',
        neurodata_type_def='MetSeries',
        neurodata_type_inc='WearableTimeSeries'
    )
    return met_series
