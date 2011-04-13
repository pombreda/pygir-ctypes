import pygtk
import gtk

def cb_window_delete_event(window, *args, **kwargs):
	print('cb_window_delete_event:', window, args, kwargs)
	return False

def cb_window_destroy(window, *args, **kwargs):
	print('cb_window_destroy:', window, args, kwargs)
	gtk.main_quit()

def cb_button_clicked(button, *args, **kwargs):
	print('cb_button_clicked:', button, args, kwargs)
	gtk.main_quit()

def main(skip_main=False):
	window = gtk.Window(0)
	window.set_title('Test 1')
	vbox = gtk.VBox(False, 0)
	label = gtk.Label('Hello world!')
	vbox.pack_start(label, True, True, 10)
	button = gtk.Button(stock='gtk-quit')
	button.connect('clicked', cb_button_clicked)
	vbox.pack_start(button, False, True, 0)
	window.add(vbox)
	window.show_all()
	window.connect('delete-event', cb_window_delete_event)
	window.connect('destroy', cb_window_destroy)
	if not skip_main: gtk.main()

if __name__ == '__main__':
	main()
