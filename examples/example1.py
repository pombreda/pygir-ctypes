import sys
sys.path.append('..')

import gir
import gir._girepository

if __name__ == '__main__':
	rep = gir.GIRepository()
	GLib = rep.GLib
	#~ GLib._wrap_all()
	
	GObject = rep.GObject
	#~ GObject._wrap_all()
	
	Gtk = rep.Gtk
	#~ Gtk._wrap_all()
	
	#~ print(gir, dir(gir))
	#~ print(rep, dir(rep))
	#~ print(Gtk, dir(Gtk))
	#~ print(Gtk, dir(Gtk.Window))
	
	#~ print(GObject, dir(GObject))
	#~ print(GObject, dir(GObject.Object))
	#~ print(GObject.Closure, dir(GObject.Closure))
	#~ 
	#~ closure = GObject.Closure()
	#~ print(closure, dir(closure))
	
	#~ print(Gtk, dir(Gtk), Gtk._attrs.keys())
	#~ print(Gtk.Window)
	#~ print(Gtk, dir(Gtk), Gtk._attrs.keys())
	#~ Gtk._wrap_all()
	#~ print(Gtk, dir(Gtk), Gtk._attrs.keys())
	
	#~ print(Gtk.Window)
	#~ print(Gtk.Window.__bases__)
	#~ print(Gtk.Window.__mro__)
	#~ print(Gtk.Window.connect)
	#~ print(GObject.signal_connect_data)
	
	#~ print(Gtk.Label)
	#~ print(Gtk.Label.__bases__)
	#~ print(Gtk.Label.__mro__)
	
	#~ print(Gtk.Entry)
	#~ print(Gtk.Entry.__bases__)
	#~ print(Gtk.Entry.__mro__)
	
	Gtk.init(0, [])
	window = Gtk.Window.new(Gtk.WindowType.toplevel)
	window.set_title('Test 1')
	window.show_all()
	#~ closure_p = gir._girepository.closure_new(Gtk.main_quit)
	#~ gclosure_p = gir._girepository.cast(closure_p, gir._girepository.POINTER(gir._girepository.GClosure))
	#~ hid = GObject.signal_connect_closure(window._self, 'destroy', gclosure_p, False)
	#~ _data = gir._girepository.cast(window._self, gir._girepository.POINTER(gir._girepository.Closure))
	#~ size = gir._girepository.sizeof()
	#~ print size
	#~ closure = GObject.Closure.new_object(size, window)
	#~ closure = GObject.Closure.new_object(32, window)
	#~ print closure, dir(closure)
	#~ print closure._self
	#~ Gtk.main()
