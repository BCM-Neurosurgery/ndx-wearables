from pynwb import register_class, NWBContainer
from pynwb.core import MultiContainerInterface
from pynwb.device import Device
from pynwb.spec import NWBGroupSpec, NWBDatasetSpec, NWBNamespaceBuilder, NWBAttributeSpec
from pynwb.base import TimeSeries

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

    __nwbfields__ = ("sensor", "location")

    @docval(
        *get_docval(Device.__init__)
        + (
            #{"name":"sensor", "type": WearableSensor, "doc": "Sensor associated with wearable device"},
            {"name":"location", "type": str, "doc": "Location on body of device"},
            )
    )

    def __init__(self, **kwargs):
        #sensor = popargs("sensor", kwargs)
        location = popargs("location", kwargs)
        super().__init__(**kwargs)

        #self.sensor = sensor
        self.location = location

@register_class("WearableTimeSeries", "ndx-wearables")
class WearableTimeSeries(TimeSeries):

    @docval(
        *get_docval(TimeSeries.__init__)
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs) 
    
    __clsconf__ = {
        "attr": "devices",
        "type": WearableDevice,
        "add": "add_wearable_device",
        "get": "get_wearable_device",
        "create": "create_wearable_device",
    }