from pynwb import register_class, NWBContainer
from pynwb.core import MultiContainerInterface
from pynwb.device import Device
from pynwb.spec import NWBGroupSpec, NWBDatasetSpec, NWBNamespaceBuilder, NWBAttributeSpec
from pynwb.base import TimeSeries
from ndx_events import EventsTable, CategoricalVectorData


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
        )

    def wearables_init_helper(self, **kwargs):
        print('In WearableBase init')
        wearable_device = popargs('wearable_device', kwargs)
        self.wearable_device = wearable_device
        return kwargs


# # Adding events to inherit from ndx-wearables:
# # WearableEvents inherits from EventsTable (from rly/ndx-events) to store timestamped discrete events from wearables
# @register_class("WearableEvents", "ndx-wearables")
# class WearableEvents(WearableBase, CategoricalVectorData):
#
#     @docval(
#         *(
#                 get_docval(CategoricalVectorData.__init__) + get_docval(WearableBase.__init__)
#         )
#     )
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)

@register_class("WearableTimeSeries", "ndx-wearables")
class WearableTimeSeries(WearableBase, TimeSeries):

    @docval(*(get_docval(TimeSeries.__init__) + WearableBase.get_wearables_docval()))
    def __init__(self, **kwargs):
        print('In WearableTimeSeries init')
        kwargs = self.wearables_init_helper(**kwargs)
        super().__init__(**kwargs)
