from pynwb import NWBFile, NWBHDF5IO

with NWBHDF5IO('sample_data/sleep_study.nwb', 'r') as io:
    nwbfile = io.read()
    sleep_stage_data = nwbfile.processing['sleep']
    sleep_stages = sleep_stage_data.get('Sleep Stages')
    print('Sleep stage data:', sleep_stages.data[:])
    print('Timestamps:', sleep_stages.timestamps[:])
