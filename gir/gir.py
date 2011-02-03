#
# Low-Level Python API
#
import os
import sys
import ctypes
from . import _gir

if list(sys.version_info)[0] == 2:
	PY2, PY3 = True, False
elif list(sys.version_info)[0] == 3:
	PY2, PY3 = False, True

#
# Base classes for low-level Python classes
#
class _Object(object):
	# uses convention that functiona name starts with prefix,
	# and class instance should be first argument of called function
	_c_class = None
	_c_prefix = None
	
	@classmethod
	def _new_without_init(cls):
		# similar to __new__ but without calling __init__
		# useful when args are not known for __new__ or/and __init__
		self = super(_Object, cls).__new__(cls)
		self._c_obj = None
		return self
	
	@classmethod
	def _new_with_c_obj(cls, c_obj):
		# this is pygir convention for instatiating python class
		# without calling __new__ or __init__ and storing c_obj inside
		# python class instance with name '_c_obj'
		self = cls._new_without_init()
		self._c_obj = c_obj
		return self
	
	def __repr__(self):
		# generic repr function for all _Object derivatives
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
	
	def __getattr__(self, attr):
		# generic __getattr__ for all _GObject derivatives
		mod_attr = ''.join((self._c_prefix, attr))
		c_value = getattr(_gir, mod_attr)
		
		py_value = self.convert_c_to_python_object(
			c_value,
			func_name=mod_attr,
		)
		
		return py_value
	
	def convert_c_to_python_object(self, c_obj, bind_self=True, func_name=''):
		# object conversion from c to python
		if isinstance(c_obj, ctypes._CFuncPtr):
			# wrap c function and bind self._c_obj
			if bind_self:
				py_obj = lambda *py_args: \
					self.convert_c_to_python_object(
						c_obj(
							self._c_obj,
							*map(self.convert_python_to_c_object, py_args)
						)
					)
			else:
				py_obj = lambda *py_args: \
					self.convert_c_to_python_object(
						c_obj(
							*map(self.convert_python_to_c_object, py_args)
						)
					)
			
			# set function name instead of '<lambda>'
			if PY2:
				py_obj.func_name = ''.join(('"', func_name, '"'))
			elif PY3:
				py_obj.__name__ = ''.join(('"', func_name, '"'))
			else:
				raise RuntimeError('unsupported python version')
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
				if PY2:
					py_obj = c_obj.value
				elif PY3:
					py_obj = c_obj.value.decode('utf-8')
				else:
					raise RuntimeError('unsupported python version')
		else:
			raise TypeError('cannot convert C to Python object: %s' % repr(c_obj))
		
		return py_obj

	def convert_python_to_c_object(self, py_obj):
		# Conversion from Python to C
		# depends on _gir, _c_obj convention
		
		if isinstance(py_obj, type(None)):
			c_obj = py_obj
		elif isinstance(py_obj, bool):
			c_obj = _gir.gboolean(py_obj)
		elif isinstance(py_obj, int):
			c_obj = _gir.gint(py_obj)
		elif PY2 and isinstance(py_obj, long):
			c_obj = _gir.glong(py_obj)
		elif isinstance(py_obj, float):
			c_obj = _gir.gdouble(py_obj)
		elif PY3 and isinstance(py_obj, bytes):
			c_obj = _gir.gchar_p(py_obj)
		elif isinstance(py_obj, str):
			c_obj = _gir.gchar_p(py_obj.encode('utf-8'))
		elif PY2 and isinstance(py_obj, unicode):
			c_obj = _gir.gchar_p(py_obj.encode('utf-8'))
		elif isinstance(py_obj, _GIInfoObject):
			c_obj = py_obj._c_obj
		elif isinstance(py_obj, _GObject):
			c_obj = py_obj._c_obj
		elif isinstance(py_obj, _Object):
			c_obj = py_obj._c_obj
		else:
			raise TypeError('cannot convert Python to C object: %s' % repr(py_obj))
		
		return c_obj
	
	def cast_python_to_python(self, py_obj, py_class):
		py_o = py_class._new_with_c_obj(
			ctypes.cast(py_obj._c_obj, ctypes.POINTER(py_class._c_class))
		)
		
		return py_o

class _GObject(_Object):
	# Base class for all GObject derived classes in C
	# but used low-level Python class
	pass

