from pynwb.spec import NWBGroupSpec, NWBDatasetSpec

from datetime import datetime
from dateutil.tz import tzlocal
import numpy as np

def make_vo2max_stage():
    vo2max_series = NWBGroupSpec(
        doc='Stores Vo2 max values as raw strings over time.',
        datasets=[
            NWBDatasetSpec(
                name='data',
                dtype='text',
                doc='Vo2 max valuess'
            )
        ],
        neurodata_type_def='VO2maxSeries',
        neurodata_type_inc='TimeSeries',
    )
        
    return vo2max_series