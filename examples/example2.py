import sys
sys.path.append('..')

import gir
rep = gir.GIRepository()
Gtk = rep.Gtk

class MainWindow(Gtk.Window):
	def __new__(cls, *args, **kwargs):
		print('MainWindow.__new__:', cls, args, kwargs)
		self = super(MainWindow, cls).new(Gtk.WindowType.toplevel)
		print('*', self)
		return self
	
	def __init__(self, *args, **kwargs):
		print('MainWindow.__init__', self, args, kwargs)
		Gtk.Window.__init__(self, *args, **kwargs)
		#~ self.set_title('Test 1')
		#~ vbox = Gtk.VBox.new(False, 0)
		#~ label = Gtk.Label.new('Hello world!')
		#~ vbox.pack_start(label, True, True, 10)
		#~ button = Gtk.Button.new_from_stock('gtk-quit')
		#~ button.connect('clicked', self.cb_button_clicked)
		#~ vbox.pack_start(button, False, True, 0)
		#~ self.add(vbox)
		#~ self.show_all()
		#~ self.connect('delete-event', self.cb_window_delete_event)
		#~ self.connect('destroy', self.cb_window_destroy)
	
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
	Gtk.init(0, [])
	window = MainWindow()
	Gtk.main()
