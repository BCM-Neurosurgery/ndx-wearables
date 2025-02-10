import numpy as np
from pynwb import NWBFile, NWBHDF5IO
from pynwb.base import ProcessingModule
from datetime import datetime
from ndx_wearables import SleepStageSeries
import pytz

timestamps = np.arange(0., 3600, 30)
stages = np.random.choice(['awake', 'light_sleep', 'deep_sleep', 'rem'], size=len(timestamps))

nwbfile = NWBFile(
    session_description='Example sleep study session',
    identifier='ID123',
    session_start_time=datetime.now(pytz.timezone('America/Chicago'))
)

sleep_stage_series = SleepStageSeries(
    name='Sleep Stages',
    data=stages,
    unit='stage',
    timestamps=timestamps,
    description='Example sleep stage data'
)

sleep_module = ProcessingModule(
    name='sleep',
    description='Sleep stage data'
)
sleep_module.add(sleep_stage_series)
nwbfile.add_processing_module(sleep_module)

with NWBHDF5IO('sleep_study.nwb', 'w') as io:
    io.write(nwbfile)
