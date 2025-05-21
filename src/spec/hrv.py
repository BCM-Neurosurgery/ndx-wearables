from pynwb.spec import NWBGroupSpec, NWBDatasetSpec
from datetime import datetime
from dateutil.tz import tzlocal
import numpy as np
from pynwb import register_class
from ndx_wearables import WearableTimeSeries

@register_class('HRVSeries', 'ndx-wearables')
class HRVSeries(WearableTimeSeries):
    """HRV data stored as a wearable time series"""
    pass

def make_hrv_stage():
    hrv_series = NWBGroupSpec(
        doc='Stores HRV values as strings over time.',
        neurodata_type_def='HRVSeries',
        neurodata_type_inc='WearableTimeSeries',
    )

    return hrv_series 

from ndx_wearables import WearableTimeSeries
from pynwb import register_class

