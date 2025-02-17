from pynwb import NWBFile, NWBHDF5IO

with NWBHDF5IO('hrv_study.nwb', 'r') as io:
    nwbfile = io.read()
    hrv_data = nwbfile.processing['hrv']
    hrv_max = hrv_data.get('HRV')
    print('HRV data:',  hrv_max.data[:])
    print('Timestamps:',  hrv_max.timestamps[:]) 