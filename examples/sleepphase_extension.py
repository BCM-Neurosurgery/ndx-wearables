# examples/sleep_phase_extension.py
import numpy as np
from datetime import datetime, timezone
from pynwb import NWBFile, NWBHDF5IO
from ndx_wearables import (
    CategoricalSeries,       # wrapper over WearableEnumSeries using ENUM_MAP
    WearableDevice,
    build_sleep_phase_meanings,
)

def main():
    nwb = NWBFile(
        session_description="Wearables SleepPhase example",
        identifier="SLEEP-001",
        session_start_time=datetime.now(timezone.utc),
    )

    wearable_dev = WearableDevice(
        name="wearable_device",
        manufacturer="ExampleCo",
        description="Example wearable",
        location="left_wrist",
    )
    nwb.add_device(wearable_dev)

    wearables = nwb.create_processing_module("wearables", "Wearables derived data")

    # toy labels over 7 seconds
    labels = np.array(["awake", "n1", "n2", "n2", "n3", "rem", "awake"])
    timestamps = np.arange(labels.size, dtype="float64")

    meanings = build_sleep_phase_meanings()

    series = CategoricalSeries(
        category_type="sleep_phase",     # resolves SleepPhase enum via ENUM_MAP
        data=labels,                     # strings or int codes are both accepted
        timestamps=timestamps,
        meanings=meanings,               # DynamicTable with category meanings
        wearable_device=wearable_dev,    # now accepted because we enabled WearableBase docval
        algorithm="sleep_stager_v1",
    )
    wearables.add(series)

    out_path = "examples/sleep_phase_example.nwb"
    with NWBHDF5IO(out_path, "w") as io:
        io.write(nwb)
    print("Wrote:", out_path)

    # roundtrip and quick check
    with NWBHDF5IO(out_path, "r") as io:
        read = io.read()
        ts = read.processing["wearables"].get("sleep_phase")
        print("Series:", ts.name)
        print("Categories:", getattr(ts, "categories", None))
        print("First 5 stored:", ts.data[:5])
        # decode if strings were converted to codes
        cats = list(ts.categories) if getattr(ts, "categories", None) else []
        if cats and ts.data.dtype.kind in {"i", "u"}:
            print("First 5 labels:", [cats[int(x)] for x in ts.data[:5]])
        # meanings table
        mt = getattr(ts, "meanings", None)
        if mt:
            print("Meanings table name:", mt.name)
            print("Meaning rows:", len(mt))

if __name__ == "__main__":
    main()
