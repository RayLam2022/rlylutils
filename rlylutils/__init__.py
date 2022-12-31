import os
from importlib import import_module


if os.getenv('Cparam') == None:
    os.environ['Cparam'] = input('Cparam:')

from rlylutils.decorators.decorators import *
from rlylutils.configs.cfg import *

from rlylutils.utils import *








