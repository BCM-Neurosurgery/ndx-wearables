from pynwb import NWBFile, NWBHDF5IO

with NWBHDF5IO('hrv_study.nwb', 'r') as io:
    nwbfile = io.read()
    hrv_data = nwbfile.processing['hrv']
    hrv = hrv_data.get('HRV')
    print('HRV data:',  hrv.data[:])
    print('Timestamps:',  hrv.timestamps[:]) 