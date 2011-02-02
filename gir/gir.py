#
# High-level Python API
#
import os
import sys
import ctypes
import _gir

# Base class for Glib Python classes
# uses convention that class instance should be first argument
# of calling/invoking function
class _Object(object):
	_c_func_prefix = None
	
	# similar to __new__ but without calling __init__
	# useful when args are not known for __new__ or/and __init__
	@classmethod
	def _new_without_init(cls):
		self = super(_Object, cls).__new__(cls)
		self._c_obj = None
		return self
	
	# this is pygir convention for instatiating python class
	# without calling __new__ or __init__ and storing c_obj inside
	# python class instance with name '_c_obj'
	@classmethod
	def _new_with_c_obj(cls, c_obj):
		self = cls._new_without_init()
		self._c_obj = c_obj
		return self
	
	# generic repr function for all _Object derivatives
	def __repr__(self):
		return ''.join((
			'<',
			self.__class__.__name__,
			' (',
			self._c_obj.__class__.__name__,
			' object at ',
			hex(id(self._c_obj)),
			') object at ',
			hex(id(self)), '>'
		))
	
	# generic __getattr__ for all _GObject derivatives
	# requires _c_func_prefix
	def __getattr__(self, attr):
		c_attr = ''.join((self._c_func_prefix, attr))
		c_value = getattr(_gir, c_attr)
		py_value = convert_c_to_python_object(c_value)
		return lambda *args: py_value(self, *args)

# Base class for all _GObject derived classes in C
# but used as Python classes
class _GObject(_Object):
	pass

# Base class for all GI/GIR Python classes
# derived from _GObject but adapted for GI/GIR operations
class _GIObject(_GObject):
	pass

# Base class for all GI*Info Python classes
# derived from _Object - None Glib _Object classes
class _GIInfoObject(_Object):
	pass

#
# GIRepository
#
class GIRepository(_GIObject):
	_c_func_prefix = 'g_irepository_'
	
	def __init__(self):
		_gir.g_type_init()
		self._c_obj = _gir.g_irepository_get_default()
	
class GICallbackInfo(_GIInfoObject):
	def __init__(self):
		pass

#
# GIRepositoryError
#
class GIRepositoryError(object):
	(
		TYPELIB_NOT_FOUND,
		NAMESPACE_MISMATCH,
		NAMESPACE_VERSION_CONFLICT,
		LIBRARY_NOT_FOUND,
	) = range(4)

#
# GIRepositoryLoadFlags
#
class GIRepositoryLoadFlags(object):
	LAZY = 1 << 0

#
# GIBaseInfo
#
class GIBaseInfo(_GIInfoObject):
	_c_func_prefix = 'g_base_info_'
	
	def __init__(self):
		pass

class GIAttributeIter(object):
	def __init__(self):
		pass

class _GIObjectType(object):
	(
		INVALID,
		FUNCTION,
		CALLBACK,
		STRUCT,
		BOXED,
		ENUM,
		FLAGS,
		OBJECT,
		INTERFACE,
		CONSTANT,
		ERROR_DOMAIN,
		UNION,
		VALUE,
		SIGNAL,
		VFUNC,
		PROPERTY,
		FIELD,
		ARG,
		TYPE,
		UNRESOLVED
	) = range(20)

#
# GICallableInfo
#
class GICallableInfo(_GIInfoObject):
	_c_func_prefix = 'g_callable_info_'
	
	def __init__(self):
		pass

#
# GIFunctionInfo
#
class GIFunctionInfo(_GIInfoObject):
	_c_func_prefix = 'g_function_info_'
	
	def __init__(self):
		pass

class GInvokeError(object):
	(
		FAILED,
		SYMBOL_NOT_FOUND,
		ARGUMENT_MISMATCH
	) = range(3)

class GIFunctionInfoFlags(object):
	IS_METHOD = 1 << 0
	IS_CONSTRUCTOR = 1 << 1
	IS_GETTER = 1 << 2
	IS_SETTER = 1 << 3
	WRAPS_VFUNC = 1 << 4
	THROWS = 1 << 5

#
# GISignalInfo
#
class GISignalInfo(_GIInfoObject):
	_c_func_prefix = 'g_signal_info_'
	
	def __init__(self):
		pass

