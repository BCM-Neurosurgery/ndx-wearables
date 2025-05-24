import pytest
import numpy as np
from datetime import datetime
import pytz
from pynwb import NWBFile, NWBHDF5IO
from pynwb.file import ProcessingModule
from ndx_wearables import HeartRateSeries  # Assumes HeartRateSeries is registered in the namespace and accessible via get_class

def add_heart_rate_data(nwbfile, device):
    # Generate heart rate data
    timestamps = np.arange(0., 3600, 5)  # Every 5 seconds for 1 hour
    np.random.seed(42)
    #heart_rate_values = np.random.randint(60, 100, size=120)  # Random BPM values
    heart_rate_values = np.random.randint(60, 100, size=len(timestamps))  # 721 values


    # Create HeartRateSeries object
    heart_rate_series = HeartRateSeries(
        name='HeartRate Data',
        data=heart_rate_values,
        unit='bpm',  # Beats per minute
        timestamps=timestamps,
        description='Example HeartRate data',
        wearable_device=device  #  Must be accepted via WearableTimeSeries
    )

    # Add heart rate data to the wearables processing module
    def add_heart_rate_data(nwbfile, device):
        # Step 1: Generate heart rate data
        timestamps = np.arange(0., 3600, 5)
        np.random.seed(42)
        heart_rate_values = np.random.randint(60, 100, size=len(timestamps))

        # Step 2: Create HeartRateSeries for this device
        heart_rate_series = HeartRateSeries(
            name=f"{device.name}_heart_rate",
            data=heart_rate_values,
            unit='bpm',
            timestamps=timestamps,
            description='Heart rate data from wrist sensor',
            wearable_device=device
        )

        # Step 3: Get or create the 'wearables' processing module
        if "wearables" not in nwbfile.processing:
            wearables_module = nwbfile.create_processing_module(
                name="wearables",
                description="Wearable device data"
            )
        else:
            wearables_module = nwbfile.processing["wearables"]

        # Step 4: Get or create the 'heart_rate' modality container
        if "heart_rate" not in wearables_module.data_interfaces:
            heart_rate_container = ProcessingModule(name="heart_rate", description="Heart rate modality")
            wearables_module.add(heart_rate_container)
        else:
            heart_rate_container = wearables_module["heart_rate"]

        # Step 5: Add device-specific HeartRateSeries to the modality
        heart_rate_container.add(heart_rate_series)

    return nwbfile



@pytest.fixture
def nwb_with_heart_rate_data(wearables_nwbfile_device):
    nwbfile, device = wearables_nwbfile_device
    nwbfile = add_heart_rate_data(nwbfile, device)
    return nwbfile


@pytest.fixture
def write_nwb_with_heart_rate_data(tmp_path, nwb_with_heart_rate_data):
    with NWBHDF5IO(tmp_path, 'w') as io:
        io.write(nwb_with_heart_rate_data)
    return tmp_path


def test_heart_rate_write_read(write_nwb_with_heart_rate_data):
    '''
    Test that HeartRateSeries can be written and read from an NWB file.
    '''
    # Expected test data
    np.random.seed(42)
    expected_heart_rate_values = np.random.randint(60, 100, size=720)
    expected_timestamps = np.arange(0., 3600, 5)

    # Read the NWB file
    with NWBHDF5IO(write_nwb_with_heart_rate_data, 'r') as io:
        nwbfile = io.read()

        # Confirm wearables module exists
        assert 'wearables' in nwbfile.processing, 'Wearables processing module is missing.'

        # Check the HeartRateSeries interface
        wearables = nwbfile.processing['wearables']
        assert 'HeartRate Data' in wearables.data_interfaces, 'HeartRateSeries is missing.'

        heart_rate_series = wearables.get('HeartRate Data')

        # Validate shape and content
        assert heart_rate_series.data.shape == expected_heart_rate_values.shape, "Incorrect data shape."
        assert heart_rate_series.timestamps.shape == expected_timestamps.shape, "Incorrect timestamp shape."
        np.testing.assert_array_equal(heart_rate_series.data[:], expected_heart_rate_values)
        np.testing.assert_array_equal(heart_rate_series.timestamps[:], expected_timestamps)
