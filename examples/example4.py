import sys
sys.path.append('..')

from gir import Gtk, GObject, GLib

class MainWindow(Gtk.Window):
	def __init__(self, parent=None):
		Gtk.Window.__init__(self)
		self.set_title(__file__)
		self.set_resizable(False)
		self.connect('destroy', lambda *w: Gtk.main_quit())
		
		vbox = Gtk.VBox(homogeneous=False, spacing=0)
		self.add(vbox)
		vbox.set_border_width(5)
		
		label = Gtk.Label(label='')
		label.set_markup("Completion demo, try writing <b>total</b> or <b>gnome</b> for example.")
		vbox.pack_start(label, False, False, 0)
		
		entry = Gtk.Entry()
		completion = Gtk.EntryCompletion()
		completion_model = self.create_completion_model()
		completion.set_model(completion_model)
		completion.set_text_column(0)
		entry.set_completion(completion)
		vbox.pack_start(entry, False, False, 0)
		
		self.show_all()
	
	def create_completion_model(self):
		store = Gtk.ListStore.newv(1, [GObject.TYPE_STRING])
		iter = Gtk.TreeIter()
		
		iter = store.append(iter)
		store.set_value(iter, 0, 'gnome')
		
		iter = store.append(iter)
		store.set_value(iter, 0, 'total')
		
		iter = store.append(iter)
		store.set_value(iter, 0, 'totally')
		
		return store

def main():
	MainWindow()
	Gtk.main()

if __name__ == '__main__':
	main()
