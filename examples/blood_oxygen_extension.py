import numpy as np
from datetime import datetime, timezone
from pynwb import NWBFile, NWBHDF5IO
from ndx_wearables import BloodOxygenSeries, WearableDevice 

def main():
    # 1) Create an NWBFile container (timezone-aware start time)
    nwbfile = NWBFile(
        session_description="Wearables BloodOxygen example",
        identifier="SPO2-001",
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


    # 4) Create the series and add it to the processing module
    series = BloodOxygenSeries(
        name="BloodOxygen Data",
        data=values,
        unit="percent",
        timestamps=timestamps,
        description="Example blood oxygen data",
        wearable_device=wearable_dev,
        algorithm="pulse_oximeter",
    )
    wearables.add(series)

    # 5) Write to disk
    out_path = "examples/blood_oxygen_example.nwb"
    with NWBHDF5IO(out_path, "w") as io:
        io.write(nwbfile)
    print(f"Wrote: {out_path}")

    # 6) Read back (roundtrip) and print summary
    with NWBHDF5IO(out_path, "r") as io:
        read_nwb = io.read()
        pm = read_nwb.processing["wearables"]
        s = pm.get("BloodOxygen Data")
        print("Series:", s.name)
        print("Samples:", len(s.data[:]))
        print("First 5 values:", s.data[:5])
        print("Timestamps length:", len(s.timestamps[:]))

if __name__ == "__main__":
    main()