#
# GIVFuncInfo
#
class GIVFuncInfo(_GIInfoObject):
	_c_func_prefix = 'g_vfunc_info_'
	
	def __init__(self):
		pass

class GIVFuncInfoFlags(object):
	MUST_CHAIN_UP = 1 << 0
	MUST_OVERRIDE = 1 << 1
	MUST_NOT_OVERRIDE = 1 << 2

#
# GIRegisteredTypeInfo
#
class GIRegisteredTypeInfo(_GIInfoObject):
	_c_func_prefix = 'g_registered_type_info_'
	
	def __init__(self):
		pass

#
# GIEnumInfo
#
class GIEnumInfo(_GIInfoObject):
	_c_func_prefix = 'g_enum_info_'
	
	def __init__(self):
		pass

class GIValueInfo(_GIInfoObject):
	_c_func_prefix = 'g_value_info_'
	
	def __init__(self):
		pass

#
# GIInterfaceInfo
#
class GIInterfaceInfo(_GIInfoObject):
	_c_func_prefix = 'g_interface_info_'
	
	def __init__(self):
		pass

#
# _GIObjectInfo
#
class _GIObjectInfo(_GIInfoObject):
	_c_func_prefix = 'g_object_info_'
	
	def __init__(self):
		pass

#
# GIStructInfo
#
class GIStructInfo(_GIInfoObject):
	_c_func_prefix = 'g_struct_info_'
	
	def __init__(self):
		pass

#
# GIUnionInfo
#
class GIUnionInfo(_GIInfoObject):
	_c_func_prefix = 'g_union_info_'
	
	def __init__(self):
		pass

#
# GIArgInfo
#
class GIArgInfo(_GIInfoObject):
	_c_func_prefix = 'g_arg_info_'
	
	def __init__(self):
		pass

class GIDirection(object):
	(
		IN,
		OUT,
		INOUT,
	) = range(3)

class GIScopeType(object):
	(
		INVALID,
		CALL,
		ASYNC,
		NOTIFIED,
	) = range(4)

class GITransfer(object):
	(
		NOTHING,
		CONTAINER,
		EVERYTHING,
	) = range(3)

#
# GIArgument
#
class GIArgument(object):
	def __init__(self):
		pass

#
# GIConstantInfo
#
class GIConstantInfo(_GIInfoObject):
	_c_func_prefix = 'g_constant_info_'
	
	def __init__(self):
		pass

#
# GIErrorDomainInfo
#
class GIErrorDomainInfo(_GIInfoObject):
	_c_func_prefix = 'g_error_domain_info_'
	
	def __init__(self):
		pass

#
# GIFieldInfo
#
class GIFieldInfo(_GIInfoObject):
	_c_func_prefix = 'g_field_info_'
	
	def __init__(self):
		pass

class GIFieldInfoFlags(object):
	IS_READABLE = 1 << 0
	IS_WRITABLE = 1 << 1

#
# GIPropertyInfo
#
class GIPropertyInfo(_GIInfoObject):
	_c_func_prefix = 'g_property_info_'
	
	def __init__(self):
		pass

#
# GITypeInfo
#
class GITypeInfo(_GIInfoObject):
	_c_func_prefix = 'g_type_info_'
	
	def __init__(self):
		pass

class GIArrayType(object):
	(
		C,
		ARRAY,
		PTR_ARRAY,
		BYTE_ARRAY
	) = range(4)

class GITypeTag(object):
	VOID = 0
	BOOLEAN = 1
	INT8 =  2
	UINT8 =  3
	INT16 =  4
	UINT16 =  5
	INT32 =  6
	UINT32 =  7
	INT64 =  8
	UINT64 = 9
	FLOAT = 10
	DOUBLE = 11
	GTYPE = 12
	UTF8 = 13
	FILENAME = 14
	ARRAY = 15
	INTERFACE = 16
	GLIST = 17
	GSLIST = 18
	GHASH = 19
	ERROR = 20

#
# GITypelib
#

