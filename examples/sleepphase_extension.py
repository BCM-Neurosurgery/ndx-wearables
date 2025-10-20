import pytest
import numpy as np
from datetime import datetime
import pytz
from pynwb import NWBFile, NWBHDF5IO
from pynwb.file import ProcessingModule
from ndx_wearables import SleepPhaseSeries  # Assumes SleepPhaseSeries is registered in the namespace and accessible via get_class

def main():
    nwb = NWBFile("Wearables SleepPhase example", "SLEEP-001", datetime.now())

    device = Device(name="wearable_device", manufacturer="ExampleCo", description="Example wearable")
    nwb.add_device(device)

    wearables = ProcessingModule("wearables", "Wearables derived data")
    nwb.add_processing_module(wearables)

    labels = np.array(["awake", "n1", "n2", "n2", "n3", "rem", "awake"])
    timestamps = np.arange(labels.size, dtype=float)

    series = SleepPhaseSeries(
        name="sleep_phase",
        data=labels,              # labels map to codes internally
        timestamps=timestamps,
        unit="na",                # categorical
        description="Toy sleep stage labels over time",
        wearable_device=device,
        algorithm="sleep_stager_v1",
    )
    wearables.add_container(series)

    out_path = "examples/sleep_phase_example.nwb"
    with NWBHDF5IO(out_path, "w") as io:
        io.write(nwb)
    print("Wrote:", out_path)

    with NWBHDF5IO(out_path, "r") as io:
        read = io.read()
        ts = read.processing["wearables"].get("sleep_phase")
        print("Series:", ts.name)
        print("Samples:", len(ts.data[:]))
        print("First 5 labels (as stored):", ts.data[:5])  # may be codes depending on your base
        print("Categories:", getattr(ts, "categories", None))

if __name__ == "__main__":
    main()