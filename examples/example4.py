import sys
sys.path.append('..')

from gir import Gtk, GObject, GLib

class MainWindow(Gtk.Window):
	def __new__(cls, *args, **kwargs):
		self = super(MainWindow, cls).new(Gtk.WindowType.toplevel)
		return self
	
	def __init__(self, parent=None):
		# super(Gtk.Window, MainWindow).__init__(self)
		self.set_resizable(False)
		self.connect('destroy', lambda *w: Gtk.main_quit())
		
		vbox = Gtk.VBox.new(False, 5)
		self.add(vbox)
		vbox.set_border_width(5)
		
		label = Gtk.Label.new('')
		label.set_markup("Completion demo, try writing <b>total</b> or <b>gnome</b> for example.")
		vbox.pack_start(label, False, False, 0)
		
		entry = Gtk.Entry.new()
		completion = Gtk.EntryCompletion.new()
		#~ completion_model = self.__create_completion_model()
		#~ completion.set_model(completion_model)
		#~ completion.set_text_column(0)
		entry.set_completion(completion)
		vbox.pack_start(entry, False, False, 0)
		
		self.show_all()

	#~ def __create_completion_model(self):
		#~ store = Gtk.ListStore.newv(1, [GObject.TYPE_STRING])
		
		#~ iter = store.append()
		#~ store.set(iter, 0, "GNOME")
		#~ 
		#~ iter = store.append()
		#~ store.set(iter, 0, "total")
		#~ 
		#~ iter = store.append()
		#~ store.set(iter, 0, "totally")
		
		#~ return store

def main():
	Gtk.init(len(sys.argv), sys.argv)
	MainWindow()
	Gtk.main()

if __name__ == '__main__':
	main()
