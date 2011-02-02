# print all possible infos that are fetched from repository
import os
import sys
sys.path.append('..')
from gir._gir import *

if __name__ == '__main__':
	g_type_init()
	Gir = g_irepository_get_default()
	
	Gtk = g_irepository_require(
		Gir,
		gchar_p('Gtk'),
		None,
		G_IREPOSITORY_LOAD_FLAG_LAZY,
		None
	)
	
	n_infos = g_irepository_get_n_infos(Gir, gchar_p('Gtk'))
	
	for i in range(n_infos):
		info = g_irepository_get_info(Gir, gchar_p('Gtk'), gint(i))
		info_print(info)
		
	g_typelib_free(Gtk)
