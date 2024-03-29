import sys
sys.path.append('..')

from gir import Gtk

class MainWindow(Gtk.Window):
	def __new__(cls, *args, **kwargs):
		print('MainWindow.__new__:', cls, args, kwargs)
		self = super(MainWindow, cls).new(Gtk.WindowType.toplevel)
		return self
	
	def __init__(self):
		print('MainWindow.__init__', self)
		Gtk.Window.__init__(self)
		screen = self.get_screen()
		self.set_screen(screen)
		self.set_title('Test 1')
		vbox = Gtk.VBox(homogeneous=False, spacing=0)
		label = Gtk.Label(label='Hello world!')
		vbox.pack_start(label, True, True, 10)
		button = Gtk.Button.new_from_stock('gtk-quit')
		button.connect('clicked', self.cb_button_clicked)
		vbox.pack_start(button, False, True, 0)
		self.add(vbox)
		self.show_all()
		self.connect('delete-event', self.cb_window_delete_event)
		self.connect('destroy', self.cb_window_destroy)
	
	def cb_window_delete_event(self, window, *args, **kwargs):
		print('MainWindow.cb_window_delete_event:', window, args, kwargs)
		return False
	
	def cb_window_destroy(self, window, *args, **kwargs):
		print('MainWindow.cb_window_destroy:', window, args, kwargs)
		Gtk.main_quit()
	
	def cb_button_clicked(self, button, *args, **kwargs):
		print('MainWindow.cb_button_clicked:', window, args, kwargs)
		Gtk.main_quit()

if __name__ == '__main__':
	window = MainWindow()
	Gtk.main()
