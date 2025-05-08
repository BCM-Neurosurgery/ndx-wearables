from pynwb import register_class, NWBContainer
from pynwb.core import MultiContainerInterface
from pynwb.device import Device
from pynwb.spec import NWBGroupSpec, NWBDatasetSpec, NWBNamespaceBuilder, NWBAttributeSpec
from pynwb.base import TimeSeries
from ndx_events import EventsTable


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
# WearableEvents inherits from EventsTable (from rly/ndx-events) to store timestamped discrete events from wearables
@register_class("WearableEvents", "ndx-wearables")
class WearableEvents(WearableBase, EventsTable):

    @docval(
        * (get_docval(EventsTable.__init__) + get_docval(WearableBase.__init__)),
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
