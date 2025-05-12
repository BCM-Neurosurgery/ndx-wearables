import pytz
import pytest
from pathlib import Path
from datetime import datetime
from pynwb.file import ProcessingModule
from ndx_events import NdxEventsNWBFile, MeaningsTable, CategoricalVectorData
from ndx_wearables import WearableDevice, WearableTimeSeries, WearableEvents


def make_wearables_nwbfile():
    nwbfile = NdxEventsNWBFile(
        session_description="Example wearables study session",
        identifier='TEST_WEARABLES',
        session_start_time=datetime.now(pytz.timezone('America/Chicago')),
    )

    # create processing module
    wearables_module = ProcessingModule(
        name="wearables",
        description="Wearables data",
    )

    nwbfile.add_processing_module(wearables_module)
    return nwbfile

def add_wearables_device(nwbfile):
    # create wearables device
    device = WearableDevice(name="test_wearable_device", description="test", location="arm", manufacturer="test")
    nwbfile.add_device(device)

    return nwbfile, device

@pytest.fixture
def tmp_path():
    return Path('./src/pynwb/tests')

@pytest.fixture
def wearables_nwbfile():
    return make_wearables_nwbfile()

@pytest.fixture
def wearables_nwbfile_device(wearables_nwbfile):
    wearables_module, nwbfile = wearables_nwbfile
    return add_wearables_device(nwbfile)