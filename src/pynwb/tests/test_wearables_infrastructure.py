import pytest
import numpy as np
from datetime import datetime
import pytz
from pynwb import NWBFile, NWBHDF5IO
from pynwb.base import TimeSeries
from pynwb.file import ProcessingModule
from pathlib import Path
from ndx_wearables import WearableDevice, WearableSensor, WearableTimeSeries, PhysiologicalMeasure

@pytest.fixture
def tmp_path():
    return Path('/Users/diazlc1/Desktop/EMBER/ndx-wearables')

@pytest.fixture
def nwb_with_wearables_data(tmp_path):
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
    ts = WearableTimeSeries(name="test_wearable_timeseries", sensor=sensor, data=wearable_values, timestamps=timestamps, unit='test')

    # add wearables objects to processing module
    nwbfile.processing["wearables_module"].add_container(ts)

    file_path = tmp_path / "wearables_test.nwb"
    with NWBHDF5IO(file_path, 'w') as io:
        io.write(nwbfile)
    
    return file_path

def test_wearables_read(nwb_with_wearables_data):
    expected_timestamps = np.arange(0, 3600, 30)
    np.random.seed(0)
    expected_wearable_values = np.random.random(size=(120,2))

    with NWBHDF5IO(nwb_with_wearables_data, 'r') as io:
        nwbfile = io.read()

        # ensure processing module is in the file
        assert 'wearables_module' in nwbfile.processing, 'Wearables processing module is missing.'
        wearables_module = nwbfile.processing["wearables_module"]

        # ensure wearable timeseries is in file
        assert 'test_wearable_timeseries' in wearables_module.data_interfaces, "Wearable timeseries data not present in processing module"
        # ensure data is correct
        wearable_timeseries = wearables_module.get('test_wearable_timeseries')
        # validate shape
        assert wearable_timeseries.data.shape == expected_wearable_values.shape, "Incorrect wearables timeseries data shape"
        assert wearable_timeseries.timestamps.shape == expected_wearable_values.shape, "Incorrect timestamp shape"
        # validate data values
        np.testing.assert_array_equal(wearable_timeseries.data[:], expected_wearable_values, "Mismatch in wearable timeseries values")
        np.testing.assert_array_equal(wearable_timeseries.timestamps[:], expected_timestamps, "Mismatch in timestamps")
        
        # validate metadata
        assert wearable_timeseries.sensor.name == "test_wearable_sensor", "Sensor not referenced in wearable timeseries"
        assert wearable_timeseries.sensor.device.name == "test_wearable_device", "Device not referenced in wearable sensor"
        assert wearable_timeseries.sensor.device.location == "arm", "Device location incorrect"
        assert wearable_timeseries.sensor.device.manufacturer == "test", "Device manufacturer incorrect"

        


