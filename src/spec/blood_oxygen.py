from pynwb.spec import NWBGroupSpec, NWBDatasetSpec

def make_blood_oxygen():
    blood_oxygen_series = NWBGroupSpec(
        doc='Stores blood oxygen over time.',
        quantity='*',
        # datasets=[
        #     NWBDatasetSpec(
        #         name='data',
        #         dtype='float',
        #         quantity='*',
        #         doc='How much oxygen blood is carrying as a percentage of the maximum it could carry'
        #     )
        # ],
        neurodata_type_def='DeviceBloodOxygen',
        neurodata_type_inc='TimeSeries', # WearablesSeries
    )

    breathing_disturbance_series = NWBGroupSpec(
        doc='Stores breathing disturbance index (BDI) over time',
        quantity='*',
        # datasets=[
        #     NWBDatasetSpec(
        #         name='data',
        #         dtype='int',
        #         quantity='*',
        #         doc='Quantification of the severity of sleep-disordered breathing'
        #     )
        # ],
        neurodata_type_def='DeviceBreathingDisturbance',
        neurodata_type_inc='TimeSeries', # WearablesSeries
    )

    blood_oxygen = NWBGroupSpec(
        neurodata_type_def="BloodOxygenGroup",
        neurodata_type_inc="NWBDataInterface",
        name="blood_oxygen",
        doc="A collection of blood oxygen time series from one or more devices.",
        quantity="?",
        groups=[blood_oxygen_series, breathing_disturbance_series],
    )
    
    return blood_oxygen#, blood_oxygen_series, breathing_disturbance_series
