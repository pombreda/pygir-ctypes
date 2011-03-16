import sys
sys.path.append('..')

import gir

if __name__ == '__main__':
	rep = gir.GIRepository()
	Gtk = rep.require('Gtk')
	GObject = rep.require('GObject')
	GLib = rep.require('GLib')
	
	print(Gtk)
	print(Gtk.Window)
	print(Gtk.Window.__bases__)
	print(Gtk.Window.__mro__)
	
	print(Gtk.Label)
	print(Gtk.Label.__bases__)
	print(Gtk.Label.__mro__)
	
	# w = Gtk.Window()
	
	# r = Gtk.init()
	# print(r)
	# Gtk.main()
