import sys
sys.path.append('..')

import gir
import gir._girepository

rep = gir.GIRepository()
GLib = rep.GLib
# GLib._wrap_all()

GObject = rep.GObject
# GObject._wrap_all()

Gtk = rep.Gtk
# Gtk._wrap_all()

if __name__ == '__main__':
	Gtk.init(0, [])
	window = Gtk.Window.new(Gtk.WindowType.toplevel)
	window.set_title('Test 1')
	window.show_all()
	
	# create and connect closure to window
	_gclosure = gir._girepository.pyclosure_new(window._self, Gtk.main_quit)
	closure = GObject.Closure(_self=_gclosure)
	hid = GObject.signal_connect_closure(window, 'destroy', closure, False)
	
	Gtk.main()
