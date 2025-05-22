from pynwb.spec import NWBGroupSpec, NWBDatasetSpec

def make_hrv_stage():
    hrv_series = NWBGroupSpec(
        doc='Stores HRV values as strings over time.',
        neurodata_type_def='HRVSeries',
        neurodata_type_inc='WearableTimeSeries',
    )

    return hrv_series 


