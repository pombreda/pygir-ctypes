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

def cb_window_destroy(window, *args):
	print window, args
	Gtk.main_quit()

if __name__ == '__main__':
	Gtk.init(0, [])
	window = Gtk.Window.new(Gtk.WindowType.toplevel)
	window.set_title('Test 1')
	window.show_all()
	
	# create and connect closure to window
	hid = window.connect('destroy', cb_window_destroy, None)
	print hid
	
	Gtk.main()
