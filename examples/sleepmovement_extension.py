import numpy as np
from datetime import datetime, timezone
import pytz
from pynwb import NWBFile, NWBHDF5IO
from pynwb.file import ProcessingModule
from ndx_wearables import SleepMovementSeries, WearableDevice 

def main():
    # 1) Create an NWBFile container (timezone-aware start time)
    nwbfile = NWBFile(
        session_description="Wearables SleepMovement example",
        identifier="SLPMOVE-001",
        session_start_time=datetime.now(timezone.utc),
    )

    # 2) Add a device and a wearables processing module
    wearable_dev = WearableDevice(
        name="wearable_device",
        manufacturer="ExampleCo",
        description="Example wearable",
        location="left_wrist",  # required by spec
    )
    nwbfile.add_device(wearable_dev)
    wearables = nwbfile.create_processing_module(
        name="wearables",
        description="Wearables derived data",
    )

    # 3) Generate synthetic SpO2 data (every 30s for 1 hour)
    timestamps = np.arange(0.0, 3600.0, 30.0, dtype="float64")
    rng = np.random.default_rng(42)
    # small movement magnitudes in arbitrary units
    movement = rng.normal(loc=0.3, scale=0.15, size=timestamps.size)
    movement = np.clip(movement, 0.0, None).astype("float64")  # float64 per spec

    # 4) Create the series and add it to the processing module
    series = SleepMovementSeries(
        name="SleepMovement Data",
        data=movement,
        unit="a.u.",  # arbitrary units
        timestamps=timestamps,
        description="Actigraphy-like movement magnitude during sleep",
        wearable_device=wearable_dev,     # REQUIRED
        algorithm="actigraphy_peaks_v1",  # REQUIRED
    )
    wearables.add(series)

    # 5) Write to disk
    out_path = "examples/sleepmovement_example.nwb"
    with NWBHDF5IO(out_path, "w") as io:
        io.write(nwbfile)
    print(f"Wrote: {out_path}")

    # 6) Read back (roundtrip) and print summary
    with NWBHDF5IO(out_path, "r") as io:
        read_nwb = io.read()
        pm = read_nwb.processing["wearables"]
        s = pm.get("SleepMovement Data")
        print("Series:", s.name)
        print("Samples:", len(s.data[:]))
        print("First 5 values:", s.data[:5])
        print("Timestamps length:", len(s.timestamps[:]))

if __name__ == "__main__":
    main()