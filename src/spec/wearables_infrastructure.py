from pynwb import register_class, NWBContainer
from pynwb.core import MultiContainerInterface
from pynwb.spec import NWBGroupSpec, NWBDatasetSpec, NWBNamespaceBuilder, NWBAttributeSpec, RefSpec, LinkSpec
from pynwb.base import TimeSeries

from hdmf.utils import docval, popargs, get_docval, get_data_shape

from datetime import datetime
from dateutil.tz import tzlocal
import numpy as np


def make_wearables_infrastructure():
    
    wearable_device = NWBGroupSpec(
        neurodata_type_def="WearableDevice",
        neurodata_type_inc="Device",
        doc="Wearable device from which data was recorded",
        quantity="*",
        attributes=[
            NWBAttributeSpec(
                name="location", doc="Location of wearable device on body", dtype="text", required=True
            )
        ],
    )
    
    wearable_timeseries = NWBGroupSpec(
        neurodata_type_def="WearableTimeSeries",
        neurodata_type_inc="TimeSeries",
        doc="Data recorded from wearable sensor/device",
        datasets=[
            NWBDatasetSpec(
                name="data",
                dtype="float64",
                doc="Data which was collected from sensor",
            )
        ],
        links=[
            LinkSpec(
                name= 'wearable_device',
                target_type='WearableDevice',
                doc= 'Link to WearableDevice used to record WearableTimeSeries'
            )
        ]
    )

    wearable_events = NWBGroupSpec(
        neurodata_type_def="WearableEvents",
        neurodata_type_inc="Events",
        doc="Interval-style data (e.g., workouts) from wearable sensors/devices",
        quantity="*",
        attributes=[
            NWBAttributeSpec(
                name="sensor", doc="Sensor from which event-based data was collected", dtype=RefSpec("WearableSensor", "object"), required=True
            ),
            NWBAttributeSpec(
                name="name", doc="Name of the event", dtype="text", required=True
            ),
        ],
    )

    return [wearable_device, wearable_timeseries]

