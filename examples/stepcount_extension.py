
import numpy as np
from datetime import datetime, timezone
import pytz
from pynwb import NWBFile, NWBHDF5IO
from pynwb.file import ProcessingModule
from ndx_wearables import StepCountSeries, WearableDevice  # Assumes StepCountSeries is registered in the namespace and accessible via get_class

def main():
    # 1) Create NWB container
    nwbfile = NWBFile(
        session_description="Wearables StepCount example",
        identifier="STEP-001",
        session_start_time=datetime.now(timezone.utc),
    )

    # 2) Add a device and a wearables processing module
    wearable_dev = WearableDevice(
        name="wearable_device",
        manufacturer="ExampleCo",
        description="Example wearable",
        location="left_wrist",
    )
    nwbfile.add_device(wearable_dev)
    wearables = nwbfile.create_processing_module("wearables", "Wearables derived data")

    # 3) Generate synthetic SpO2 data (every 30s for 1 hour)
    timestamps = np.arange(0.0, 3600.0, 30.0, dtype="float64")
    rng = np.random.default_rng(42)
    values = rng.integers(90, 100, size=timestamps.size).astype("float64")

    # 4) Create series and add to processing module
    series = StepCountSeries(
        name="StepCount Data",
        data=values,
        unit="steps",
        timestamps=timestamps,
        description="Example step count values",
        wearable_device=wearable_dev,
        algorithm="test_algorithm",
    )
    wearables.add(series)

    # 5) Write to disk
    out_path = "examples/stepcount_example.nwb"
    with NWBHDF5IO(out_path, "w") as io:
        io.write(nwbfile)
    print(f"Wrote: {out_path}")

    # 6) Read back (roundtrip) and summarize
    with NWBHDF5IO(out_path, "r") as io:
        read_nwb = io.read()
        pm = read_nwb.processing["wearables"]
        s = pm.get("StepCount Data")
        print("Series:", s.name)
        print("Samples:", len(s.data[:]))
        print("First 5 step counts:", s.data[:5])
        print("Timestamps length:", len(s.timestamps[:]))

if __name__ == "__main__":
    main()