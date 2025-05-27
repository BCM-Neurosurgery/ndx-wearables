from pynwb import register_class
from pynwb.base import MultiContainerInterface
from hdmf.utils import docval, popargs, get_docval
from pynwb import NWBContainer
    def __init__(self, **kwargs):
        description = popargs('description', kwargs)
        super().__init__(**kwargs)
        self.description = description

