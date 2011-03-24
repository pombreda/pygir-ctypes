import sys
sys.path.append('..')

import gir
import gir._girepository

if __name__ == '__main__':
	rep = gir.GIRepository()
	GLib = rep.GLib
	GLib._wrap_all()
	
	GObject = rep.GObject
	GObject._wrap_all()
	
	Gtk = rep.Gtk
	Gtk._wrap_all()
	
	print [n for n in dir(GObject) if 'connect' in n]
	
	#~ Gtk.init(0, [])
	#~ window = Gtk.Window.new(Gtk.WindowType.toplevel)
	#~ window.set_title('Test 1')
	#~ window.show_all()
	#~ closure_p = gir._girepository.closure_new(Gtk.main_quit)
	#~ gclosure_p = gir._girepository.cast(closure_p, gir._girepository.POINTER(gir._girepository.GClosure))
	#~ hid = GObject.signal_connect_closure(window._self, 'destroy', gclosure_p, False)
	#~ _data = gir._girepository.cast(window._self, gir._girepository.POINTER(gir._girepository.Closure))
	#~ size = gir._girepository.sizeof()
	#~ print size
	#~ closure = GObject.Closure.new_object(size, window)
	#~ closure_p = gir._girepository.closure_new(Gtk.main_quit)
	#~ closure = GObject.Closure(_self=closure_p)
	#~ hid = GObject.signal_connect_closure(window, 'destroy', closure, False)
	#~ print(hid)
	#~ print GObject.signal_connect_object
	#~ print GObject.signal_connect_data(window, 'destroy', Gtk.main_quit, None, 0)
	#~ Gtk.main()
