from pynwb import register_class, NWBContainer
from pynwb.core import MultiContainerInterface
from pynwb.spec import NWBGroupSpec, NWBDatasetSpec, NWBNamespaceBuilder, NWBAttributeSpec, RefSpec
from pynwb.base import TimeSeries

from hdmf.utils import docval, popargs, get_docval, get_data_shape

from datetime import datetime
from dateutil.tz import tzlocal
import numpy as np

'''
def make_physiological_measures():
    #ns_builder.include_type("WearableTimeseries")

    hr = NWBGroupSpec(
        "Heart Rate TimeSeries",
        attributes=[],
        neurodata_type_inc="TimeSeries",
        neurodata_type_def="HeartRateSeries",
    )
    
    return hr
'''
''' alternate '''
'''
@register_class("WearableTimeseries")
class WearableTimeseries(TimeSeries):
    __nwbfields__ = ("name") # insert wearables-specific fields here

    @docval(
        {"name": "name", "type": str, "doc": "Physiological Measure"},
    )

    def __init__(self, **kwargs):
        super().__init__(name=kwargs["name"])

def make_physiological_measures_alt():
    hr = NWBGroupSpec(
        "Heart Rate WearableTimeseries",
        attributes=[],
        neurodata_type_inc="WearableTimeseries",
        neurodata_type_def="HeartRateSeries",
    )

    hrv = NWBGroupSpec(
        "Heart Rate Variability WearableTimeseries",
        attributes=[],
        neurodata_type_inc="WearableTimeseries",
        neurodata_type_def="HeartRateSeries",
    )

    return hr, hrv

'''

#TODO: fill out docs


#note: may need to break out into a separate file?
#pynwb mentions that these are generally done in separate files
def make_wearables_infrastructure():
    wearable_device = NWBGroupSpec(
        neurodata_type_def="WearableDevice",
        neurodata_type_inc="NWBDataInterface",
        doc="Wearable device from which data was recorded",
        quantity="*",
        attributes=[
            NWBAttributeSpec(
                name="description", doc="Description of wearable device", dtype="text", required=False
            ),
            NWBAttributeSpec(
                name="manufacturer", doc="Wearable device manufacturer", dtype="text", required=False
            ),
            NWBAttributeSpec(
                name="location", doc="Location of wearable device on body", dtype="text", required=True
            ),
        ],
    )
    
    wearable_sensor = NWBGroupSpec(
        neurodata_type_def="WearableSensor",
        neurodata_type_inc="NWBDataInterface",
        doc="Sensor on wearable device from which data was recorded",
        quantity="*",
        attributes=[
            NWBAttributeSpec(
                name="description", doc="Description of sensor on wearable device", dtype="text", required=False
            ),
            NWBAttributeSpec(
                name="device", doc="Wearable device associated with the sensor", dtype=RefSpec("WearableDevice", "object"), required=True
            ),
        ],
    )

    #TODO: add dims field?
    wearable_timeseries = NWBGroupSpec(
        neurodata_type_def="WearableTimeSeries",
        neurodata_type_inc="NWBDataInterface",
        doc="Data recorded from wearable sensor/device",
        quantity="*",
        attributes=[
            NWBAttributeSpec(
                name="sensor", doc="Sensor from which data was collected", dtype=RefSpec("WearableSensor", "object"), required=True
            ),
            NWBAttributeSpec(
                name="data", doc="Data which was collected from sensor", dtype=RefSpec("TimeSeries", "object"), required=True
                # im not sure if the dtype here is correct
            ),
            NWBAttributeSpec(
                name="name", doc="Name of the series", dtype="text", required=True
            ),
        ],

    )

    physiological_measure = NWBGroupSpec(
        neurodata_type_def="PhysiologicalMeasure",
        neurodata_type_inc="NWBDataInterface",
        name="physiological_measure",
        doc="A grouping of wearable series data from various sensors/wearable devices",
        quantity="?",
        groups=[wearable_timeseries],
    )

    return [wearable_device, wearable_sensor, wearable_timeseries, physiological_measure]

