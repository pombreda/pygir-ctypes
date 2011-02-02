# find Gtk.main and call it
import os
import sys
sys.path.append('..')
from gir._gir import *

if __name__ == '__main__':
	g_type_init()
	gir = g_irepository_get_default()
	
	Gtk = g_irepository_require(gir, gchar_p('Gtk'), None, G_IREPOSITORY_LOAD_FLAG_LAZY, None)
	Gtk_main = g_irepository_find_by_name(gir, gchar_p('Gtk'), gchar_p('main'))
	
	in_args = GIArgument()
	out_args = GIArgument()
	return_value = GIArgument()
	
	g_function_info_invoke(
		cast(Gtk_main, POINTER(GIFunctionInfo)),
		pointer(in_args),
		0,
		pointer(out_args),
		0,
		pointer(return_value),
		None
	)
	
	g_typelib_free(Gtk)
