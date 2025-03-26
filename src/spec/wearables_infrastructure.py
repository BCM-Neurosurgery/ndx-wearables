from pynwb import register_class, NWBContainer
from pynwb.core import MultiContainerInterface
from pynwb.spec import NWBGroupSpec, NWBDatasetSpec, NWBNamespaceBuilder, NWBAttributeSpec
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
        name = popargs("name", kwargs)
        description = popargs("description", kwargs)
        manufacturer = popargs("manufacturer", kwargs)
        location = popargs("location", kwargs)

        super().__init__(**kwargs)

        self.name = name
        self.description = description
        self.manufacturer = manufacturer
        self.location = location

@register_class("Sensor", "ndx-wearables")
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
        name = popargs("name", kwargs)
        description = popargs("description", kwargs)
        device = popargs("device", kwargs)

        super().__init__(**kwargs)

        self.name = name
        self.description = description
        self.device = device

@register_class("WearableSeries", "ndx-wearables")
class WearableSeries(TimeSeries):
    '''
    - data
    - unit (included in timeseries)
    - sensor
    '''
    __nwbfields__ = ({'name': 'sensor', 'doc':'', })

    @docval(*get_docval(TimeSeries.__init__, 'name'),
            {
                'name': 'data', 'type': ('array_data', 'data', TimeSeries), # required
                'shape': ((None, None), (None, None, None)),
                'doc': ''
            },
            {
                'name': 'sensor', 'type': WearableSensor, # required
                'doc': ''
            },
    )

    def __init__(self, **kwargs):
        self.sensor = kwargs['sensor']
        self.data = kwargs['data']

        # TODO: add logic for checking data shape - should we check data shape?
        data_shape = get_data_shape(kwargs['data'], strict_no_data_load = True)

        super().__init__(**kwargs)
    
    def get_sensor(self):
        # note: is this necessary?
        return self.sensor

@register_class("PhysiologicalMeasure", "ndx-wearables")
class PhysiologicalMeasure(MultiContainerInterface):
    '''
    - wearableseries
    '''
    __clsconf__ = [
        {
            'attr': 'wearable_series',
            'type': WearableSeries,
            'add': 'add_wearable_series',
            'get': 'get_wearable_series',
            'create': 'create_wearable_series'
        }]

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
                name="description", doc="Description of wearable device", dtype=str, required=False
            ),
            NWBAttributeSpec(
                name="manufacturer", doc="Wearable device manufacturer", dtype=str, required=False
            ),
            NWBAttributeSpec(
                name="location", doc="Location of wearable device on body", dtype=str, required=True
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
                name="description", doc="Description of sensor on wearable device", dtype=str, required=False
            ),
            NWBAttributeSpec(
                name="device", doc="Wearable device associated with the sensor", dtype=WearableDevice, required=True
            ),
        ],
    )

    #TODO: add dims field?
    wearable_timeseries = NWBDatasetSpec(
        neurodata_type_def="WearableTimeseries",
        neurodata_type_inc="NWBDatasetSpec",
        doc="Sensor on wearable device from which data was recorded",
        quantity="*",
        dtype=(float, int, str), #?
        shape=((None, None), (None, None, None)),
        dims=(("measurement_duration", "data"),("measurement_duration", "data", "time")),
        attributes=[
            NWBAttributeSpec(
                name="sensor", doc="Sensor from which data was collected", dtype=WearableSensor, required=True
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

