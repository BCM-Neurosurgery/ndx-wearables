import numpy as np
from itertools import cycle, islice
from datetime import datetime, timezone
from pynwb import NWBFile, NWBHDF5IO
from ndx_wearables import CategoricalSeries, WearableDevice, build_activity_class_meanings
from ndx_wearables.categorical_enums import ENUM_MAP

def main():
    # 1) File (tz-aware)
    nwb = NWBFile(
        session_description="Wearables ActivityClass example",
        identifier="ACT-001",
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

    # 4) Canonical activity labels from ENUM_MAP
    ActEnum = ENUM_MAP["activity_class"]
    categories = [e.value for e in ActEnum]
    timestamps = np.arange(0.0, 3600.0, 30.0, dtype="float64")  # every 30s for 1h
    labels = np.array(list(islice(cycle(categories), len(timestamps))))

    # 5) Meanings table
    meanings = build_activity_class_meanings()

    # 6) Build the series
    series = CategoricalSeries(
        name="activity_class",
        data=labels,
        unit="n/a",
        timestamps=timestamps,
        wearable_device=wearable_dev,
        algorithm="activity_classifier_v1",
        description="Activity class labels over time",
    )
    wearables.add(series)

    # 7) Attach or store meanings
    if hasattr(series, "meanings"):
        series.meanings = meanings
    else:
        wearables.add(meanings)

    # 8) Write/read roundtrip
    out_path = "examples/activity_class_example.nwb"
    with NWBHDF5IO(out_path, "w") as io:
        io.write(nwb)
    print("Wrote:", out_path)

    with NWBHDF5IO(out_path, "r") as io:
        read = io.read()
        s = read.processing["wearables"]["activity_class"]
        print("Series:", s.name)
        print("Has wearable_device link:", getattr(s, "wearable_device", None))
        print("First 5 labels:", s.data[:5])
        mt = getattr(s, "meanings", None) or read.processing["wearables"].data_interfaces.get("activity_class_meanings")
        print("Meanings table:", mt.name if mt else "None")

if __name__ == "__main__":
    main()
