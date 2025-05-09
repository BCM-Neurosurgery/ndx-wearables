"""
Note, tests expect to be run from the ndc-wearables root directory
"""

import pytest
import numpy as np
from datetime import datetime
import pytz
from pynwb import NWBFile, NWBHDF5IO
from pynwb.base import TimeSeries
from pynwb.file import ProcessingModule
from pathlib import Path
from ndx_wearables import WearableDevice, WearableTimeSeries # , WearableEvents

@pytest.fixture
def tmp_path():
    return Path('./src/pynwb/tests')

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

    # create wearable timeseries
    ts = WearableTimeSeries(name="test_wearable_timeseries", data=wearable_values, timestamps=timestamps, unit='test', wearable_device=device)
    #ts.add_wearable_device(device)

    # add wearables objects to processing module
    nwbfile.processing["wearables_module"].add_container(ts)
    nwbfile.add_device(device)

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
        assert wearable_timeseries.timestamps.shape == expected_timestamps.shape, "Incorrect timestamp shape"
        # validate data values
        np.testing.assert_array_equal(wearable_timeseries.data[:], expected_wearable_values, "Mismatch in wearable timeseries values")
        np.testing.assert_array_equal(wearable_timeseries.timestamps[:], expected_timestamps, "Mismatch in timestamps")
        
        # validate metadata
        assert 'test_wearable_device' in nwbfile.devices, "Wearable device is missing"

        # ensure wearabletimeseries has link to wearabledevice
        assert wearable_timeseries.wearable_device is nwbfile.devices['test_wearable_device']

# Testing WearableEvents based on EventsRecord inheritance
def test_wearable_events(nwb_with_wearables_data):
    with NWBHDF5IO(nwb_with_wearables_data, 'r+') as io:
        nwbfile = io.read()
        wearables_module = nwbfile.processing["wearables_module"]

        # Create events
        timestamps = np.array([0.0, 60.0, 120.0])  # example workout start times
        event = WearableEvents(
            name="workout_event",
            wearable_device=nwbfile.devices['test_wearable_device'],
            timestamps=timestamps,
            description="Workout start times"
        )

        # Create a new processing module
        if "event_module" not in nwbfile.processing:
            event_module = ProcessingModule(name="event_module", description="Events data")
            nwbfile.add_processing_module(event_module)
        else:
            event_module = nwbfile.processing["event_module"]

        event_module.add(event)

        # Reopen and validate
        io.write(nwbfile)

    with NWBHDF5IO(nwb_with_wearables_data, 'r') as io:
        nwbfile = io.read()
        assert 'event_module' in nwbfile.processing, "Events processing module is missing"

        event_module = nwbfile.processing["event_module"]
        assert 'workout_event' in event_module.data_interfaces, "Workout event not present in event module"

        workout_event = event_module.get('workout_event')
        np.testing.assert_array_equal(workout_event.timestamps[:], [0.0, 60.0, 120.0])
        assert workout_event.device.name == "test_wearable_device"

