from .. import _gobject

def override(module):
	class GType(int):
		pass
	
	TYPE_GTYPE = _gobject.G_TYPE_GTYPE.value
	TYPE_INVALID = _gobject.G_TYPE_INVALID.value
	TYPE_NONE = _gobject.G_TYPE_NONE.value
	TYPE_INTERFACE = _gobject.G_TYPE_INTERFACE.value
	TYPE_CHAR = _gobject.G_TYPE_CHAR.value
	TYPE_UCHAR = _gobject.G_TYPE_UCHAR.value
	TYPE_BOOLEAN = _gobject.G_TYPE_BOOLEAN.value
	TYPE_INT = _gobject.G_TYPE_INT.value
	TYPE_UINT = _gobject.G_TYPE_UINT.value
	TYPE_LONG = _gobject.G_TYPE_LONG.value
	TYPE_ULONG = _gobject.G_TYPE_ULONG.value
	TYPE_INT64 = _gobject.G_TYPE_INT64.value
	TYPE_UINT64 = _gobject.G_TYPE_UINT64.value
	TYPE_ENUM = _gobject.G_TYPE_ENUM.value
	TYPE_FLAGS = _gobject.G_TYPE_FLAGS.value
	TYPE_FLOAT = _gobject.G_TYPE_FLOAT.value
	TYPE_DOUBLE = _gobject.G_TYPE_DOUBLE.value
	TYPE_STRING = _gobject.G_TYPE_STRING.value
	TYPE_POINTER = _gobject.G_TYPE_POINTER.value
	TYPE_BOXED = _gobject.G_TYPE_BOXED.value
	TYPE_PARAM = _gobject.G_TYPE_PARAM.value
	TYPE_OBJECT = _gobject.G_TYPE_OBJECT.value
	TYPE_VARIANT = _gobject.G_TYPE_VARIANT.value
	TYPE_RESERVED_GLIB_FIRST = _gobject.G_TYPE_RESERVED_GLIB_FIRST.value
	TYPE_RESERVED_GLIB_LAST = _gobject.G_TYPE_RESERVED_GLIB_LAST.value
	TYPE_RESERVED_BSE_FIRST = _gobject.G_TYPE_RESERVED_BSE_FIRST.value
	TYPE_RESERVED_BSE_LAST = _gobject.G_TYPE_RESERVED_BSE_LAST.value
	TYPE_RESERVED_BSE_LAST = _gobject.G_TYPE_RESERVED_BSE_LAST.value
	
	# attach new attributes
	for attr, value in locals().items():
		if attr != 'module':
			setattr(module, attr, value)
	
	return module
