import sys
sys.path.append('..')
import threading

import gir
import gir._girepository

if __name__ == '__main__':
	rep = gir.GIRepository()
	Gtk = rep.require('Gtk')
	GObject = rep.require('GObject')
	GLib = rep.require('GLib')
	
	#~ print(Gtk)
	#~ print(dir(Gtk))
	#~ print(Gtk.Window)
	#~ print(Gtk.Window.__bases__)
	#~ print(Gtk.Window.__mro__)
	#~ print(dir(Gtk.Window))
	
	#~ print(Gtk.Label)
	#~ print(Gtk.Label.__bases__)
	#~ print(Gtk.Label.__mro__)
	
	#~ print(Gtk.Entry)
	#~ print(Gtk.Entry.__bases__)
	#~ print(Gtk.Entry.__mro__)
	
	#~ print(Gtk.WindowType)
	#~ print(Gtk.WindowType.__bases__)
	#~ print(Gtk.WindowType.__mro__)
	#~ print(dir(Gtk.WindowType))
	#~ print(Gtk.WindowType.popup)
	#~ print(Gtk.WindowType.toplevel)
	
	#~ Gtk.init(0, [])
	#~ w = Gtk.Window(Gtk.WindowType.toplevel)
	#~ w.set_title('Test 1')
	#~ w.show_all()
	#~ Gtk.main()
