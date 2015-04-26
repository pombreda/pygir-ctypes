Pure Python GObject Introspection Repository (GIR) wrapper using ctypes.


### Supported interpreters ###
  * CPython >= 2.7
  * CPython >= 3.0
  * PyPy >= 1.4.0


### Supported platforms ###
  * Linux
  * Windows
  * MacOS X
  * other platforms


### Hello World example ###
```
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
```

### Hello World example using classes ###
```
from gir import Gtk

class MainWindow(Gtk.Window):
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
```