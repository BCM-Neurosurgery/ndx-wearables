# examples/activityclass_extension.py
import numpy as np
from datetime import datetime, timezone
from pynwb import NWBFile, NWBHDF5IO
from ndx_wearables import (
    CategoricalSeries, WearableDevice, build_activity_class_meanings
)

def main():
    nwb = NWBFile("Wearables ActivityClass example", "ACT-001", datetime.now(timezone.utc))

    wearable_dev = WearableDevice(
        name="wearable_device",
        manufacturer="ExampleCo",
        description="Example wearable",
        location="left_wrist",
    )
    nwb.add_device(wearable_dev)
    wearables = nwb.create_processing_module("wearables", "Wearables derived data")

    timestamps = np.arange(0.0, 3600.0, 30.0, dtype="float64")
    labels = np.array(["sitting", "walking", "running"])
    data = np.tile(labels, int(np.ceil(timestamps.size / labels.size)))[:timestamps.size]

    meanings = build_activity_class_meanings()

    series = CategoricalSeries(
        category_type="activity_class",     # becomes the series name
        data=data,
        timestamps=timestamps,
        meanings=meanings,
        wearable_device=wearable_dev,       # REQUIRED
        algorithm="activity_classifier_v1", # REQUIRED
        # no name=..., no description=...
    )
    wearables.add(series)

    out_path = "examples/activity_class_example.nwb"
    with NWBHDF5IO(out_path, "w") as io:
        io.write(nwb)
    print("Wrote:", out_path)

    with NWBHDF5IO(out_path, "r") as io:
        read = io.read()
        s = read.processing["wearables"].get("activity_class")  # use the auto name
        print("Series:", s.name)
        print("Samples:", len(s.data[:]))
        print("First 5 labels:", s.data[:5])
        print("Categories:", getattr(s, "categories", None))

if __name__ == "__main__":
    main()
