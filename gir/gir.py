#
# High-level Python API
#
import os
import sys
import ctypes
import types
import _gir

#
# Utils
#
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
	else:
		raise TypeError('cannot convert C to Python object: %s' % repr(c_obj))
	
	return py_obj

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
	elif isinstance(py_obj, GIObject):
		# FIXME:
		raise TypeError('cannot convert Python to C object: %s' % repr(py_obj))
	elif isinstance(py_obj, GObject):
		c_obj = py_obj._c_obj
	else:
		raise TypeError('cannot convert Python to C object: %s' % repr(py_obj))
	
	return c_obj

# Base class for Glib Python classes
# uses convention that class instance should be first argument
# of calling/invoking function
class GObject(object):
	# similar to __new__ but without calling __init__
	# useful when args are not known for __new__ or/and __init__
	@classmethod
	def _new_without_init(cls):
		self = super(GObject, cls).__new__(cls)
		self._c_func_prefix = None
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
	
	# generic __getattr__ for all OBject derivatives
	# requires _c_func_prefix
	def __getattr__(self, attr):
		c_attr = ''.join((self._c_func_prefix, attr))
		c_value = getattr(_gir, c_attr)
		py_value = convert_c_to_python_object(c_value)
		return lambda *args: py_value(self, *args)

# Base class for all GI*Info Python classes
# derived from GObject but adapted for GI operations
class GIObject(GObject):
	pass

#
# GIRepository
#
class GIRepository(GObject):
	def __init__(self):
		_gir.g_type_init()
		self._c_func_prefix = 'g_irepository_'
		self._c_obj = _gir.g_irepository_get_default()

class GICallbackInfo(GIObject):
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

	def __init__(self):
		pass

#
# GIRepositoryLoadFlags
#
class GIRepositoryLoadFlags(object):
	LAZY = 1 << 0
	
	def __init__(self):
		pass

#
# GIBaseInfo
#
class GIBaseInfo(GIObject):
	def __init__(self):
		pass

class GIAttributeIter(object):
	def __init__(self):
		pass

class GIObjectType(object):
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
class GICallableInfo(GIObject):
	def __init__(self):
		pass

#
# GIFunctionInfo
#
class GIFunctionInfo(GIObject):
	def __init__(self):
		pass

class GInvokeError(object):
	(
		FAILED,
		SYMBOL_NOT_FOUND,
		ARGUMENT_MISMATCH
	) = range(3)
	
	def __init__(self):
		pass

class GIFunctionInfoFlags(object):
	IS_METHOD = 1 << 0
	IS_CONSTRUCTOR = 1 << 1
	IS_GETTER = 1 << 2
	IS_SETTER = 1 << 3
	WRAPS_VFUNC = 1 << 4
	THROWS = 1 << 5
	
	def __init__(self):
		pass

#
# GISignalInfo
#
class GISignalInfo(GIObject):
	def __init__(self):
		pass

#
# GIVFuncInfo
#
class GIVFuncInfo(GIObject):
	def __init__(self):
		pass

class GIVFuncInfoFlags(object):
	MUST_CHAIN_UP = 1 << 0
	MUST_OVERRIDE = 1 << 1
	MUST_NOT_OVERRIDE = 1 << 2
	
	def __init__(self):
		pass

#
# GIRegisteredTypeInfo
#
class GIRegisteredTypeInfo(GIObject):
	def __init__(self):
		pass

#
# GIEnumInfo
#
class GIEnumInfo(GIObject):
	def __init__(self):
		pass

class GIValueInfo(GIObject):
	def __init__(self):
		pass

#
# GIInterfaceInfo
#
class GIInterfaceInfo(GIObject):
	def __init__(self):
		pass

#
# GIObjectInfo
#
class GIObjectInfo(GIObject):
	def __init__(self):
		pass

#
# GIStructInfo
#
class GIStructInfo(GIObject):
	def __init__(self):
		pass

#
# GIUnionInfo
#
class GIUnionInfo(GIObject):
	def __init__(self):
		pass

#
# GIArgInfo
#
class GIArgInfo(GIObject):
	def __init__(self):
		pass

class GIDirection(object):
	(
		IN,
		OUT,
		INOUT,
	) = range(3)
	
	def __init__(self):
		pass

class GIScopeType(object):
	(
		INVALID,
		CALL,
		ASYNC,
		NOTIFIED,
	) = range(4)

	def __init__(self):
		pass

class GITransfer(object):
	(
		NOTHING,
		CONTAINER,
		EVERYTHING,
	) = range(3)
	
	def __init__(self):
		pass

#
# GIArgument
#
class GIArgument(object):
	def __init__(self):
		pass

#
# GIConstantInfo
#
class GIConstantInfo(GIObject):
	def __init__(self):
		pass

#
# GIErrorDomainInfo
#
class GIErrorDomainInfo(GIObject):
	def __init__(self):
		pass

#
# GIFieldInfo
#
class GIFieldInfo(GIObject):
	def __init__(self):
		pass

class GIFieldInfoFlags(object):
	IS_READABLE = 1 << 0
	IS_WRITABLE = 1 << 1
	
	def __init__(self):
		pass

#
# GIPropertyInfo
#
class GIPropertyInfo(GIObject):
	def __init__(self):
		pass

#
# GITypeInfo
#
class GITypeInfo(GIObject):
	def __init__(self):
		pass

class GIArrayType(object):
	(
		C,
		ARRAY,
		PTR_ARRAY,
		BYTE_ARRAY
	) = range(4)
	
	def __init__(self):
		pass

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
	
	def __init__(self):
		pass

#
# GITypelib
#

# NOTE: GITypelib is not on C-level subclass of GObject
# but it is used that way because of calling convenction
# which states that instance should be first argument in function call
# so it mimics GObject
class GITypelib(GObject):
	def __init__(self):
		pass

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
	
	def __init__(self):
		pass
