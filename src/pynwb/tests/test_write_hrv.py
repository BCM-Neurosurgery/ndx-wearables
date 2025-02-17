import numpy as np
from pynwb import NWBFile, NWBHDF5IO
from pynwb.base import ProcessingModule
from datetime import datetime
from ndx_wearables import HRVSeries #Assuming HRVSeries is correctly implemented in ndx_wearables/yaml file
import pytz

timestamps = np.arange(0., 3600, 30)
# HRV often expressed in milliseconds or as a unitless measure
heart_rate_values = #TODO: Incorporate BPM values from the wearable 
timestamps = np.arange(0, len(heart_rate_values), 1)  # Assuming HR data is collected every second

# Compute R-R intervals in milliseconds
rr_intervals = 60000 / heart_rate_values  # Convert BPM to R-R intervals in ms

nwbfile = NWBFile(
    session_description='HRV data collected from wearable device',
    identifier='ID125',
    session_start_time=datetime.now(pytz.timezone('America/Chicago'))
)

# Creating a time series for HRV from heart rate data
hrv_series = HRVSeries(
    name='HRV_RR_Intervals',
    data=rr_intervals,
    unit='ms',  # HRV is measured in milliseconds
    timestamps=timestamps,
    description='R-R intervals computed from heart rate collected from wearable'
)

# Create a processing module for HRV data
hrv_module = ProcessingModule(
    name='cardiac_health',
    description='R-R interval data stored for HRV analysis'
)

hrv_module.add(hrv_series)
nwbfile.add_processing_module(hrv_module)

# Write the data to an NWB file
with NWBHDF5IO('hrv_study.nwb', 'w') as io:
    io.write(nwbfile)