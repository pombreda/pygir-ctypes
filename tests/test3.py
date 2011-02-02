# C-level Gtk.Window example
import os
import sys
sys.path.append('..')
from gir._gir import *

def tmp1():
	g_type_init()
	Gir = g_irepository_get_default()
	
	GObject = g_irepository_require(
		Gir,
		gchar_p('GObject'),
		None,
		G_IREPOSITORY_LOAD_FLAG_LAZY,
		None
	)
	
	Gtk = g_irepository_require(
		Gir,
		gchar_p('Gtk'),
		None,
		G_IREPOSITORY_LOAD_FLAG_LAZY,
		None
	)
	
	Gtk_Window = g_irepository_find_by_name(Gir, gchar_p('Gtk'), gchar_p('Window'))
	info_print(Gtk_Window)
	
	#~ n_interfaces = g_object_info_get_n_interfaces(cast(Gtk_Window, POINTER(GIObjectInfo)))
	#~ 
	#~ for i in range(n_interfaces):
		#~ interface = g_object_info_get_interface(
			#~ cast(Gtk_Window, POINTER(GIObjectInfo)),
			#~ gint(i),
		#~ )
		#~ # info_print(interface)
	
	parent = g_object_info_get_parent(
		cast(Gtk_Window, POINTER(GIObjectInfo))
	)
	info_print(parent)
	
	#~ n = g_object_info_get_n_methods(
		#~ cast(parent, POINTER(GIObjectInfo))
	#~ ).value
	#~ 
	#~ for i in range(n):
		#~ info = g_object_info_get_method(
			#~ cast(parent, POINTER(GIObjectInfo)),
			#~ gint(i)
		#~ )
		#~ info_print(info)
	#~ print()
	
	parent = g_object_info_get_parent(
		cast(parent, POINTER(GIObjectInfo))
	)
	info_print(parent)
	
	#~ n = g_object_info_get_n_methods(
		#~ cast(parent, POINTER(GIObjectInfo))
	#~ ).value
	#~ 
	#~ for i in range(n):
		#~ info = g_object_info_get_method(
			#~ cast(parent, POINTER(GIObjectInfo)),
			#~ gint(i)
		#~ )
		#~ info_print(info)
	#~ print()
	
	parent = g_object_info_get_parent(
		cast(parent, POINTER(GIObjectInfo))
	)
	info_print(parent)
	
	n = g_object_info_get_n_methods(
		cast(parent, POINTER(GIObjectInfo))
	).value
	
	for i in range(n):
		info = g_object_info_get_method(
			cast(parent, POINTER(GIObjectInfo)),
			gint(i)
		)
		info_print(info)
	print()
	
	parent = g_object_info_get_parent(
		cast(parent, POINTER(GIObjectInfo))
	)
	info_print(parent)
		
	#~ n = g_object_info_get_n_methods(
		#~ cast(parent, POINTER(GIObjectInfo))
	#~ ).value
	#~ 
	#~ for i in range(n):
		#~ info = g_object_info_get_method(
			#~ cast(parent, POINTER(GIObjectInfo)),
			#~ gint(i)
		#~ )
		#~ info_print(info)
	#~ print()
	
	#~ Gtk_Window_new = g_object_info_find_method(
		#~ cast(Gtk_Window, POINTER(GIObjectInfo)),
		#~ gchar_p('new')
	#~ )
	#~ info_print(Gtk_Window_new)
	
	#~ Gtk_Window_connect = g_object_info_find_method(
		#~ cast(Gtk_Window, POINTER(GIObjectInfo)),
		#~ gchar_p('connect')
	#~ )
	#~ info_print(Gtk_Window_connect)
	
	#~ Gtk_main = g_irepository_find_by_name(gir, gchar_p('Gtk'), gchar_p('main'))
	#~ 
	#~ in_args = GIArgument()
	#~ out_args = GIArgument()
	#~ return_value = GIArgument()
	#~ 
	#~ g_function_info_invoke(
		#~ cast(Gtk_main, POINTER(GIFunctionInfo)),
		#~ pointer(in_args),
		#~ 0,
		#~ pointer(out_args),
		#~ 0,
		#~ pointer(return_value),
		#~ None
	#~ )
	
	g_typelib_free(Gtk)
	g_typelib_free(GObject)

if __name__ == '__main__':
	g_type_init()
	Gir = g_irepository_get_default()
	
	GObject = g_irepository_require(
		Gir,
		gchar_p('GObject'),
		None,
		G_IREPOSITORY_LOAD_FLAG_LAZY,
		None
	)
	
	Gtk = g_irepository_require(
		Gir,
		gchar_p('Gtk'),
		None,
		G_IREPOSITORY_LOAD_FLAG_LAZY,
		None
	)
	
	Gtk_Window = g_irepository_find_by_name(Gir, gchar_p('Gtk'), gchar_p('Window'))
	info_print(Gtk_Window)
	
	Gtk_Window_new = g_object_info_find_method(
		cast(Gtk_Window, POINTER(GIObjectInfo)),
		gchar_p('new')
	)
	info_print(Gtk_Window_new)
	
	Gtk_Window_show = g_object_info_find_method(
		cast(Gtk_Window, POINTER(GIObjectInfo)),
		gchar_p('show')
	)
	info_print(Gtk_Window_show)
	
	g_typelib_free(Gtk)
	g_typelib_free(GObject)
