import os
import sys
sys.path.append('..')
from gir import GIRepository

if __name__ == '__main__':
	Gir = GIRepository()
	Gtk = Gir.require('Gtk', None, GIRepositoryLoadFlags.LAZY)
