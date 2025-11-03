
import numpy as np
from datetime import datetime, timezone
import pytz
from pynwb import NWBFile, NWBHDF5IO
from pynwb.file import ProcessingModule
from ndx_wearables import VO2MaxSeries, WearableDevice

def main():
    # 1) Create an NWBFile container (timezone-aware start time)
    nwbfile = NWBFile(
        session_description="Wearables VO2 Max example",
        identifier="VO2-001",
        session_start_time=datetime.now(timezone.utc),
    )

    # 2) Add a device and a wearables processing module
    wearable_dev = WearableDevice(
        name="wearable_device",
        manufacturer="ExampleCo",
        description="Example wearable",
        location="left_wrist",   # required by your spec
    )
    nwbfile.add_device(wearable_dev)
    wearables = nwbfile.create_processing_module(
        name="wearables",
        description="Wearables derived data",
    )

    # 3) Generate synthetic SpO2 data (every 30s for 1 hour)
    timestamps = np.arange(0.0, 3600.0, 30.0, dtype="float64")
    rng = np.random.default_rng(42)
    vo2max_values = rng.normal(loc=42.0, scale=6.0, size=timestamps.size).astype("float64")

    # 4) Create the series and add it to the processing module
    series = VO2MaxSeries(
        name="VO2 Max Data",
        data=vo2max_values,
        unit="mL/kg/min",
        timestamps=timestamps,
        description="Estimated VO2max over time",
        wearable_device=wearable_dev,     # REQUIRED link object
        algorithm="vo2max_estimator_v1",  # REQUIRED by your schema
    )
    wearables.add(series)

    # 5) Write to disk
    out_path = "examples/vo2max_example.nwb"
    with NWBHDF5IO(out_path, "w") as io:
        io.write(nwbfile)
    print(f"Wrote: {out_path}")

    # 6) Read back (roundtrip) and print summary
    with NWBHDF5IO(out_path, "r") as io:
        read_nwb = io.read()
        pm = read_nwb.processing["wearables"]
        s = pm.get("VO2 Max Data")
        print("Series:", s.name)
        print("Samples:", len(s.data[:]))
        print("First 5 values (mL/kg/min):", s.data[:5])
        print("Timestamps length:", len(s.timestamps[:]))

if __name__ == "__main__":
    main()