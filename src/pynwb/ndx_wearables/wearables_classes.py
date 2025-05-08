from pynwb import register_class, NWBContainer
from pynwb.core import MultiContainerInterface
from pynwb.device import Device
from pynwb.spec import NWBGroupSpec, NWBDatasetSpec, NWBNamespaceBuilder, NWBAttributeSpec
from pynwb.base import TimeSeries
from ndx_events_record import EventsRecord


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

class WearableBase(NWBContainer):
    @docval([
            {'name': 'wearable_device', 'type': 'WearableDevice', 'doc': 'Link to the WearableDevice used to record the data'}
        ])

    def __init__(self, **kwargs):
        wearable_device = popargs('wearable_device', kwargs)
        super().__init__(**kwargs)
        self.wearable_device = wearable_device


# Adding events to inherit from ndx-wearables:
# WearableEvents inherits from EventsRecord (from ndx-events-record) to store timestamped discrete events from wearables
@register_class("WearableEvents", "ndx-wearables")
class WearableEvents(WearableBase, EventsRecord):
    __nwbfields__ = ("sensor")

    @docval(
        * (get_docval(EventsRecord.__init__) + get_docval(WearableBase.__init__)),
        {"name": "sensor", "type": 'WearableSensor', "doc": "Sensor associated with the event"},
        # Include other required fields like timestamps/description if needed
    )
    def __init__(self, **kwargs):
        sensor = popargs("sensor", kwargs)
        super().__init__(**kwargs)
        self.sensor = sensor

@register_class("WearableTimeSeries", "ndx-wearables")
class WearableTimeSeries(WearableBase, TimeSeries):
    @docval(* (get_docval(TimeSeries.__init__) + get_docval(WearableBase.__init__)))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
