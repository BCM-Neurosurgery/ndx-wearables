import pytest
import numpy as np
from datetime import datetime
import pytz
from pynwb import NWBFile, NWBHDF5IO
from pynwb.file import ProcessingModule
from ndx_wearables import DeviceBloodOxygen, DeviceBreathingDisturbance, BloodOxygenGroup

@pytest.fixture
def nwb_with_blood_oxygen(tmp_path):
    '''
    Creates a temporary NWB file with DeviceBloodOxygenSeries for testing.
    Returns the file path.
    '''
    nwbfile = NWBFile(
        session_description='Example blood oxygen study session',
        identifier='TEST_BLOOD_OXYGEN',
        session_start_time=datetime.now(pytz.timezone('America/Chicago')),
    )

    spo2_group = BloodOxygenGroup()

    # Generate sample data
    timestamps = np.arange(0., 365*24*60*60, 24*60*60)  # Once per day for 1 year, in seconds
    blood_oxygen_data = np.random.RandomState(42).uniform(90, 100, size=len(timestamps))
    breathing_disturbance_data = np.random.RandomState(42).uniform(0, 100, size=len(timestamps))

    # Create sample DeviceBloodOxygen and DeviceBreathingDisturbance series
    blood_oxygen_series_apple_watch = DeviceBloodOxygen(
        name='Blood Oxygen Apple Watch',
        data=blood_oxygen_data,
        unit='%',
        timestamps=timestamps,
        description='Example blood oxygen data'
    )
    blood_oxygen_series_samsung_watch = DeviceBloodOxygen(
        name='Blood Oxygen Samsung Watch',
        data=blood_oxygen_data-1, # Say that Samsung underestimates values compared to Apple
        unit='%',
        timestamps=timestamps,
        description='Example blood oxygen data'
    )
    breathing_disturbance_series_oura_ring = DeviceBreathingDisturbance(
        name='Breathing Disturbance Index Oura Ring',
        data=breathing_disturbance_data,
        unit='n/a',
        timestamps=timestamps,
        description='Example breathing disturbance index data'
    )
    breathing_disturbance_series_samsung_ring = DeviceBreathingDisturbance(
        name='Breathing Disturbance Index Samsung Ring',
        data=breathing_disturbance_data-1, # Say that Samsung underestimates values compared to Oura
        unit='n/a',
        timestamps=timestamps,
        description='Example breathing disturbance index data'
    )

    spo2_group.add_device_blood_oxygens([blood_oxygen_series_apple_watch, blood_oxygen_series_samsung_watch])
    spo2_group.add_device_breathing_disturbances([breathing_disturbance_series_oura_ring, breathing_disturbance_series_samsung_ring])

    # Add to a processing module
    blood_oxygen_module = ProcessingModule(
        name='blood_oxygen',
        description='Blood oxygen and breathing disturbance data'
    )
    blood_oxygen_module.add(spo2_group)
    nwbfile.add_processing_module(blood_oxygen_module)

    # Save NWB file to a temporary directory
    file_path = tmp_path / 'test_blood_oxygen.nwb'
    with NWBHDF5IO(file_path, 'w') as io:
        io.write(nwbfile)

    return file_path

