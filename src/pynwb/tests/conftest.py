# src/pynwb/tests/conftest.py
import sys
from pathlib import Path
import pytest

# Ensure the package under src/pynwb is importable
REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = REPO_ROOT / "src" / "pynwb"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

# Import after sys.path fix so ndx_wearables loads its namespace
from pynwb import NWBFile, get_class  
from datetime import datetime, timezone 


# Legacy helper API (so existing tests won't break) 
def make_wearables_nwbfile():
    """
    Legacy helper: create a minimal NWBFile with tz-aware start_time and a
    'wearables' processing module.
    """
    nwb = NWBFile(
        session_description="pytest ndx-wearables",
        identifier="pytest-ndx-wearables",
        session_start_time=datetime.now(timezone.utc),
    )
    nwb.create_processing_module(name="wearables", description="Wearables derived data")
    return nwb


def add_wearables_device(nwb, name="test_wearable_device"):
    """
    Legacy helper: add a WearableDevice to the file and return it.
    """
    WearableDevice = get_class("WearableDevice", "ndx-wearables")
    dev = WearableDevice(
        name=name,
        manufacturer="PyTestCo",
        description="device for tests",
        location="left_wrist",
    )
    nwb.add_device(dev)
    return dev


# Pytest fixtures 

@pytest.fixture(scope="session")
def wearables_pkg():
    """Import ndx_wearables once to ensure its namespace is loaded."""
    import ndx_wearables  
    return ndx_wearables


@pytest.fixture
def wearables_nwbfile_device(wearables_pkg):
    """Provide (NWBFile, WearableDevice) with a wearables processing module."""
    nwb = make_wearables_nwbfile()
    dev = add_wearables_device(nwb)
    return nwb, dev
