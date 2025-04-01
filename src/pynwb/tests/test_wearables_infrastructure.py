import pytest
import numpy as np
from datetime import datetime
import pytz
from pynwb import NWBFile, NWBHDF5IO
from pynwb.base import TimeSeries
from pynwb.file import ProcessingModule
from ndx_wearables import WearableDevice, WearableSensor, WearableTimeSeries, PhysiologicalMeasure

@pytest.fixture
def nwb_with_wearables_data(tmp_path):
    print('here')
    nwbfile = NWBFile(
        session_description = "Example wearables study session",
        identifier='TEST_WEARABLES',
        session_start_time = datetime.now(pytz.timezone('America/Chicago')),
    )

    # generate fake wearables data
    timestamps = np.arange(0, 3600, 30)
    np.random.seed(0)
    wearable_values = np.random.random(size=(120,2))

    # create processing module
    wearables_module = ProcessingModule(
        name = "wearables_module",
        description = "Wearables data",
    )

    nwbfile.add_processing_module(wearables_module)

    # create wearables device
    device = WearableDevice(name="test_wearable_device", description="test", location="arm", manufacturer="test")

    # create wearable sensor
    sensor = WearableSensor(name="test_wearable_sensor", description="test", device=device)

    # create wearable timeseries
    normal_ts = TimeSeries(name="test_timeseries", data=wearable_values, timestamps=timestamps, unit='test')
    ts = WearableTimeSeries(name="test_wearable_timeseries", sensor=sensor, data=normal_ts)#, timestamps=timestamps)

    # create physiological measure
    pm = PhysiologicalMeasure(wearable_timeseries=ts) # name is automatically physiological_measure

    # add wearables objects to processing module
    nwbfile.processing["wearables_module"].add(device)
    nwbfile.processing["wearables_module"].add(sensor)
    nwbfile.processing["wearables_module"].add(pm)

    file_path = tmp_path / "wearables_test.nwb"
    with NWBHDF5IO(file_path, 'w') as io:
        io.write(nwbfile)
    
    return file_path

def test_wearables_read(nwb_with_wearables_data):
    expected_timestamps = np.arange(0, 3600, 30)
    np.random.seed(0)
    expected_wearable_values = np.random(0, 1, size=120)

    with NWBHDF5IO(nwb_with_wearables_data, 'r') as io:
        nwbfile = io.read()

        # ensure processing module is in the file
        assert 'wearables_module' in nwbfile.processing, 'Wearables processing module is missing.'
        print('here')
        wearables_module = nwbfile.processing["wearables_module"]
        # ensure device is in file
        assert 'test_wearable_device' in wearables_module
        # ensure sensor is in file
        # ensure physiological measure is in file
        # ensure wearable timeseries is in physiological measure
        


