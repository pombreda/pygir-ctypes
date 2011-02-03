import os
import sys
sys.path.append('..')
from gir import *

if __name__ == '__main__':
	Gir = GIRepository()
	#~ print(Gir)
	
	GObject = Gir.require('GObject', None, GIRepositoryLoadFlags.LAZY, None)
	#~ print(GObject)
	
	Gtk = Gir.require('Gtk', None, GIRepositoryLoadFlags.LAZY, None)
	#~ print(Gtk)
	
	#~ print(GObject.signal_connect_closure)
	#~ print(Gtk.Window)
	#~ print(Gtk.Window.get_parent)
	#~ print(Gtk.Window.get_parent())
	#~ print(Gtk.Window.get_name())
	#~ print(Gtk.Window.get_parent().get_name())
	#~ print(Gtk.main)
	#~ Gtk.main()
	
	print(Gtk.Window)
	print(Gtk.Window.get_name)
	print(Gtk.Window.get_name())
	print(Gtk.WindowType)
	print(Gtk.WindowType.get_name())
	print(Gtk.WindowType.get_n_values())
	print(Gtk.WindowType.get_value(0))
	print(Gtk.WindowType.get_value(0).get_name)
	print(Gtk.WindowType.get_value(0).get_name())
	print(Gtk.Window.find_method('new'))
	print(Gtk.Widget.find_method('show'))
	
