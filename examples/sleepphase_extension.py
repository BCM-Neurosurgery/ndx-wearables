import numpy as np
from itertools import cycle, islice
from datetime import datetime, timezone
from pynwb import NWBFile, NWBHDF5IO
from ndx_wearables import CategoricalSeries, WearableDevice, build_sleep_phase_meanings
from ndx_wearables.categorical_enums import ENUM_MAP

def main():
    # 1) File (tz-aware)
    nwb = NWBFile(
        session_description="Wearables SleepPhase example",
        identifier="SLEEP-001",
        session_start_time=datetime.now(timezone.utc),
    )

    # 2) WearableDevice
    wearable_dev = WearableDevice(
        name="wearable_device",
        manufacturer="ExampleCo",
        description="Example wearable",
        location="left_wrist",
    )
    nwb.add_device(wearable_dev)

    # 3) Processing module
    wearables = nwb.create_processing_module("wearables", "Wearables derived data")

    # 4) Canonical sleep phase labels from ENUM_MAP
    SleepEnum = ENUM_MAP["sleep_phase"]
    categories = [e.value for e in SleepEnum]
    timestamps = np.arange(0.0, 420.0, 60.0, dtype="float64")  # every 60s for 7 min
    labels = np.array(list(islice(cycle(categories), len(timestamps))))

    # 5) Meanings table
    meanings = build_sleep_phase_meanings()

    # 6) Build the series
    series = CategoricalSeries(
        name="sleep_phase",
        data=labels,
        unit="n/a",
        timestamps=timestamps,
        wearable_device=wearable_dev,
        algorithm="sleep_stager_v1",
        description="Sleep phase labels over time",
    )
    wearables.add(series)

    # 7) Attach or store meanings
    if hasattr(series, "meanings"):
        series.meanings = meanings
    else:
        wearables.add(meanings)

    # 8) Write/read roundtrip
    out_path = "examples/sleep_phase_example.nwb"
    with NWBHDF5IO(out_path, "w") as io:
        io.write(nwb)
    print("Wrote:", out_path)

    with NWBHDF5IO(out_path, "r") as io:
        read = io.read()
        s = read.processing["wearables"]["sleep_phase"]
        print("Series:", s.name)
        print("Has wearable_device link:", getattr(s, "wearable_device", None))
        print("First 5 labels:", s.data[:5])
        mt = getattr(s, "meanings", None) or read.processing["wearables"].data_interfaces.get("sleep_phase_meanings")
        print("Meanings table:", mt.name if mt else "None")

if __name__ == "__main__":
    main()
