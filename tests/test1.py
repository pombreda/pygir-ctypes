import os
import sys
sys.path.append('..')
from gir import *

# version
version_info = tuple(sys.version_info)

if version_info[0] == 2:
	PY2, PY3 = True, False
elif version_info[0] == 3:
	PY2, PY3 = False, True
else:
	print('Not supported Python version: %s' % sys.version)
	sys.exit(1)

if __name__ == '__main__':
	func_g_type_init()
	_gir = func_g_irepository_get_default()
	
	_Gtk = func_g_irepository_require(_gir, c_char_p('Gtk'), None, enum_G_IREPOSITORY_LOAD_FLAG_LAZY, None)
	n_infos = func_g_irepository_get_n_infos(_gir, c_char_p('Gtk'))
	
	for i in range(n_infos):
		info = func_g_irepository_get_info(_gir, c_char_p('Gtk'), c_int(i))
		type = func_g_base_info_get_type(info)
		name = func_g_base_info_get_name(info)
		
		if PY3:
			name = name.decode('utf-8')
		
		print(info, name_GIInfoType[type], name)
		
		#~ if name == 'main':
			#~ print(info, name_GIInfoType[type], name)
			#~ r = union_GIArgument()
			#~ 
			#~ func_g_function_info_invoke(cast(info, POINTER(struct_GIFunctionInfo)), None, 0, None, 0, pointer(r), None)
			#~ 
			#~ print(r)
	
	func_g_typelib_free(_Gtk)
