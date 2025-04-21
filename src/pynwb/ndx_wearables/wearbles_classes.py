#  Creating custom class (like how Lauren built WearableDevice, WearableSensor) 
# Will likely need to copy/paste this in after merge?

@register_class("WearableEvents", "ndx-wearables")
class WearableEvents(Events):
    __nwbfields__ = ("name", "sensor")

    @docval(
        {"name": "name", "type": str, "doc": "Name of the event"},
        {"name": "sensor", "type": WearableSensor, "doc": "Sensor associated with the event"},
        *get_docval(Events.__init__, 'timestamps', 'description')  # Include other required fields
    )
    def __init__(self, **kwargs):
        sensor = popargs("sensor", kwargs)
        super().__init__(**kwargs)
        self.sensor = sensor



