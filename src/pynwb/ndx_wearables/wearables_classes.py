from pynwb import register_class, get_class, NWBContainer
from pynwb.core import MultiContainerInterface
from hdmf.common import SimpleMultiContainer
from pynwb.device import Device
from pynwb.spec import NWBGroupSpec, NWBDatasetSpec, NWBNamespaceBuilder, NWBAttributeSpec
from pynwb.base import TimeSeries, NWBDataInterface
from ndx_events import EventsTable, CategoricalVectorData
from hdmf.utils import docval, popargs, get_docval, get_data_shape, getargs  # <-- added getargs
from datetime import datetime
from dateutil.tz import tzlocal
import numpy as np
from enum import Enum
from typing import Union
from .enums import Placement, SensorType
from hdmf.common import DynamicTable  # <-- already present

# Common enums (used across multiple classes)
class Placement(str, Enum):
    WRIST = "wrist"
    CHEST = "chest"
    ANKLE = "ankle"
    THIGH = "thigh"
    HEAD = "head"

class SensorType(str, Enum):
    ACCEL = "accel"  # accelerometer
    ECG = "ecg"      # electrocardiogram
    TEMP = "temp"    # temperature
    
class WearableBase(object):
    """
    HDMF and by extension NWB does not really support multiple inheritance.
    As a result, this class is "invisibly" inherited as a mixin

    For this to work properly, the inheriting class (at the time of writing, WearableTimeSeries and WearableEvents)
    must append the result of get_wearables_docval() to the docval of the init method, and call the function
    wearables_init_helper in the init method.
    """

    @staticmethod
    def get_wearables_docval():
        return (
            {
                'name': 'wearable_device',
                'type': 'WearableDevice',
                'doc': 'Link to the WearableDevice used to record the data'
            },
            {
                'name': 'algorithm',
                'type': str,
                'doc': 'Algorithm used to extract data from raw sensor readings'
            }
        )

    def wearables_init_helper(self, **kwargs):
        wearable_device = popargs('wearable_device', kwargs)
        algorithm = popargs('algorithm', kwargs)

        self.wearable_device = wearable_device
        self.algorithm = algorithm
        return kwargs

# Categorical TimeSeries container (what Tomek expected)

@register_class('WearablesEnumTimeseriesBase', 'ndx-wearables')
class WearablesEnumTimeseriesBase(TimeSeries, WearableBase):
    """
    A categorical TimeSeries for wearable data.
    Stores category values (strings or integer indices), the allowed categories,
    and an optional meanings table with human-readable descriptions.
    """
    # ensure round-trip of these fields
    __nwbfields__ = tuple(list(getattr(TimeSeries, "__nwbfields__", ())) + ["categories", "meanings"])

    @docval(
        {'name': 'name', 'type': str, 'doc': 'name of the series'},
        {'name': 'data', 'type': ('array_data',), 'doc': 'categorical values as strings or int indices'},
        {'name': 'categories', 'type': ('array_data',), 'doc': 'list of allowed string labels'},
        {'name': 'rate', 'type': (float, type(None)), 'doc': 'sampling rate', 'default': None},
        {'name': 'timestamps', 'type': ('array_data', type(None)), 'doc': 'timestamps', 'default': None},
        {'name': 'meanings', 'type': (DynamicTable, type(None)), 'doc': 'optional category->description table', 'default': None},
        # If you want WearableBase metadata, uncomment the next line and the helper call below:
        # *WearableBase.get_wearables_docval(),
    )
    def __init__(self, **kwargs):
        name, data, categories, rate, timestamps, meanings = getargs(
            'name', 'data', 'categories', 'rate', 'timestamps', 'meanings', kwargs
        )

        # If you enabled WearableBase docval above, also call:
        # kwargs = self.wearables_init_helper(**kwargs)

        arr = np.asanyarray(list(data) if not hasattr(data, "__array__") else data)
        categories = [str(c) for c in categories]

        # Validate membership
        if arr.size:
            if arr.dtype.kind in {'U', 'S', 'O'}:
                bad = sorted(set(arr.tolist()) - set(categories))
                if bad:
                    raise ValueError(f"values not in categories: {bad}")
            else:
                # integer indices
                if arr.min() < 0 or arr.max() >= len(categories):
                    raise ValueError("index values out of range for categories")

        # categorical → use a non-physical unit
        super().__init__(name=name, data=data, rate=rate, timestamps=timestamps, unit='na')

        # Attach categories for downstream access and serialization
        self.categories = categories

        # Meanings table (category → description)
        if meanings is None:
            meanings = DynamicTable(
                name=f"{name}_meanings",
                description="Category definitions for this series"
            )
            meanings.add_column(name='category', description='category label', data=categories)
            meanings.add_column(name='description', description='human-readable definition',
                                data=[''] * len(categories))
        self.meanings = meanings
        
