from pynwb.spec import NWBGroupSpec, NWBDatasetSpec

from datetime import datetime
from dateutil.tz import tzlocal
import numpy as np

def make_hrv_stage():
    hrv_series = NWBGroupSpec(
        doc='Stores HRV values as strings over time.',
        datasets=[
            NWBDatasetSpec(
                name='data',
                dtype='int',
                doc='HRV calculated values'
            )
        ],
        neurodata_type_def='HRVSeries',
        neurodata_type_inc='TimeSeries',
    )

    return hrv_series 
