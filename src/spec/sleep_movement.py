from pynwb import register_class
from hdmf.utils import docval, get_docval
from ndx_wearables.wearables_classes import WearableTimeSeries

@register_class("SleepMovementSeries", "ndx-wearables")
class SleepMovementSeries(WearableTimeSeries):
    @docval(*get_docval(WearableTimeSeries.__init__))
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