# Concrete constrained subclass examples 
class SleepPhase(str, Enum):
    AWAKE = "awake"
    N1 = "n1"
    N2 = "n2"
    N3 = "n3"
    REM = "rem"

class SleepPhaseSeries(WearablesEnumTimeseriesBase):
    def __init__(self, name='sleep_phase', data=(), rate=None, timestamps=None, meanings=None, **kwargs):
        categories = [e.value for e in SleepPhase]
        super().__init__(name=name,
                         data=list(data),
                         categories=categories,
                         rate=rate,
                         timestamps=timestamps,
                         meanings=meanings,
                         **kwargs)
        
class ActivityClass(str, Enum):
    SITTING = "sitting"
    WALKING = "walking"
    RUNNING = "running"

class ActivityClassSeries(WearablesEnumTimeseriesBase):
    def __init__(self, name='activity_class', data=(), rate=None, timestamps=None, meanings=None, **kwargs):
        categories = [e.value for e in ActivityClass]
        super().__init__(name=name,
                         data=list(data),
                         categories=categories,
                         rate=rate,
                         timestamps=timestamps,
                         meanings=meanings,
                         **kwargs)

# Device and existing classes (unchanged except for Placement handling)

@register_class("WearableDevice", "ndx-wearables")
class WearableDevice(Device):
    '''
    - name
    - description
    - manufacturer
    - location (on body)
    '''
    __nwbfields__ = ("location",)

    @docval(
        *get_docval(Device.__init__)
        + (
            {"name":"location", "type": str, "doc": "Location on body of device"},
            {"name":"os_software_version", "type": str,
             "doc":"The version number of the OS/software for the WearableDevice", "default": None}
        )
    )
    def __init__(self, **kwargs):
        location = popargs("location", kwargs)
        os_software_version = popargs("os_software_version", kwargs)
        super().__init__(**kwargs)

        # Normalize/validate against Placement enum (since Placement.validate() no longer exists)
        if isinstance(location, Placement):
            self.location = location.value
        else:
            norm = location.strip().lower()
            # simple synonyms (optional)
            synonyms = {"forearm": "wrist", "hand": "wrist", "arm": "wrist"}
            norm = synonyms.get(norm, norm)
            self.location = Placement(norm).value  # raises ValueError if invalid

        self.os_software_version = os_software_version

@register_class("WearableTimeSeries", "ndx-wearables")
class WearableTimeSeries(WearableBase, TimeSeries):
    @docval(
        *(get_docval(TimeSeries.__init__) + WearableBase.get_wearables_docval())
    )
    def __init__(self, **kwargs):
        kwargs = self.wearables_init_helper(**kwargs)
        super().__init__(**kwargs)

PhysiologicalMeasure = get_class("PhysiologicalMeasure", "ndx-wearables")

@register_class("WearableEvents", "ndx-wearables")
class WearableEvents(WearableBase, EventsTable):
    @docval(
        *(get_docval(EventsTable.__init__) + WearableBase.get_wearables_docval())
    )
    def __init__(self, **kwargs):
        kwargs = self.wearables_init_helper(**kwargs)
        super().__init__(**kwargs)
