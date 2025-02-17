from pynwb import NWBFile, NWBHDF5IO

with NWBHDF5IO('vo2max_study.nwb', 'r') as io:
    nwbfile = io.read()
    vo2_max_data = nwbfile.processing['vo2max']
    vo2_max = vo2_max_data.get('Vo2 Max')
    print('Vo2 Max data:',  vo2_max.data[:])
    print('Timestamps:',  vo2_max.timestamps[:])