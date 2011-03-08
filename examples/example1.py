import sys
sys.path.append('..')

import gir

if __name__ == '__main__':
	rep = gir.GIRepository()
	Gtk = rep.require('Gtk')
	GObject = rep.require('GObject')
	GLib = rep.require('GLib')
	
	r = Gtk.init()
	print(r)
	# Gtk.main()
