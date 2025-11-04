
import numpy as np
from datetime import datetime
import pytz
from pynwb import NWBFile, NWBHDF5IO
from pynwb.file import ProcessingModule
from ndx_wearables import WearableDevice, WearableTimeSeries

def main():
    # 1) Create the NWB container
    nwbfile = NWBFile(
        session_description="Wearables VO2 Max example",
        identifier="VO2-001",
        session_start_time=datetime.now()
    )

    # 2) Add a device and processing module
    device = WearableDevice(
        name="wearable_device",
        manufacturer="ExampleCo",
        description="Example wearable",
        location="wrist"
    )
    nwbfile.add_device(device)

    wearables = ProcessingModule(
        name="wearables",
        description="Wearables derived data"
    )
    nwbfile.add_processing_module(wearables)

    # 3) Generate synthetic VO2 max data (every 30s for 1 hour)
    timestamps = np.arange(0.0, 3600.0, 30.0)
    np.random.seed(42)
    vo2max_values = np.random.randint(30, 60, size=timestamps.size)  # mL/kg/min

    # 4) Create the VO2maxSeries and add to processing module
    series = WearableTimeSeries(
        name="VO2 Max Data",
        data=vo2max_values,
        unit="mL/kg/min",
        timestamps=timestamps,
        description="Example VO2 max data",
        wearable_device=device,
        algorithm="test_algorithm"
    )
    wearables.add(series)

    # 5) Write to disk
    out_path = "vo2max_example.nwb"
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
        print("First 5 VO2 max values (mL/kg/min):", s.data[:5])
        print("Timestamps length:", len(s.timestamps[:]))

if __name__ == "__main__":
    main()