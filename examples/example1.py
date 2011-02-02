import os
import sys
sys.path.append('..')
from gir import *

if __name__ == '__main__':
	Gir = GIRepository()
	print(Gir)
	Gtk = Gir.require('Gtk', None, GIRepositoryLoadFlags.LAZY, None)
	print(Gtk)
