
import numpy as np
from datetime import datetime, timezone
import pytz
from pynwb import NWBFile, NWBHDF5IO
from pynwb.file import ProcessingModule
from ndx_wearables import MetSeries, WearableDevice  # Assumes MetSeries is registered in the namespace and accessible via get_class

def main():
    # 1) Create the NWB container (timezone-aware start time)
    nwbfile = NWBFile(
        session_description="Wearables MET example",
        identifier="MET-001",
        session_start_time=datetime.now(timezone.utc),
    )

    # 2) Create your extension device (WearableDevice), then add it to the file
    wearable_dev = WearableDevice(
        name="wearable_device",
        manufacturer="ExampleCo",
        description="Example wearable",
        location="left_wrist",  # required by your spec
    )
    nwbfile.add_device(wearable_dev)

    # Processing module
    wearables = nwbfile.create_processing_module(
        name="wearables",
        description="Wearables derived data",
    )

    # 3) Generate synthetic MET data (every 30 s for 1 hour)
    timestamps = np.arange(0.0, 3600.0, 30.0, dtype="float64")
    rng = np.random.default_rng(42)
    met_values = rng.uniform(1.0, 10.0, size=timestamps.size).astype("float64")

    # 4) Create the series and add it to the processing module
    series = MetSeries(
        name="Met Data",
        data=met_values,
        unit="MET",
        timestamps=timestamps,
        description="Example metabolic equivalent values",
        wearable_device=wearable_dev,   # REQUIRED: link to WearableDevice
        algorithm="met_estimator_v1",   # REQUIRED by schema
    )
    wearables.add(series)

    # 5) Write to disk
    out_path = "examples/met_example.nwb"
    with NWBHDF5IO(out_path, "w") as io:
        io.write(nwbfile)
    print(f"Wrote: {out_path}")

    # 6) Read back (roundtrip) and print a summary
    with NWBHDF5IO(out_path, "r") as io:
        read_nwb = io.read()
        pm = read_nwb.processing["wearables"]
        s = pm.get("Met Data")
        print("Series:", s.name)
        print("Samples:", len(s.data[:]))
        print("First 5 values:", s.data[:5])
        print("Timestamps length:", len(s.timestamps[:]))

if __name__ == "__main__":
    main()
