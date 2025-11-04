from pynwb import register_class, get_class
from pynwb.device import Device
from pynwb.base import TimeSeries
from ndx_events import EventsTable
from hdmf.utils import docval, popargs, get_docval, getargs  
import numpy as np
from enum import Enum
from hdmf.common import DynamicTable  
from ndx_wearables.categorical_enums import ENUM_MAP

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
        wearable_device = kwargs.pop('wearable_device', None)
        algorithm = kwargs.pop('algorithm', None)
        self.wearable_device = wearable_device
        self.algorithm = algorithm
        return kwargs

# Categorical TimeSeries container (what Tomek expected)

@register_class('WearableEnumSeries', 'ndx-wearables')
class WearableEnumSeries(TimeSeries, WearableBase):
    # make sure these round-trip
    __nwbfields__ = tuple(list(getattr(TimeSeries, "__nwbfields__", ())) +
                          ["categories", "meanings", "wearable_device", "algorithm"])

    @docval(
        {'name': 'name', 'type': str, 'doc': 'name of the series'},
        {'name': 'data', 'type': ('array_data',), 'doc': 'categorical values as strings or int indices'},
        {'name': 'categories', 'type': (('array_data',), type(None)), 'doc': 'list of allowed string labels', 'default': None},
        {'name': 'rate', 'type': (float, type(None)), 'doc': 'sampling rate', 'default': None},
        {'name': 'timestamps', 'type': ('array_data', type(None)), 'doc': 'timestamps', 'default': None},
        {'name': 'meanings', 'type': (DynamicTable, type(None)), 'doc': 'optional category->description table', 'default': None},
        {'name': 'description', 'type': (str, type(None)), 'doc': 'description of the series', 'default': None},
        # wearables metadata (may be None in some files)
        {'name': 'wearable_device', 'type': ('WearableDevice', type(None)), 'doc': 'Device used to record the data', 'default': None},
        {'name': 'algorithm', 'type': (str, type(None)), 'doc': 'Algorithm used to extract data', 'default': None},
    )
    def __init__(self, **kwargs):
        name, data, categories, rate, timestamps, meanings, description = getargs(
            'name', 'data', 'categories', 'rate', 'timestamps', 'meanings', 'description', kwargs
        )
        # pull wearables args off kwargs (don’t assign yet)
        wearable_device = popargs('wearable_device', kwargs)
        algorithm = popargs('algorithm', kwargs)

        arr = np.asanyarray(list(data) if not hasattr(data, "__array__") else data)
        if categories is not None:
            categories = [str(c) for c in categories]

        if arr.size and categories is not None:
            if arr.dtype.kind in {'U','S','O'}:
                bad = sorted(set(arr.tolist()) - set(categories))
                if bad:
                    raise ValueError(f"values not in categories: {bad}")
            else:
                if arr.min() < 0 or arr.max() >= len(categories):
                    raise ValueError("index values out of range for categories")
        super().__init__(name=name,
                         data=data,
                         rate=rate,
                         timestamps=timestamps,
                         unit='na',
                         description=(description or ""))

        # now it is safe to set custom fields
        self.wearable_device = wearable_device
        self.algorithm = algorithm

        # categories
        self.categories = categories

        # meanings table (robust creation: add columns then rows)
        if meanings is None:
            meanings = DynamicTable(
                name=f"{name}_meanings",
                description="Category definitions for this series"
            )
            meanings.add_column(name='category', description='category label')
            meanings.add_column(name='meaning', description='human-readable definition')
            if categories is not None:
                for cat in categories:
                    meanings.add_row(category=cat, meaning='')
        self.meanings = meanings


class CategoricalSeries(WearableEnumSeries):
    def __init__(self, category_type, data=(), rate=None, timestamps=None, meanings=None, description=None, **kwargs):
        enum_class = ENUM_MAP[category_type]
        categories = [e.value for e in enum_class]
        super().__init__(
            name=category_type,
            data=list(data),
            categories=categories,
            rate=rate,
            timestamps=timestamps,
            meanings=meanings,
            description=description or f"{category_type} categorical series",
            **kwargs
        )

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
