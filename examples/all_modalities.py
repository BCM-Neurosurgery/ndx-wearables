from pynwb import NWBHDF5IO

from tests import make_wearables_nwbfile, add_wearables_device
from tests.test_wearables_infrastructure import add_wearable_events, add_wearable_timeseries
from tests.test_hrv_extension import add_hrv_data

# List of all modality specific build functions. Add your mode functions here to register them in the full demo NWB
# Each of these functions should take a pre-built NWB file, and add some synthetic data for the modality in question
MODALITY_BUILDERS = [
    add_wearable_events,
    add_wearable_timeseries,    # TODO: Remove generic types once more interesting test data is available
    add_hrv_data
]

OUTPUT_PATH = './all_wearable_modalities.nwb'


def main():
    ready_nwb, device = add_wearables_device(make_wearables_nwbfile())

    for mode_build in MODALITY_BUILDERS:
        ready_nwb = mode_build(ready_nwb, device)

    with NWBHDF5IO(OUTPUT_PATH, mode='w') as io:
        io.write(ready_nwb)


if __name__ == "__main__":
    main()