class _GIInfoObject(_Object):
	# Base class for all GI*Info Python classes
	# None GObject classes
	
	def __repr__(self):
		c_name = _gir.info_get_name(self._c_obj)
		py_name = self.convert_c_to_python_object(c_name)
		
		return ''.join((
			'<',
			self.__class__.__name__,
			' "',
			py_name,
			'" (',
			self._c_obj.__class__.__name__,
			' object at ',
			hex(id(self._c_obj)),
			') object at ',
			hex(id(self)),
			'>',
		))
	
	def __getattr__(self, attr):
		try:
			# search instance first
			mod_attr = ''.join((self._c_prefix, attr))
			c_value = getattr(_gir, mod_attr)
			py_value = self.convert_c_to_python_object(
				c_value,
				func_name=mod_attr,
			)
			return py_value
		except AttributeError:
			# avoid self.__class__ and 'object' classes
			for cls in self.__class__.__mro__[1:-1]:
				try:
					py_o = self.cast_python_to_python(self, cls)
					mod_attr = ''.join((cls._c_prefix, attr))
					c_value = getattr(_gir, mod_attr)
					py_value = py_o.convert_c_to_python_object(
						c_value,
						func_name=mod_attr,
					)
					return py_value
				except AttributeError:
					pass
			else:
				raise AttributeError('could not find attribute %s' % attr)

#
# GIRepository
#
class GIRepository(_GObject):
	_c_class = _gir.GIRepository
	_c_prefix = 'g_irepository_'
	
	def __init__(self):
		_gir.g_type_init()
		self._c_obj = _gir.g_irepository_get_default()
	
class GICallbackInfo(_GIInfoObject):
	_c_class = _gir.GICallbackInfo

class GIRepositoryError(object):
	_c_class = _gir.GIRepositoryError
	
	(
		TYPELIB_NOT_FOUND,
		NAMESPACE_MISMATCH,
		NAMESPACE_VERSION_CONFLICT,
		LIBRARY_NOT_FOUND,
	) = range(4)

class GIRepositoryLoadFlags(object):
	_c_class = _gir.GIRepositoryLoadFlags
	
	LAZY = 1 << 0

#
# GITypelib
#

class GITypelib(_Object):
	# NOTE: GITypelib is not on C-level subclass of _GObject
	# but it is used that way because of calling convenction
	# which states that instance should be first argument in function call
	# so it mimics _GObject
	#
	# responsible for class creation
	_c_class = _gir.GITypelib
	_c_prefix = 'g_typelib_'
	
	def __repr__(self):
		c_name = _gir.g_typelib_get_namespace(self._c_obj)
		py_name = self.convert_c_to_python_object(c_name)
		
		return ''.join((
			'<',
			self.__class__.__name__,
			' "',
			py_name,
			'" (',
			self._c_obj.__class__.__name__,
			' object at ',
			hex(id(self._c_obj)),
			') object at ',
			hex(id(self)),
			'>',
		))
	
	def __getattr__(self, attr):
		c_gir = _gir.g_irepository_get_default()
		c_name = _gir.g_typelib_get_namespace(self._c_obj)
		c_attr = _gir.gchar_p(attr)
		c_info = _gir.g_irepository_find_by_name(c_gir, c_name, c_attr)
		
		c_info_type = _gir.info_get_type(c_info)
		c_casted_info = ctypes.cast(c_info, ctypes.POINTER(c_info_type))
		
		py_info = self.convert_c_to_python_object(c_casted_info)
		return py_info

class GTypelibBlobType(object):
	_c_class = _gir.GTypelibBlobType
	
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

#
# GIBaseInfo
#
class GIBaseInfo(_GIInfoObject):
	_c_class = _gir.GIBaseInfo
	_c_prefix = 'g_base_info_'

class GIAttributeIter(_GIInfoObject):
	_c_class = _gir.GIAttributeIter
	_c_prefix = None

class GIInfoType(object):
	_c_class = _gir.GIInfoType
	
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
class GICallableInfo(GIBaseInfo):
	_c_class = _gir.GICallableInfo
	_c_prefix = 'g_callable_info_'
	
	def __call__(self, *args, **kwargs):
		raise NotImplementedError('')

#
# GIFunctionInfo
#
class GIFunctionInfo(GICallableInfo):
	_c_class = _gir.GIFunctionInfo
	_c_prefix = 'g_function_info_'
	
	def __call__(self, *args, **kwargs):
		c_obj = self._c_obj
		c_in_args = _gir.GIArgument()
		c_out_args = _gir.GIArgument()
		c_return_value = _gir.GIArgument()
		
		_gir.g_function_info_invoke(
			c_obj,
			ctypes.pointer(c_in_args),
			0,
			ctypes.pointer(c_out_args),
			0,
			ctypes.pointer(c_return_value),
			None
		)

