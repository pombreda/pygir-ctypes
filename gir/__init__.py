import os
import sys
from .girepository import *

# HACK: override "gir" package to be instance of GIRepository
try:
	sys.modules[__package__] = GIRepository()
except NameError:
	sys.modules[__name__] = GIRepository()
	
