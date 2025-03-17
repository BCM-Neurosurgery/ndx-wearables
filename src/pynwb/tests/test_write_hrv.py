import numpy as np
from pynwb import NWBFile, NWBHDF5IO
from pynwb.base import ProcessingModule
from datetime import datetime
from ndx_wearables import HRVSeries #Assuming HRVSeries is correctly implemented in ndx_wearables/yaml file
import pytz


@pytest.fixture
def nwb_with_hrv_data(tmp_path):
    '''
    Creates a NWB file with HRVSeries for testing.
    Returns the file path.
    '''
    nwbfile = NWBFile(
        session_description='Example HRV study session',
        identifier='TEST_HRV',
        session_start_time=datetime.now(pytz.timezone('America/Chicago')),
    )

    # Generate heart rate data
    heart_rate_values = np.random.randint(60, 100, size=120)  # Random BPM values
    timestamps = np.arange(0, len(heart_rate_values), 1)  # Assuming HR data is collected every second

    # Create HRVSeries object
    hrv_series = HRVSeries(
        name='HRV Data',
        data=heart_rate_values,
        unit='bpm',  # Beats per minute
        timestamps=timestamps,
        description='Example HRV data'
    )

    # Add to a processing module
    cardiac_module = ProcessingModule(
        name='cardiac_health',
        description='HRV data'
    )
    cardiac_module.add(hrv_series)
    nwbfile.add_processing_module(cardiac_module)

    # Save NWB file
    file_path = tmp_path / 'hrv_study.nwb'
    with NWBHDF5IO(file_path, 'w') as io:
        io.write(nwbfile)

    return file_path

def test_hrv_write_read(nwb_with_hrv_data):
    '''
    Test that HRVSeries can be written and read from an NWB file.
    '''
    # Regenerate the expected test data
    expected_heart_rate_values = np.random.randint(60, 100, size=120)
    expected_timestamps = np.arange(0, len(expected_heart_rate_values), 1)

    # Read the NWB file
    with NWBHDF5IO(nwb_with_hrv_data, 'r') as io:
        nwbfile = io.read()

        # Check that the processing module exists
        assert 'cardiac_health' in nwbfile.processing, 'Cardiac health processing module is missing.'

        # Check that the HRVSeries exists
        cardiac_data = nwbfile.processing['cardiac_health']
        assert 'HRV Data' in cardiac_data.data_interfaces, 'HRVSeries is missing.'

        hrv_series = cardiac_data.get('HRV Data')

        # Validate shape
        assert hrv_series.data.shape == expected_heart_rate_values.shape, "Incorrect HRV data shape."
        assert hrv_series.timestamps.shape == expected_timestamps.shape, "Incorrect timestamp shape."

        # Validate actual data values (IMPORTANT)
        np.testing.assert_array_equal(hrv_series.data[:], expected_heart_rate_values, "Mismatch in HRV values.")
        np.testing.assert_array_equal(hrv_series.timestamps[:], expected_timestamps, "Mismatch in timestamps.")

        # Validate metadata
        assert hrv_series.description == "Example HRV data", "Incorrect description."