class GInvokeError(object):
	_c_class = _gir.GInvokeError
	
	(
		FAILED,
		SYMBOL_NOT_FOUND,
		ARGUMENT_MISMATCH
	) = range(3)

class GIFunctionInfoFlags(object):
	_c_class = _gir.GIFunctionInfoFlags
	
	IS_METHOD = 1 << 0
	IS_CONSTRUCTOR = 1 << 1
	IS_GETTER = 1 << 2
	IS_SETTER = 1 << 3
	WRAPS_VFUNC = 1 << 4
	THROWS = 1 << 5

#
# GISignalInfo
#
class GISignalInfo(GICallableInfo):
	_c_class = _gir.GISignalInfo
	_c_prefix = 'g_signal_info_'

#
# GIVFuncInfo
#
class GIVFuncInfo(GICallableInfo):
	_c_class = _gir.GIVFuncInfo
	_c_prefix = 'g_vfunc_info_'

class GIVFuncInfoFlags(object):
	_c_class = _gir.GIVFuncInfoFlags
	
	MUST_CHAIN_UP = 1 << 0
	MUST_OVERRIDE = 1 << 1
	MUST_NOT_OVERRIDE = 1 << 2

#
# GIRegisteredTypeInfo
#
class GIRegisteredTypeInfo(GIBaseInfo):
	_c_class = _gir.GIRegisteredTypeInfo
	_c_prefix = 'g_registered_type_info_'

#
# GIEnumInfo
#
class GIEnumInfo(GIRegisteredTypeInfo):
	_c_class = _gir.GIEnumInfo
	_c_prefix = 'g_enum_info_'

class GIValueInfo(GIBaseInfo):
	_c_class = _gir.GIValueInfo
	_c_prefix = 'g_value_info_'

#
# GIInterfaceInfo
#
class GIInterfaceInfo(GIRegisteredTypeInfo):
	_c_class = _gir.GIInterfaceInfo
	_c_prefix = 'g_interface_info_'

#
# GIObjectInfo
#
class GIObjectInfo(GIRegisteredTypeInfo):
	_c_class = _gir.GIObjectInfo
	_c_prefix = 'g_object_info_'
	
#
# GIStructInfo
#
class GIStructInfo(GIRegisteredTypeInfo):
	_c_class = _gir.GIStructInfo
	_c_prefix = 'g_struct_info_'

#
# GIUnionInfo
#
class GIUnionInfo(GIRegisteredTypeInfo):
	_c_class = _gir.GIUnionInfo
	_c_prefix = 'g_union_info_'

#
# GIArgInfo
#
class GIArgInfo(GIBaseInfo):
	_c_class = _gir.GIArgInfo
	_c_prefix = 'g_arg_info_'

class GIDirection(object):
	_c_class = _gir.GIDirection
	
	(
		IN,
		OUT,
		INOUT,
	) = range(3)

class GIScopeType(object):
	_c_class = _gir.GIScopeType
	
	(
		INVALID,
		CALL,
		ASYNC,
		NOTIFIED,
	) = range(4)

class GITransfer(object):
	_c_class = _gir.GITransfer
	
	(
		NOTHING,
		CONTAINER,
		EVERYTHING,
	) = range(3)

#
# GIArgument
#
class GIArgument(_Object):
	_c_class = _gir.GIArgument

#
# GIConstantInfo
#
class GIConstantInfo(GIBaseInfo):
	_c_class = _gir.GIConstantInfo
	_c_prefix = 'g_constant_info_'

#
# GIErrorDomainInfo
#
class GIErrorDomainInfo(GIBaseInfo):
	_c_class = _gir.GIErrorDomainInfo
	_c_prefix = 'g_error_domain_info_'

#
# GIFieldInfo
#
class GIFieldInfo(GIBaseInfo):
	_c_class = _gir.GIFieldInfo
	_c_prefix = 'g_field_info_'

class GIFieldInfoFlags(object):
	_c_class = _gir.GIFieldInfoFlags
	
	IS_READABLE = 1 << 0
	IS_WRITABLE = 1 << 1

#
# GIPropertyInfo
#
class GIPropertyInfo(GIBaseInfo):
	_c_class = _gir.GIPropertyInfo
	_c_prefix = 'g_property_info_'
	
#
# GITypeInfo
#
class GITypeInfo(GIBaseInfo):
	_c_class = _gir.GITypeInfo
	_c_prefix = 'g_type_info_'

class GIArrayType(object):
	_c_class = _gir.GIArrayType
	
	(
		C,
		ARRAY,
		PTR_ARRAY,
		BYTE_ARRAY
	) = range(4)

class GITypeTag(object):
	_c_class = _gir.GITypeTag
	
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
