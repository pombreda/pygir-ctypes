import os
import sys

from . import GObject
from . import Gtk

def override(module, namespace):
	try:
		override_module = globals()[namespace]
		module = override_module.override(module)
	except KeyError:
		pass
	
	return module
