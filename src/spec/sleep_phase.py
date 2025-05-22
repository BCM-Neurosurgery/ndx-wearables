from pynwb import register_class
from hdmf.utils import docval, get_docval
from ndx_wearables.wearables_classes import WearableEvents

@register_class("SleepPhaseSeries", "ndx-wearables")
class SleepPhaseSeries(WearableEvents):
    @docval(*get_docval(WearableEvents.__init__))
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
