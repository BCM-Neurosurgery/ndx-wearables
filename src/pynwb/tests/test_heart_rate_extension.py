import pytest
import numpy as np
from datetime import datetime
from dateutil.tz import tzlocal
from pynwb import NWBFile, NWBHDF5IO
from ndx_wearables import HeartRateSeries, WearableDevice


def add_heart_rate_data(nwbfile, device):
    print("[DEBUG] Entered add_heart_rate_data")

    timestamps = np.arange(0., 3600, 5)
    np.random.seed(42)
    heart_rate_values = np.random.randint(60, 100, size=len(timestamps))

    heart_rate_series = HeartRateSeries(
    name=f"heart_rate_{device.name}",
        data=heart_rate_values,
        unit='bpm',
        timestamps=timestamps,
        description='Heart rate data from wrist sensor',
        wearable_device=device
    )

    print("[DEBUG] Added series:", heart_rate_series.name)

    if "wearables" not in nwbfile.processing:
        wearables_module = nwbfile.create_processing_module(
            name="wearables",
            description="Wearable device data"
        )
    else:
        wearables_module = nwbfile.processing["wearables"]

    wearables_module.add(heart_rate_series)

    print("[DEBUG] wearables module contents:", list(nwbfile.processing["wearables"].data_interfaces.keys()))
    return nwbfile


@pytest.fixture
def wearables_nwbfile_device():
    nwbfile = NWBFile(
        session_description='Heart rate test session',
        identifier='HR123',
        session_start_time=datetime(2024, 1, 1, tzinfo=tzlocal())
    )

    device = WearableDevice(
        name="test_device",
        manufacturer="test",
        description="test",
        location="arm"
    )

    nwbfile.add_device(device)
    return nwbfile, device


@pytest.fixture
def write_nwb_with_heart_rate_data(tmp_path_factory, wearables_nwbfile_device):
    nwbfile, device = wearables_nwbfile_device
    nwbfile = add_heart_rate_data(nwbfile, device)

    file_path = tmp_path_factory.mktemp("nwb") / "test_heart_rate.nwb"
    with NWBHDF5IO(str(file_path), 'w') as io:
        io.write(nwbfile)

    return file_path, device


def test_heart_rate_write_read(write_nwb_with_heart_rate_data):
    file_path, device = write_nwb_with_heart_rate_data

    np.random.seed(42)
    expected_heart_rate_values = np.random.randint(60, 100, size=720)
    expected_timestamps = np.arange(0., 3600, 5)

    with NWBHDF5IO(str(file_path), 'r') as io:
        nwbfile = io.read()

        assert 'wearables' in nwbfile.processing
        wearables = nwbfile.processing['wearables']

        expected_series_name = f"heart_rate_{device.name}"  
        assert expected_series_name in wearables.data_interfaces

        heart_rate_series = wearables[expected_series_name]

        assert heart_rate_series.data.shape == expected_heart_rate_values.shape
        assert heart_rate_series.timestamps.shape == expected_timestamps.shape
        np.testing.assert_array_equal(heart_rate_series.data[:], expected_heart_rate_values)
        np.testing.assert_array_equal(heart_rate_series.timestamps[:], expected_timestamps)
