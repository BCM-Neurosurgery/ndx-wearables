from pynwb import register_class, NWBContainer
from pynwb.core import MultiContainerInterface
from pynwb.device import Device
from pynwb.spec import NWBGroupSpec, NWBDatasetSpec, NWBNamespaceBuilder, NWBAttributeSpec
from pynwb.base import TimeSeries, Events

from hdmf.utils import docval, popargs, get_docval, get_data_shape

from datetime import datetime
from dateutil.tz import tzlocal
import numpy as np

# when extending NWBContainer, define __nwbfields__
# tells PyNWB properties of the NWBContainer extension
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
            )
    )


    def __init__(self, **kwargs):
        location = popargs("location", kwargs)
        super().__init__(**kwargs)

        self.location = location

# Adding events:
@register_class("WearableEvents", "ndx-wearables")
class WearableEvents(Events):
    __nwbfields__ = ("name", "sensor")

    @docval(
        {"name": "name", "type": str, "doc": "Name of the event"},
        {"name": "sensor", "type": 'WearableSensor', "doc": "Sensor associated with the event"},
        # Include other required fields like timestamps/description if needed
    )
    def __init__(self, **kwargs):
        sensor = popargs("sensor", kwargs)
        super().__init__(**kwargs)
        self.sensor = sensor