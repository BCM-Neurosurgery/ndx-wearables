from pynwb.spec import NWBGroupSpec, NWBDatasetSpec
from datetime import datetime
from dateutil.tz import tzlocal
import numpy as np
from pynwb import register_class
from ndx_wearables import WearableTimeSeries  

@register_class('VO2maxSeries', 'ndx-wearables')
class VO2maxSeries(WearableTimeSeries):
    """VO2 max data stored as a wearable time series"""
    pass

def make_vo2max_stage():
    vo2max_series = NWBGroupSpec(
        doc='Stores Vo2 max values as raw strings over time.',
        neurodata_type_def='VO2maxSeries',
        neurodata_type_inc='WearableTimeSeries',
    )
        
    return vo2max_series