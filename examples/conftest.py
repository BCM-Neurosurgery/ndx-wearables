
from pathlib import Path
from examples import make_wearables_nwbfile, add_wearables_device

def tmp_path():
    return Path('./examples/test_nwb_file.nwb')
    #return Path('./src/pynwb/tests/test_nwb_file.nwb')

def wearables_nwbfile():
    nwbfile = make_wearables_nwbfile()
    return nwbfile

def wearables_nwbfile_device(wearables_nwbfile):
    nwbfile = wearables_nwbfile
    nwbfile, device = add_wearables_device(nwbfile)
    return nwbfile, device