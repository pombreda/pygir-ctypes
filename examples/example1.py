import sys
sys.path.append('..')

import gir

if __name__ == '__main__':
	rep = gir.GIRepository()
	Gtk = rep.require('Gtk', '2.0')
	GObject = rep.require('GObject', '2.0')
	GLib = rep.require('GLib', '2.0')
	
	print(Gtk.main)
	
	Gtk.init()
	Gtk.main()
