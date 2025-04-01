from pynwb import register_class, NWBContainer
from pynwb.core import MultiContainerInterface
from pynwb.spec import NWBGroupSpec, NWBDatasetSpec, NWBNamespaceBuilder, NWBAttributeSpec
from pynwb.base import TimeSeries

from hdmf.utils import docval, popargs, get_docval, get_data_shape

from datetime import datetime
from dateutil.tz import tzlocal
import numpy as np

# when extending NWBContainer, define __nwbfields__
# tells PyNWB properties of the NWBContainer extension
@register_class("WearableDevice", "ndx-wearables")
class WearableDevice(NWBContainer):
    '''
    - name
    - description
    - manufacturer
    - location (on body)
    '''
    __nwbfields__ = ("name", "description", "manufacturer", "location")

    @docval(
        {"name":"name", "type": str, "doc": "Name of wearable device"},
        {"name":"description", "type": str, "doc": "Description of wearable device"},
        {"name":"manufacturer", "type": str, "doc": "Wearable device manufacturer"},
        {"name":"location", "type": str, "doc": "Location of wearable device on body"},
    )

    def __init__(self, **kwargs):
        description = popargs("description", kwargs)
        manufacturer = popargs("manufacturer", kwargs)
        location = popargs("location", kwargs)

        super().__init__(**kwargs)

        self.description = description
        self.manufacturer = manufacturer
        self.location = location

@register_class("WearableSensor", "ndx-wearables")
class WearableSensor(NWBContainer):
    '''
    - name
    - description
    - device
    '''
    __nwbfields__ = ("name", "description", "device")

    @docval(
        {"name":"name", "type": str, "doc": "Name of sensor on wearable device"},
        {"name":"description", "type": str, "doc": "Description of sensor on wearable device"},
        {"name":"device", "type": WearableDevice, "doc": "Wearable device associated with sensor"},
    )

    def __init__(self, **kwargs):
        description = popargs("description", kwargs)
        device = popargs("device", kwargs)

        super().__init__(**kwargs)

        self.description = description
        self.device = device