# NOTE: GITypelib is not on C-level subclass of _GObject
# but it is used that way because of calling convenction
# which states that instance should be first argument in function call
# so it mimics _GObject
class GITypelib(_Object):
	_c_func_prefix = 'g_typelib_'
	
	def __repr__(self):
		c_name = _gir.g_typelib_get_namespace(self._c_obj)
		py_name = convert_c_to_python_object(c_name)
		
		return ''.join((
			'<',
			py_name,
			' (',
			self._c_obj.__class__.__name__,
			' object at ',
			hex(id(self._c_obj)),
			') object at ',
			hex(id(self)),
			'>'
		))
	
	def __getattr__(self, attr):
		c_gir = _gir.g_irepository_get_default()
		c_name = _gir.g_typelib_get_namespace(self._c_obj)
		c_attr = _gir.gchar_p(attr)
		c_info = _gir.g_irepository_find_by_name(c_gir, c_name, c_attr)
		py_info = convert_c_to_python_object(c_info)
		return py_info

class GTypelibBlobType(object):
	(
		INVALID,
		FUNCTION,
		CALLBACK,
		STRUCT,
		BOXED,
		ENUM,
		FLAGS,
		OBJECT,
		INTERFACE,
		CONSTANT,
		ERROR_DOMAIN,
		UNION,
	) = range(12)

# Conversion from C to Python
# depends on ctypes, convert_python_to_c_object, _new_with_c_obj
def convert_c_to_python_object(c_obj):
	if isinstance(c_obj, ctypes._CFuncPtr):
		py_obj = lambda *py_args: convert_c_to_python_object(
			c_obj(
				*map(convert_python_to_c_object, py_args)
			)
		)
	elif isinstance(c_obj, ctypes._Pointer):
		py_class = globals()[c_obj._type_.__name__]
		py_obj = py_class._new_with_c_obj(c_obj)
	elif isinstance(c_obj, _gir.gboolean):
		py_obj = bool(c_obj.value)
	elif isinstance(c_obj, _gir.gint8) or \
		isinstance(c_obj, _gir.guint8) or \
		isinstance(c_obj, _gir.gint16) or \
		isinstance(c_obj, _gir.guint16) or \
		isinstance(c_obj, _gir.gint32) or \
		isinstance(c_obj, _gir.guint32) or \
		isinstance(c_obj, _gir.gint64) or \
		isinstance(c_obj, _gir.guint64) or \
		isinstance(c_obj, _gir.gshort) or \
		isinstance(c_obj, _gir.gushort) or \
		isinstance(c_obj, _gir.gint) or \
		isinstance(c_obj, _gir.guint) or \
		isinstance(c_obj, _gir.glong) or \
		isinstance(c_obj, _gir.gulong) or \
		isinstance(c_obj, _gir.gssize) or \
		isinstance(c_obj, _gir.gsize) or \
		isinstance(c_obj, _gir.gpointer):
			py_obj = c_obj.value
	elif isinstance(c_obj, _gir.gchar) or \
		isinstance(c_obj, _gir.gchar_p):
			py_obj = c_obj.value
	else:
		raise TypeError('cannot convert C to Python object: %s' % repr(c_obj))
	
	return py_obj

# Conversion from Python to C
# depends on _gir, _c_obj convention
def convert_python_to_c_object(py_obj):
	if isinstance(py_obj, type(None)):
		c_obj = py_obj
	elif isinstance(py_obj, bool):
		c_obj = _gir.gboolean(py_obj)
	elif isinstance(py_obj, int):
		c_obj = _gir.gint(py_obj)
	elif isinstance(py_obj, long):
		c_obj = _gir.glong(py_obj)
	elif isinstance(py_obj, float):
		c_obj = _gir.gdouble(py_obj)
	elif isinstance(py_obj, str):
		c_obj = _gir.gchar_p(py_obj)
	elif isinstance(py_obj, unicode):
		c_obj = _gir.gchar_p(py_obj)
	elif isinstance(py_obj, _GIInfoObject):
		c_obj = py_obj._c_obj
	elif isinstance(py_obj, _GIObject):
		c_obj = py_obj._c_obj
	elif isinstance(py_obj, _GObject):
		c_obj = py_obj._c_obj
	elif isinstance(py_obj, _Object):
		c_obj = py_obj._c_obj
	else:
		raise TypeError('cannot convert Python to C object: %s' % repr(py_obj))
	
	return c_obj
