import os
import sys
from ctypes import *
from ctypes.util import find_library

def ctypes_get_func(lib, name, restype=None, *argtypes):
	func = getattr(lib, name)
	func.restype = restype
	func.argtypes = argtypes
	return func
