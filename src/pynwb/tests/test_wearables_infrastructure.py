"""
Note: tests expect to be run from the ndx-wearables repo root.
Validates core infra: WearableDevice, WearableTimeSeries, and (optionally) WearableEvents.
"""

import numpy as np
import pytest
from pynwb import NWBHDF5IO

from ndx_wearables import WearableDevice, WearableTimeSeries

# ndx_events / events compatibility 

WearableEvents = None
MeaningsTable = None
CategoricalVectorData = None

try:
    # Our extension might expose WearableEvents directly
    from ndx_wearables import WearableEvents as _WE  # type: ignore
    WearableEvents = _WE
except Exception:
    try:
        # ndx_events variants
        from ndx_events import EventsRecord as _WE  # type: ignore
        WearableEvents = _WE
    except Exception:
        try:
            from ndx_events import Events as _WE  # type: ignore
            WearableEvents = _WE
        except Exception:
            WearableEvents = None

try:
    from ndx_events import MeaningsTable as _MT, CategoricalVectorData as _CVD  # type: ignore
    MeaningsTable, CategoricalVectorData = _MT, _CVD
except Exception:
    MeaningsTable, CategoricalVectorData = None, None

# Helpers

def add_wearable_timeseries(nwbfile, device: WearableDevice):
    """Create a simple WearableTimeSeries and add it to the 'wearables' module."""
    #timestamps = np.arange(0, 3600, 30)  # 120 samples, every 30s
    timestamps = np.arange(0.0, 3600.0, 30.0, dtype="float64")
    np.random.seed(0)
    wearable_values = np.random.random(size=(120, 2))

    ts = WearableTimeSeries(
        name="test_wearable_timeseries",
        data=wearable_values,
        timestamps=timestamps,
        unit="tests/s",
        wearable_device=device,
        algorithm="test_algorithm",
    )
    nwbfile.processing["wearables"].add(ts)
    return nwbfile


def add_wearable_events(nwbfile, device: WearableDevice):
    """Create a minimal WearableEvents table and add it to the 'wearables' module."""
    if WearableEvents is None or MeaningsTable is None or CategoricalVectorData is None:
        pytest.skip("No events class/tables available in this environment")

    meanings = MeaningsTable(name="test_meanings", description="test")
    meanings.add_row(value="a", meaning="first value entered")
    meanings.add_row(value="b", meaning="second value entered")

    cat_column = CategoricalVectorData(
        name="cat_column",
        description="test categories description",
        meanings=meanings,
    )
    text_column = VectorData(
        name="text_column",
        description="test columns description",
    )

    events = WearableEvents(
        name="test_wearable_events",
        description=f"test events collected from {device.name}",
        wearable_device=device,
        columns=[cat_column, text_column],
        meanings_tables=[meanings],
        algorithm="test_algorithm",
    )
    events.add_row(timestamp=10.0, cat_column="a", text_column="first row text")
    events.add_row(timestamp=30.0, cat_column="b", text_column="second row text")
    events.add_row(timestamp=120.0, cat_column="a", text_column="third row text")

    nwbfile.processing["wearables"].add(events)
    return nwbfile


# Fixtures (relies on wearables_nwbfile_device from tests/conftest.py)

@pytest.fixture
def nwb_with_wearable_ts(wearables_nwbfile_device):
    nwbfile, device = wearables_nwbfile_device
    return add_wearable_timeseries(nwbfile, device)


@pytest.fixture
def write_nwb_with_wearable_timeseries(tmp_path, nwb_with_wearable_ts):
    out_path = tmp_path / "wearables_ts.nwb"  # MUST be a file, not a directory
    with NWBHDF5IO(out_path, "w") as io:
        io.write(nwb_with_wearable_ts)
    return out_path


@pytest.fixture
def nwb_with_wearable_events(wearables_nwbfile_device):
    nwbfile, device = wearables_nwbfile_device
    return add_wearable_events(nwbfile, device)


@pytest.fixture
def write_nwb_with_wearable_events(tmp_path, nwb_with_wearable_events):
    out_path = tmp_path / "wearables_events.nwb"  # MUST be a file, not a directory
    with NWBHDF5IO(out_path, "w") as io:
        io.write(nwb_with_wearable_events)
    return out_path

# Tests

def test_wearables_timeseries(write_nwb_with_wearable_timeseries):
    expected_timestamps = np.arange(0, 3600, 30)
    np.random.seed(0)
    expected_values = np.random.random(size=(120, 2))

    with NWBHDF5IO(write_nwb_with_wearable_timeseries, "r") as io:
        nwbfile = io.read()

        assert "wearables" in nwbfile.processing, "Wearables processing module is missing."
        wearables_module = nwbfile.processing["wearables"]

        assert "test_wearable_timeseries" in wearables_module.data_interfaces, \
            "Wearable timeseries not present in processing module"

        ts = wearables_module.get("test_wearable_timeseries")

        # shapes
        assert ts.data.shape == expected_values.shape
        assert ts.timestamps.shape == expected_timestamps.shape

        # values
        np.testing.assert_array_equal(ts.data[:], expected_values)
        np.testing.assert_array_equal(ts.timestamps[:], expected_timestamps)

        # device link
        assert "test_wearable_device" in nwbfile.devices
        assert ts.wearable_device is nwbfile.devices["test_wearable_device"]


@pytest.mark.skipif(WearableEvents is None, reason="No events class available in this environment")
def test_wearable_events(write_nwb_with_wearable_events):
    with NWBHDF5IO(write_nwb_with_wearable_events, "r") as io:
        nwbfile = io.read()

        assert "wearables" in nwbfile.processing, "Wearables processing module is missing."
        wearables = nwbfile.processing["wearables"]

        assert "test_wearable_events" in wearables.data_interfaces, "Missing wearable events data."
        events = wearables.get("test_wearable_events")

        all_rows = events.get(slice(None))
        np.testing.assert_array_equal(all_rows.timestamp[:], [10.0, 30.0, 120.0])
        assert events.wearable_device.name == "test_wearable_device"
