import pytest
import numpy as np
from datetime import datetime
import pytz
from pynwb import NWBFile, NWBHDF5IO
from pynwb.file import ProcessingModule
from ndx_wearables import HeartRateSeries  # Assumes HeartRateSeries is registered in the namespace and accessible via get_class


def add_heart_rate_data(nwbfile, device):
    # Step 1: Generate heart rate data
    timestamps = np.arange(0., 3600, 5)
    np.random.seed(42)
    heart_rate_values = np.random.randint(60, 100, size=len(timestamps))

    # Step 2: Create HeartRateSeries
    heart_rate_series = HeartRateSeries(
        name=f"{device.name}_heart_rate",
        data=heart_rate_values,
        unit='bpm',
        timestamps=timestamps,
        description='Heart rate data from wrist sensor',
        wearable_device=device
    )

    # Step 3: Create or get 'wearables'
    if "wearables" not in nwbfile.processing:
        wearables_module = nwbfile.create_processing_module(
            name="wearables",
            description="Wearable device data"
        )
    else:
        wearables_module = nwbfile.processing["wearables"]

    # Step 4: Create or get 'heart_rate'
    if "heart_rate" not in wearables_module.data_interfaces:
        heart_rate_container = ProcessingModule(name="heart_rate", description="Heart rate modality")
        wearables_module.add(heart_rate_container)
    else:
        heart_rate_container = wearables_module["heart_rate"]

    # Step 5: Add the HeartRateSeries to the 'heart_rate' container
    heart_rate_container.add(heart_rate_series)

    return nwbfile


@pytest.fixture
def nwb_with_heart_rate_data(wearables_nwbfile_device):
    nwbfile, device = wearables_nwbfile_device
    nwbfile = add_heart_rate_data(nwbfile, device)
    return nwbfile, device  # ✅ Return both


@pytest.fixture
def write_nwb_with_heart_rate_data(tmp_path, nwb_with_heart_rate_data):
    nwbfile, device = nwb_with_heart_rate_data
    file_path = tmp_path / "test_heart_rate.nwb"
    with NWBHDF5IO(file_path, 'w') as io:
        io.write(nwbfile)
    return file_path, device  # ✅ Return both


def test_heart_rate_write_read(write_nwb_with_heart_rate_data):
    '''
    Test that HeartRateSeries can be written and read from an NWB file.
    '''
    file_path, device = write_nwb_with_heart_rate_data

    # Expected test data
    np.random.seed(42)
    expected_heart_rate_values = np.random.randint(60, 100, size=720)
    expected_timestamps = np.arange(0., 3600, 5)

    # Read the NWB file
    with NWBHDF5IO(file_path, 'r') as io:
        nwbfile = io.read()

        # Confirm wearables module exists
        assert 'wearables' in nwbfile.processing, 'Wearables processing module is missing.'

        # Check the HeartRateSeries interface
        wearables = nwbfile.processing['wearables']
        assert 'heart_rate' in wearables.data_interfaces, 'Heart rate modality missing.'

        heart_rate_modality = wearables['heart_rate']
        expected_series_name = f"{device.name}_heart_rate"
        assert expected_series_name in heart_rate_modality.data_interfaces, f'{expected_series_name} is missing.'

        heart_rate_series = heart_rate_modality[expected_series_name]

        # Validate shape and content
        assert heart_rate_series.data.shape == expected_heart_rate_values.shape, "Incorrect data shape."
        assert heart_rate_series.timestamps.shape == expected_timestamps.shape, "Incorrect timestamp shape."
        np.testing.assert_array_equal(heart_rate_series.data[:], expected_heart_rate_values)
        np.testing.assert_array_equal(heart_rate_series.timestamps[:], expected_timestamps)
