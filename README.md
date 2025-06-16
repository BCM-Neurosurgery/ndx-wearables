# ndx-wearables Extension for NWB

Store data from human wearables

## Installation

Create a new Python environment. Python 3.11 worked for me, while 3.13 ran into some installation issues.

```terminal
conda create -n <env_name> python=3.11
```

Navigate to the project root `cd path/to/ndx-wearables`, then install the required dependencies. For developers, use:

```terminal
pip install -r requirements-dev.txt
```

## Usage

Custom extensions are added to the extension spec YAML file by running:

```terminal
python src/spec/create_extension_spec.py
```

After running this script, you can verify that the extensions are correctly added to `spec/ndx-wearables.extensions.yaml`.

Running test code may be done with PyTest using the test files located in `src/pynwb/tests`.

To use custom extensions outside of a PyTest setting, they must be registered by navigating to the directory root and installing the package:
```terminal
cd path/to/ndx-wearables
pip install -e .
```

## Creating New Extensions (Developers)

To create a new extension, first define the extension in a new file located under `src/spec`. The new file should contain a function that returns a PyNWB NWBGroupSpec object containing the extension. Then, update `src/spec/create_extension_spec.py` to define your new data type and add it to the list of data types to be exported. Finally, update `pynwb/ndx_wearables/__init__.py` to register your class to make it accessible at the package level.

You may write a test file using PyTest under `src/pynwb/tests` to verify that the new extension can properly write and read data.

## Notes on Extension Usage

Several of the modality-specific extensions (e.g., `BloodOxygenSeries`, `HeartRateSeries`, etc.) now require additional arguments beyond the usual `name`, `data`, and `timestamps`.

In particular:
- `wearable_device` is required for classes that link to a device (e.g., `BloodOxygenSeries`, `VO2MaxSeries`)
- `algorithm` is required for many classes to indicate how the data was derived (e.g., `HRVSeries`, `StepCountSeries`)

If these arguments are omitted, instantiating the class will raise an error. You can find working examples in the test scripts under `src/pynwb/tests`.

## Arguments for ndx-wearables Classes

| Class Name           | Required Arguments                                                     | Optional Arguments                            |
|----------------------|------------------------------------------------------------------------|-----------------------------------------------|
| `BloodOxygenSeries`  | `name`, `data`, `timestamps`, `wearable_device`, `unit`, `algorithm`   | `resolution`, `conversion`, `comments`        |
| `HeartRateSeries`    | `name`, `data`, `timestamps`, `wearable_device`, `unit`, `algorithm`   | `resolution`, `conversion`, `comments`        |
| `HRVSeries`          | `name`, `data`, `timestamps`, `wearable_device`, `algorithm`, `sampling_rate` | `comments`, `description`, `resolution` |
| `SleepPhaseSeries`   | `name`, `data`, `timestamps`, `wearable_device`, `enums`, `algorithm`  | `resolution`, `conversion`, `comments`        |
| `StepCountSeries`    | `name`, `data`, `timestamps`, `wearable_device`, `algorithm`           | `resolution`, `conversion`, `comments`        |
| `VO2MaxSeries`       | `name`, `data`, `timestamps`, `wearable_device`, `unit`, `algorithm`   | `comments`, `resolution`, `conversion`        |
| `ActivitySeries`     | `name`, `data`, `timestamps`, `wearable_device`, `algorithm`           | `comments`, `resolution`, `conversion`        |
| `METSeries`          | `name`, `data`, `timestamps`, `wearable_device`, `unit`, `algorithm`   | `comments`, `resolution`, `conversion`        |
| `SleepMovementSeries`  | `name`, `data`, `timestamps`, `wearable_device`, `algorithm`           | `comments`, `resolution`, `conversion`        |



These reflect typical usage in constructors. For full context or updates, refer to the class definitions in [`src/pynwb/ndx_wearables`](src/pynwb/ndx_wearables) and usage examples in [`src/pynwb/tests`](src/pynwb/tests).



---
This extension was created using [ndx-template](https://github.com/nwb-extensions/ndx-template).
