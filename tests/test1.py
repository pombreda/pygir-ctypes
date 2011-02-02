# print all possible infos that are fetched from repository
import os
import sys
sys.path.append('..')
from gir._gir import *

if __name__ == '__main__':
	g_type_init()
	gir = g_irepository_get_default()
	
	Gtk = g_irepository_require(gir, gchar_p('Gtk'), None, G_IREPOSITORY_LOAD_FLAG_LAZY, None)
	n_infos = g_irepository_get_n_infos(gir, gchar_p('Gtk'))
	
	for i in range(n_infos):
		info = g_irepository_get_info(gir, gchar_p('Gtk'), gint(i))
		type = g_base_info_get_type(info)
		name = g_base_info_get_name(info)
		
		print(info, name_GIInfoType[type], name)
		
	g_typelib_free(Gtk)
