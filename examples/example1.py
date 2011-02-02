import os
import sys
sys.path.append('..')
from gir import *

if __name__ == '__main__':
	Gir = GIRepository()
	print(Gir)
	
	GObject = Gir.require('GObject', None, GIRepositoryLoadFlags.LAZY, None)
	print(GObject)
	
	Gtk = Gir.require('Gtk', None, GIRepositoryLoadFlags.LAZY, None)
	print(Gtk)
	
	
