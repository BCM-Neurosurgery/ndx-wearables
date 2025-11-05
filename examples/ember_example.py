
import numpy as np
from datetime import datetime
import pytz
from pynwb import NWBFile, NWBHDF5IO
import pandas as pd
from pynwb.file import ProcessingModule
from hdmf.common.table import VectorData
from ndx_events import DurationVectorData
from ndx_wearables import WearableDevice, WearableTimeSeries, WearableEnumSeries, WearableEvents, PhysiologicalMeasure
from ndx_wearables.categorical_enums import build_sleep_phase_meanings


def main():
    nwb = NWBFile("NDX Wearables Example", "pre-release-0-2_2025-11", datetime.now())

    #Two example devicdes
    deviceRing = WearableDevice(
        name="ExampleRing",
        manufacturer="Examplon LLC",
        description="Example device to demonstrate how data is stored by NDX-Wearables",
        location='Right ring finger'
    )
    nwb.add_device(deviceRing)
    deviceWatch = WearableDevice(
        name="ExampleWatch",
        manufacturer="Test Industries Inc",
        description="Example device to demonstrate how data is stored by NDX-Wearables",
        location='Left wrist'
    )
    nwb.add_device(deviceWatch)

    #Example Sleep Data for Wearables Enum
    wearables = ProcessingModule(name="wearables", description="Wearables derived data")
    nwb.add_processing_module(wearables)

    meanings = build_sleep_phase_meanings()
    wearables.add(meanings)

    labels = np.array(["awake", "n1", "n2", "n2", "n3", "rem", "awake"])
    timestamps = np.arange(labels.size, dtype=float)

    series = WearableEnumSeries(
        name="sleep_phase",
        data=labels,              # labels map to codes internally
        timestamps=timestamps,
        description=f"Toy sleep stage labels over time from {deviceWatch.name}",
        wearable_device=deviceWatch,
        algorithm="sleep_stager_v1",
        meanings=meanings,
    )
    wearables.add(series)

    # Example Heart Rate Wearables Time Series- Generate synthetic heart-rate data (every 5s for 1h)
    timestamps = np.arange(0.0, 3600.0, 5.0)   # 720 samples
    np.random.seed(42)
    heart_rate_values = np.random.uniform(low=60, high=100, size=timestamps.size)

    #Create series and add to module
    series = WearableTimeSeries(
        name="Heart Rate Data",
        data=heart_rate_values,
        unit="bpm",
        timestamps=timestamps,
        description=f"Example Heart Rate data from {deviceRing.name}",
        wearable_device=deviceRing,
        algorithm="simulated data"
    )
    wearables.add(series)

    # Example Sleep Interval Wearables Events - Create the SleepEpochs table, including custom columns and add to the processing module
    fake_sleep_intervals = pd.DataFrame.from_dict({
        'start_times': [13.0, 20.0, 44.0, 52.0],      # Entered here in hours, needs to be converted to seconds
        'durations': [1.2, 8.0, 7.3, 2.1],    # Entered here in hours, needs to be converted to seconds
        'classified_types': ['nap', 'long_rest', 'long_rest', 'nap'],
        'time_in_bed': [1.2, 8.5, 9.2, 2.4]   # Entered here in hours, needs to be converted to seconds
    })
    duration = DurationVectorData(
        name="duration",
        description="The duration, in seconds, of the sleep epoch"
    )
    sleep_type = VectorData(
        name='sleep_type',
        description='Type of sleep this was categorized as',
    )
    time_in_bed = VectorData(
        name='time_in_bed',
        description='Total time (in seconds) in bed (more than just sleeping)',
    )
    sleep_epochs = WearableEvents(
        name='SleepEpochs',
        description=f"Sleep epochs collected from {deviceWatch.name}",
        wearable_device=deviceWatch,
        columns=[duration, sleep_type, time_in_bed],
        algorithm='proprietary algorithm',
    )
    for row_data in fake_sleep_intervals.itertuples():
        sleep_epochs.add_row(
            timestamp=row_data.start_times*3600,     # converting to seconds since start of file,
            duration=row_data.durations*3600,         # Converting hours to seconds
            sleep_type=row_data.classified_types,
            time_in_bed=row_data.time_in_bed*3600,
        )

    wearables.add(sleep_epochs)

    # Example Physiological Measures
    timestamps = np.arange(0.0, 3600.0, 30.0)
    np.random.seed(0)
    wearable_values = np.random.random(size=(120, 2))

    modality = PhysiologicalMeasure(
        name="TestMeasure",
    )

    # Build out a meanings table to use in the events file
    ts = WearableTimeSeries(
        name=f"{deviceWatch.name}_TestTimeseries",
        data=wearable_values,
        timestamps=timestamps,
        description="test",
        unit="unit",
        wearable_device=deviceWatch,
        algorithm='placeholder'
    )

    wearables.add([modality])

    added_ts = modality.add_wearable_time_series(ts)

    # generate fake wearables data
    timestamps = np.arange(0.0, 3600.0, 30.0)
    np.random.seed(0)
    wearable_values = np.random.random(size=(120, 2))

    # Build out a meanings table to use in the events file
    ts2 = WearableTimeSeries(
        name=f"{deviceRing.name}_TestTimeseries",
        data=wearable_values,
        timestamps=timestamps,
        description="test2",
        unit="unit",
        wearable_device=deviceRing,
        algorithm='placeholder'
    )

    added_ts2 = modality.add_wearable_time_series(ts2)

    out_path = "pre-release-0-2_2025-11.nwb"
    with NWBHDF5IO(out_path, "w") as io:
        io.write(nwb)
    print("Wrote:", out_path)

if __name__ == "__main__":
    main()