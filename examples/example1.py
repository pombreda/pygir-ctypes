import sys
sys.path.append('..')

from gir import Gtk

def cb_window_delete_event(window, *args, **kwargs):
	print('cb_window_delete_event:', window, args, kwargs)
	return False

def cb_window_destroy(window, *args, **kwargs):
	print('cb_window_destroy:', window, args, kwargs)
	Gtk.main_quit()

def cb_button_clicked(button, *args, **kwargs):
	print('cb_button_clicked:', window, args, kwargs)
	Gtk.main_quit()

if __name__ == '__main__':
	window = Gtk.Window.new(Gtk.WindowType.toplevel)
	window.set_title(__file__)
	vbox = Gtk.VBox(homogeneous=False, spacing=0)
	label = Gtk.Label(label='Hello world!')
	vbox.pack_start(label, True, True, 10)
	button = Gtk.Button.new_from_stock('gtk-quit')
	button.connect('clicked', cb_button_clicked)
	vbox.pack_start(button, False, True, 0)
	window.add(vbox)
	window.show_all()
	window.connect('delete-event', cb_window_delete_event)
	window.connect('destroy', cb_window_destroy)
	Gtk.main()
