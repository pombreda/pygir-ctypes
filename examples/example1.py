import sys
sys.path.append('..')

import gir

if __name__ == '__main__':
	rep = gir.GIRepository()
	Gtk = rep.Gtk
	GObject = rep.GObject
	GLib = rep.GLib
	
	#~ print(Gtk, dir(Gtk), Gtk._attrs.keys())
	#~ print(Gtk.Window)
	#~ print(Gtk, dir(Gtk), Gtk._attrs.keys())
	#~ Gtk._wrap_all()
	#~ print(Gtk, dir(Gtk), Gtk._attrs.keys())
	
	#~ print(Gtk.Window)
	#~ print(Gtk.Window.__bases__)
	#~ print(Gtk.Window.__mro__)
	
	#~ print(Gtk.Label)
	#~ print(Gtk.Label.__bases__)
	#~ print(Gtk.Label.__mro__)
	
	#~ print(Gtk.Entry)
	#~ print(Gtk.Entry.__bases__)
	#~ print(Gtk.Entry.__mro__)
	
	#~ Gtk.init(0, [])
	#~ w = Gtk.Window(Gtk.WindowType.toplevel)
	#~ w.set_title('Test 1')
	#~ w.show_all()
	#~ Gtk.main()
