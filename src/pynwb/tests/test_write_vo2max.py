import numpy as np
from pynwb import NWBFile, NWBHDF5IO
from pynwb.base import ProcessingModule
from datetime import datetime
from ndx_wearables import VO2maxSeries
import pytz

timestamps = np.arange(0., 3600, 30)
vo2max_data_values = np.random.uniform(low=30, high=70, size=len(timestamps))  # VO2max values in mL/kg/min

# Create an NWB file
nwbfile = NWBFile(
    session_description='Example VO2max exercise session',
    #Different than sleep stage
    identifier='ID124',
    session_start_time=datetime.now(pytz.timezone('America/Chicago'))
)

# Creating a time series for VO2max data
vo2max_series = VO2maxSeries(
    name='VO2max',
    data=vo2max_data_values,
    unit='mL/kg/min',
    timestamps=timestamps,
    description='Example VO2max data collected during an exercise test'
)

vo2max_module = ProcessingModule(
    name='exercise',
    description='VO2max data collected during an exercise session'
)
vo2max_module.add(vo2max_series)
nwbfile.add_processing_module(vo2max_module)

# Write the data to an NWB file
with NWBHDF5IO('vo2max_study.nwb', 'w') as io:
    io.write(nwbfile)