def test_blood_oxygen_write_read(nwb_with_blood_oxygen):
    '''
    Test that DeviceBloodOxygenSeries can be written and read from an NWB file.
    '''
    # Regenerate the expected test data
    expected_timestamps = np.arange(0., 365*24*60*60, 24*60*60)  # Once per day for 1 year, in seconds
    expected_blood_oxygen_data = np.random.RandomState(42).uniform(90, 100, size=len(expected_timestamps))
    expected_breathing_disturbance_data = np.random.RandomState(42).uniform(0, 100, size=len(expected_timestamps))

    # Read the NWB file
    with NWBHDF5IO(nwb_with_blood_oxygen, 'r') as io:
        nwbfile = io.read()

        # Check that the processing module exists
        assert 'blood_oxygen' in nwbfile.processing, 'Blood oxygen module is missing.'

        # Check that the BloodOxygenSeries exists
        blood_oxygen_module = nwbfile.processing['blood_oxygen']
        assert 'blood_oxygen' in blood_oxygen_module.data_interfaces, 'BloodOxygenGroup is missing.'

        blood_oxygen_group = blood_oxygen_module['blood_oxygen']

        blood_oxygen_apple_watch = blood_oxygen_group.get_device_blood_oxygens('Blood Oxygen Apple Watch')
        blood_oxygen_samsung_watch = blood_oxygen_group.get_device_blood_oxygens('Blood Oxygen Samsung Watch')
        breathing_disturbance_oura_ring = blood_oxygen_group.get_device_breathing_disturbances('Breathing Disturbance Index Oura Ring')
        breathing_disturbance_samsung_ring = blood_oxygen_group.get_device_breathing_disturbances('Breathing Disturbance Index Samsung Ring')

        # Validate shapes
        assert blood_oxygen_apple_watch.data.shape == expected_blood_oxygen_data.shape, "Incorrect blood oxygen data shape (Apple watch)."
        assert blood_oxygen_samsung_watch.data.shape == expected_blood_oxygen_data.shape, "Incorrect blood oxygen data shape (Samsung watch)."
        assert blood_oxygen_apple_watch.timestamps.shape == expected_timestamps.shape, "Incorrect blood oxygen timestamp shape (Apple watch)."
        assert blood_oxygen_samsung_watch.timestamps.shape == expected_timestamps.shape, "Incorrect blood oxygen timestamp shape (Samsung watch)."
        
        assert breathing_disturbance_oura_ring.data.shape == expected_blood_oxygen_data.shape, "Incorrect BDI data shape (Oura ring)."
        assert breathing_disturbance_samsung_ring.data.shape == expected_blood_oxygen_data.shape, "Incorrect BDI data shape (Samsung ring)."
        assert breathing_disturbance_oura_ring.timestamps.shape == expected_timestamps.shape, "Incorrect BDI timestamp shape (Oura ring)."
        assert breathing_disturbance_samsung_ring.timestamps.shape == expected_timestamps.shape, "Incorrect BDI timestamp shape (Samsung ring)."

        # Validate actual data values
        np.testing.assert_array_equal(blood_oxygen_apple_watch.data[:].astype(float), expected_blood_oxygen_data, "Mismatch in blood oxygen values (Apple watch).")
        np.testing.assert_array_equal(blood_oxygen_samsung_watch.data[:].astype(float), expected_blood_oxygen_data-1, "Mismatch in blood oxygen values (Samsung watch).")
        np.testing.assert_array_equal(breathing_disturbance_oura_ring.data[:].astype(float), expected_breathing_disturbance_data, "Mismatch in BDI values (Oura ring).")
        np.testing.assert_array_equal(breathing_disturbance_samsung_ring.data[:].astype(float), expected_breathing_disturbance_data-1, "Mismatch in BDI values (Samsung ring).")

        # Validate timestamp values
        np.testing.assert_array_equal(blood_oxygen_apple_watch.timestamps[:].astype(float), expected_timestamps, "Mismatch in blood oxygen timestamps (Apple watch).")
        np.testing.assert_array_equal(blood_oxygen_samsung_watch.timestamps[:].astype(float), expected_timestamps, "Mismatch in blood oxygen timestamps (Samsung watch).")
        np.testing.assert_array_equal(breathing_disturbance_oura_ring.timestamps[:].astype(float), expected_timestamps, "Mismatch in blood oxygen timestamps (Oura ring).")
        np.testing.assert_array_equal(breathing_disturbance_samsung_ring.timestamps[:].astype(float), expected_timestamps, "Mismatch in blood oxygen timestamps (Samsung ring).")

        # Validate metadata
        assert blood_oxygen_apple_watch.description == "Example blood oxygen data", "Incorrect description."
        assert blood_oxygen_samsung_watch.description == "Example blood oxygen data", "Incorrect description."
        assert breathing_disturbance_oura_ring.description == "Example breathing disturbance index data", "Incorrect description."
        assert breathing_disturbance_samsung_ring.description == "Example breathing disturbance index data", "Incorrect description."
