import os
import sys
import types
from . import _girepository

# major python version
if sys.version_info[0] == 2:
	PY2, PY3 = True, False
elif sys.version_info[0] == 3:
	PY2, PY3 = False, True

# cache used modules and classes
_girepository_instance = None
_modules = {}
_classes = {}

# cache used for signals/callbacks
# REASON: preserve gc
_cfunctype_cache = {}
_cfunctype_last = 0

class GIError(Exception):
	pass

class GIRepository(object):
	def __new__(cls):
		# default/single instance of GIRepository
		global _girepository_instance
		
		# act as singleton
		if not _girepository_instance:
			_girepository_instance = object.__new__(cls)
			cls.__init__(_girepository_instance)
		
		return _girepository_instance
	
	def __init__(self):
		self._repository = _girepository.g_irepository_get_default()
	
	def __getattr__(self, attr):
		try:
			return self.require(attr, None)
		except GIError:
			raise AttributeError('missing attribute "%s"' % attr)
	
	def require(self, namespace, version=None):
		global _modules
		
		# python compatibility
		if PY2:
			namespace_bytes = namespace
			version_bytes = version if version else None
		elif PY3:
			namespace_bytes = namespace.encode()
			version_bytes = version.encode() if version else None
		
		# prepare function args
		_repository = self._repository
		_namespace = _girepository.gchar_p(namespace_bytes)
		_version = _girepository.gchar_p(version_bytes)
		_flags = _girepository.G_IREPOSITORY_LOAD_FLAG_LAZY
		_error = _girepository.cast(
			_girepository.gpointer(),
			_girepository.POINTER(
				_girepository.GError
			)
		)
		
		# typelib
		_typelib = _girepository.g_irepository_require(_repository, _namespace, _version, _flags, _error)
		
		if not _typelib and _error.contents:
			raise GIError(_error.contents.message.value)
		
		# module
		try:
			module = _modules[namespace]
		except KeyError:
			# new module
			module = GITypelib(namespace, '', _typelib)
			
			# dependencies
			_dependencies = _girepository.g_irepository_get_dependencies(_repository, _namespace)
			
			if _dependencies:
				i = 0
				
				while True:
					# dependency
					_dependency = _dependencies[i]
					
					if _dependency.value:
						dependency_bytes = _dependency.value
						if PY2: dependency = dependency_bytes
						elif PY3: dependency = dependency_bytes.decode()
						
						# require (import) dependency
						namespace_, version_ = dependency.split('-')
						module_ = self.require(namespace_, version_)
					else:
						break
					
					i += 1
			
			_modules[namespace] = module
			setattr(self, namespace, module)
		
		return module

class GITypelib(types.ModuleType):
	def __init__(self, modulename, moduledoc, _typelib):
		types.ModuleType.__init__(self, modulename, moduledoc)
		self._typelib = _typelib
	
	def __del__(self):
		#if self._typelib and _girepository:
		#	_girepository.g_typelib_free(self._typelib)
		pass
	
	def __getattr__(self, attr):
		try:
			return self._wrap(attr)
		except GIError:
			raise AttributeError('missing attribute "%s"' % attr)
	
	def _wrap(self, attr):
		global _girepository_instance
		
		# python compatibility
		if PY2: attr_bytes = attr
		elif PY3: attr_bytes = attr.encode()
		
		# prepare
		_namespace = _girepository.g_typelib_get_namespace(self._typelib)
		namespace_bytes = _namespace.value
		if PY2: namespace = namespace_bytes
		elif PY3: namespace = namespace_bytes.decode()
		
		namespace_classname = '%s.%s'	% (namespace, attr)
		_attr = _girepository.gchar_p(attr_bytes)
		_base_info = _girepository.g_irepository_find_by_name(_girepository_instance._repository, _namespace, _attr)
		if not _base_info: raise GIError('missing attribute "%s"' % attr)
		_info_type = _girepository.g_base_info_get_type(_base_info)
		
		# switch _info_type
		if _info_type.value == _girepository.GI_INFO_TYPE_INVALID.value:
			raise GIError('unknown info type "%s" for %s' % (_info_type.value, attr))
		elif _info_type.value in (
			_girepository.GI_INFO_TYPE_FUNCTION.value,
			_girepository.GI_INFO_TYPE_CALLBACK.value,
		):
			# function/callback
			_function_info = _girepository.cast(_base_info, _girepository.POINTER(_girepository.GIFunctionInfo))
			function = GIFunction(_function_info=_function_info)
			setattr(self, attr, function)
			return function
		elif _info_type.value in (
			_girepository.GI_INFO_TYPE_STRUCT.value,
			_girepository.GI_INFO_TYPE_BOXED.value,
		):
			# struct/boxed
			_struct_info = _girepository.cast(_base_info, _girepository.POINTER(_girepository.GIStructInfo))
			
			# create class
			clsname = namespace_classname
			clsbases = (clsbase for clsbase in _mro([GIStruct]) if clsbase in clsbases)
			clsdict = {}
			clsdict['_struct_info'] = _struct_info
			
			# FIXME: parse fields
			
			# methods
			_struct_info_n_methods = _girepository.g_struct_info_get_n_methods(_struct_info)
			
			for i in range(_struct_info_n_methods.value):
				# method
				_function_info_method = _girepository.g_struct_info_get_method(_struct_info, _girepository.gint(i))
				_base_info_method = _girepository.cast(_function_info_method, _girepository.POINTER(_girepository.GIBaseInfo))
				_base_info_method_name = _girepository.g_base_info_get_name(_base_info_method)
				base_info_method_name_bytes = _base_info_method_name.value
				if PY2: base_info_method_name = base_info_method_name_bytes
				elif PY3: base_info_method_name = base_info_method_name_bytes.decode()
				method = GIFunction(_function_info=_function_info_method)
				clsdict[base_info_method_name] = method
			
			# new class
			class_ = type(clsname, clsbases, clsdict)
			class_.__module__ = self
			_classes[namespace_classname] = class_
			setattr(self, attr, class_)
			return class_
		elif _info_type.value in (
			_girepository.GI_INFO_TYPE_ENUM.value,
			_girepository.GI_INFO_TYPE_FLAGS.value,
		):
			# enum/flags
			_enum_info = _girepository.cast(_base_info, _girepository.POINTER(_girepository.GIEnumInfo))
			
			# class args
			clsname = namespace_classname
			clsbases = (GIEnum,)
			clsdict = {}
			clsdict['_enum_info'] = _enum_info
			
			# values
			_n_values = _girepository.g_enum_info_get_n_values(_enum_info)
			
			for i in range(_n_values.value):
				# value
				_value_info = _girepository.g_enum_info_get_value(_enum_info, _girepository.gint(i))
				_value_info_base_info = _girepository.cast(_value_info, _girepository.POINTER(_girepository.GIBaseInfo))
				_value_info_name = _girepository.g_base_info_get_name(_value_info_base_info)
				value_info_name_bytes = _value_info_name.value
				if PY2: value_info_name = value_info_name_bytes
				elif PY3: value_info_name = value_info_name_bytes.decode()
				_value_info_value = _girepository.g_value_info_get_value(_value_info)
				clsdict[value_info_name] = _value_info_value.value
			
			# create new class
			class_ = type(clsname, clsbases, clsdict)
			class_.__module__ = self
			_classes[namespace_classname] = class_
			setattr(self, attr, class_)
			return class_
		elif _info_type.value == _girepository.GI_INFO_TYPE_OBJECT.value:
			# object
			_object_info = _girepository.cast(_base_info, _girepository.POINTER(_girepository.GIObjectInfo))
			_object_info_parent = _girepository.g_object_info_get_parent(_object_info)
			_base_info_parent = _girepository.cast(_object_info_parent, _girepository.POINTER(_girepository.GIBaseInfo))
			_base_info_parent_namespace = _girepository.g_base_info_get_namespace(_base_info_parent)
			base_info_parent_namespace_bytes = _base_info_parent_namespace.value
			if PY2: base_info_parent_namespace = base_info_parent_namespace_bytes
			elif PY3: base_info_parent_namespace = base_info_parent_namespace_bytes.decode()
			_base_info_parent_name = _girepository.g_base_info_get_name(_base_info_parent)
			base_info_parent_name_bytes = _base_info_parent_name.value
			if PY2: base_info_parent_name = base_info_parent_name_bytes
			elif PY3: base_info_parent_name = base_info_parent_name_bytes.decode()
			
			# class
			clsname = namespace_classname
			clsdict = {}
			clsdict['_object_info'] = _object_info
			
			# bases
			if namespace == base_info_parent_namespace and attr == base_info_parent_name:
				clsbases = [GIObject]
			else:
				# bases = [parent] + interfaces
				clsbases = []
				
				# parent
				module_parent = _modules[base_info_parent_namespace]
				clsbase = getattr(module_parent, base_info_parent_name)
				clsbases.append(clsbase)
				
				# interfaces
				_object_info_n_interfaces = _girepository.g_object_info_get_n_interfaces(_object_info)
				
				for i in range(_object_info_n_interfaces.value):
					# interface
					_object_info_interface = _girepository.g_object_info_get_interface(_object_info, _girepository.gint(i))
					_base_info_interface = _girepository.cast(_object_info_interface, _girepository.POINTER(_girepository.GIBaseInfo))
					
					# interface namespace
					_base_info_interface_namespace = _girepository.g_base_info_get_namespace(_base_info_interface)
					base_info_interface_namespace_bytes = _base_info_interface_namespace.value
					
					if PY2:
						base_info_interface_namespace = base_info_interface_namespace_bytes
					elif PY3:
						base_info_interface_namespace = base_info_interface_namespace_bytes.decode()
					
					# interface name
					_base_info_interface_name = _girepository.g_base_info_get_name(_base_info_interface)
					base_info_interface_name_bytes = _base_info_interface_name.value
					
					if PY2:
						base_info_interface_name = base_info_interface_name_bytes
					elif PY3:
						base_info_interface_name = base_info_interface_name_bytes.decode()
					
					# add interface to clsbasses
					module_interface = _modules[base_info_interface_namespace]
					clsbase = getattr(module_interface, base_info_interface_name)
					clsbases.append(clsbase)
			
			mrobases = _mro(clsbases)
			clsbases = [clsbase for clsbase in mrobases if clsbase in clsbases]
			clsbases = tuple(clsbases)
			
			# FIXME: parse fields
			# FIXME: parse properties
			
			# methods
			_object_info_n_methods = _girepository.g_object_info_get_n_methods(_object_info)
			
			for i in range(_object_info_n_methods.value):
				# method
				_function_info_method = _girepository.g_object_info_get_method(_object_info, _girepository.gint(i))
				_base_info_method = _girepository.cast(_function_info_method, _girepository.POINTER(_girepository.GIBaseInfo))
				
				# method name
				_base_info_method_name = _girepository.g_base_info_get_name(_base_info_method)
				base_info_method_name_bytes = _base_info_method_name.value
				
				if PY2:
					base_info_method_name = base_info_method_name_bytes
				elif PY3:
					base_info_method_name = base_info_method_name_bytes.decode()
				
				# attach method to class dict
				method = GIFunction(_function_info=_function_info_method)
				clsdict[base_info_method_name] = method
			
			# FIXME: parse signals
			# FIXME: parse constant
			
			# HACK: uses direct low-level access to shared library
			if namespace_classname == 'GObject.Object':
				_libgobject = _girepository.libgobject
				
				def connect(instance, detailed_signal, py_handler, *args, **kwargs):
					global _cfunctype_cache
					
					def py_handler_func():
						return_ = py_handler(instance, *args, **kwargs)
						
						try:
							return int(return_)
						except TypeError:
							return 0
					
					def py_closure_notify_func(_data, _closure):
						return 0
					
					# prepare
					_instance = instance._self
					
					if PY2:
						_detailed_signal = _girepository.gchar_p(detailed_signal)
					elif PY3:
						_detailed_signal = _girepository.gchar_p(detailed_signal.encode())
					
					_c_handler = _girepository.GCallback(py_handler_func)
					_data = _girepository.gpointer(0)
					_destroy_data = _girepository.GClosureNotify(py_closure_notify_func)
					_connect_flags = _girepository.gint(0)
					
					# connect
					_handler_id = _libgobject.g_signal_connect_data(
						_instance,
						_detailed_signal,
						_c_handler,
						_data,
						_destroy_data,
						_connect_flags
					)
					
					handler_id = int(_handler_id.value)
					
					# cache
					_cfunctype_cache[(instance, handler_id)] = (_c_handler, _destroy_data)
					
					return handler_id
				
				def disconnect(instance, handler_id):
					global _cfunctype_cache
					_instance = instance._self
					_handler_id = _girepository.gulong(handler_id)
					_libgobject.g_signal_handler_disconnect(_instance, _handler_id)
					del _cfunctype_cache[(instance, handler_id)]
				
				def block(instance, handler_id):
					_instance = instance._self
					_handler_id = _girepository.gulong(handler_id)
					_libgobject.g_signal_handler_block(_instance, _handler_id)
				
				def unblock(instance, handler_id):
					_instance = instance._self
					_handler_id = _girepository.gulong(handler_id)
					_libgobject.g_signal_handler_unblock(_instance, _handler_id)
				
				clsdict['connect'] = connect
				clsdict['disconnect'] = disconnect
				clsdict['block'] = block
				clsdict['unblock'] = unblock
			
			# new class
			class_ = type(clsname, clsbases, clsdict)
			class_.__module__ = self
			_classes[namespace_classname] = class_
			setattr(self, attr, class_)
			return class_
		elif _info_type.value == _girepository.GI_INFO_TYPE_INTERFACE.value:
			# interface
			_interface_info = _girepository.cast(_base_info, _girepository.POINTER(_girepository.GIInterfaceInfo))
			
			# class
			clsname = namespace_classname
			clsbases = []
			clsdict = {}
			clsdict['_interface_info'] = _interface_info
			
			# bases
			_interface_info_n_prerequisites = _girepository.g_interface_info_get_n_prerequisites(_interface_info)
			
			if _interface_info_n_prerequisites.value:
				# if any prerequisite
				for i in range(_interface_info_n_prerequisites.value):
					# prerequisite
					_base_info_prerequisite = _girepository.g_interface_info_get_prerequisite(_interface_info, _girepository.gint(i))
					
					# prerequisite namespace
					_base_info_prerequisite_namespace = _girepository.g_base_info_get_namespace(_base_info_prerequisite)
					base_info_prerequisite_namespace_bytes = _base_info_prerequisite_namespace.value
					
					if PY2:
						base_info_prerequisite_namespace = base_info_prerequisite_namespace_bytes
					elif PY3:
						base_info_prerequisite_namespace = base_info_prerequisite_namespace_bytes.decode()
					
					# prerequisite name
					_base_info_prerequisite_name = _girepository.g_base_info_get_name(_base_info_prerequisite)
					base_info_prerequisite_name_bytes = _base_info_prerequisite_name.value
					
					if PY2:
						base_info_prerequisite_name = base_info_prerequisite_name_bytes
					elif PY3:
						base_info_prerequisite_name = base_info_prerequisite_name_bytes.decode()
					
					# append prerequisite (parent interface) to clsbases
					module_prerequisite = _modules[base_info_prerequisite_namespace]
					clsbase = getattr(module_prerequisite, base_info_prerequisite_name)
					clsbases.append(clsbase)
			else:
				# other, base class is GIInterface
				clsbases.append(GIInterface)
			
			mrobases = _mro(clsbases)
			clsbases = [clsbase for clsbase in mrobases if clsbase in clsbases]
			clsbases = tuple(clsbases)
			
			# FIXME: parse properties
			
			# methods
			_interface_info_n_methods = _girepository.g_interface_info_get_n_methods(_interface_info)
			
			for i in range(_interface_info_n_methods.value):
				# method
				_function_info_method = _girepository.g_interface_info_get_method(_interface_info, _girepository.gint(i))
				_base_info_method = _girepository.cast(_function_info_method, _girepository.POINTER(_girepository.GIBaseInfo))
				
				# method name
				_base_info_method_name = _girepository.g_base_info_get_name(_base_info_method)
				base_info_method_name_bytes = _base_info_method_name.value
				
				if PY2:
					base_info_method_name = base_info_method_name_bytes
				elif PY3:
					base_info_method_name = base_info_method_name_bytes.decode()
				
				# attach method to class dict
				method = GIFunction(_function_info=_function_info_method)
				clsdict[base_info_method_name] = method
			
			# FIXME: parse signals
			# FIXME: parse vfuncs
			# FIXME: parse constants
			
			# create class
			class_ = type(clsname, clsbases, clsdict)
			class_.__module__ = self
			_classes[namespace_classname] = class_
			setattr(self, attr, class_)
			return class_
		elif _info_type.value == _girepository.GI_INFO_TYPE_CONSTANT.value:
			# constant
			_constant_info = _girepository.cast(_base_info, _girepository.POINTER(_girepository.GIConstantInfo))
			_arg = _girepository.GIArgument()
			_transfer = _girepository.GI_TRANSFER_NOTHING
			_type_info = _girepository.g_constant_info_get_type(_constant_info)
			argument = _convert_giargument_to_pyobject_with_typeinfo_transfer(_arg, _type_info, _transfer)
			setattr(self, attr, argument)
			return argument
		elif _info_type.value == _girepository.GI_INFO_TYPE_ERROR_DOMAIN.value:
			# error domain
			raise GIError('unknown info type "%s" for %s' % (_info_type.value, attr))
		elif _info_type.value == _girepository.GI_INFO_TYPE_UNION.value:
			# union
			_union_info = _girepository.cast(_base_info, _girepository.POINTER(_girepository.GIUnionInfo))
			
			# create class
			clsname = namespace_classname
			clsbases = (GIUnion,)
			mrobases = _mro(clsbases)
			clsbases = [clsbase for clsbase in mrobases if clsbase in clsbases]
			clsbases = tuple(clsbases)
			clsdict = {}
			clsdict['_union_info'] = _union_info
			
			# FIXME: parse fields
			
			# methods
			_union_info_n_methods = _girepository.g_union_info_get_n_methods(_union_info)
			
			for i in range(_union_info_n_methods.value):
				# method
				_function_info_method = _girepository.g_union_info_get_method(_union_info, _girepository.gint(i))
				_base_info_method = _girepository.cast(_function_info_method, _girepository.POINTER(_girepository.GIBaseInfo))
				_base_info_method_name = _girepository.g_base_info_get_name(_base_info_method)
				base_info_method_name_bytes = _base_info_method_name.value
				
				if PY2:
					base_info_method_name = base_info_method_name_bytes
				elif PY3:
					base_info_method_name = base_info_method_name_bytes.decode()
				
				method = GIFunction(_function_info=_function_info_method)
				clsdict[base_info_method_name] = method
			
			# new class
			class_ = type(clsname, clsbases, clsdict)
			class_.__module__ = self
			_classes[namespace_classname] = class_
			setattr(self, attr, class_)
			return class_
		elif _info_type.value == _girepository.GI_INFO_TYPE_VALUE.value:
			# value
			raise GIError('unknown info type "%s" for %s' % (_info_type.value, attr))
		elif _info_type.value == _girepository.GI_INFO_TYPE_SIGNAL.value:
			# signal
			raise GIError('unknown info type "%s" for %s' % (_info_type.value, attr))
		elif _info_type.value == _girepository.GI_INFO_TYPE_VFUNC.value:
			# vfunc
			raise GIError('unknown info type "%s" for %s' % (_info_type.value, attr))
		elif _info_type.value == _girepository.GI_INFO_TYPE_PROPERTY.value:
			# property
			raise GIError('unknown info type "%s" for %s' % (_info_type.value, attr))
		elif _info_type.value == _girepository.GI_INFO_TYPE_FIELD.value:
			# field
			raise GIError('unknown info type "%s" for %s' % (_info_type.value, attr))
		elif _info_type.value == _girepository.GI_INFO_TYPE_ARG.value:
			# arg
			raise GIError('unknown info type "%s" for %s' % (_info_type.value, attr))
		elif _info_type.value == _girepository.GI_INFO_TYPE_TYPE.value:
			# type
			raise GIError('unknown info type "%s" for %s' % (_info_type.value, attr))
		elif _info_type.value == _girepository.GI_INFO_TYPE_UNRESOLVED.value:
			# unresolved
			raise GIError('unknown info type "%s" for %s' % (_info_type.value, attr))
		else:
			# error
			raise GIError('unknown info type "%s" for %s' % (_info_type.value, attr))
	
	def _wrap_all(self):
		# repository, namespace
		_repository = _girepository_instance._repository
		_namespace = _girepository.g_typelib_get_namespace(self._typelib)
		
		# infos
		_n_infos = _girepository.g_irepository_get_n_infos(_repository, _namespace)
		
		for i in range(_n_infos.value):
			# info
			_base_info = _girepository.g_irepository_get_info(_repository, _namespace, _girepository.gint(i))
			_name = _girepository.g_base_info_get_name(_base_info)
			name_bytes = _name.value
			
			if PY2:
				name = name_bytes
			elif PY3:
				name = name_bytes.decode()
			
			o = self._wrap(name)

########################################################################

class GIBase(object):
	_base_info = None
	
	def __new__(cls, *args, **kwargs):
		self = super(GIBase, cls).__new__(cls, *args, **kwargs)
		GIBase.__init__(self, *args, **kwargs)
		return self
	
	def __init__(self, *args, **kwargs):
		try:
			_base_info = kwargs.pop('_base_info')
			self._base_info = _base_info
		except KeyError:
			pass
		
		try:
			self._self = kwargs.pop('_self')
		except KeyError:
			self._self = None
	
	def __del__(self):
		#if self._base_info:
		#	_girepository.g_base_info_unref(self._base_info)
		pass

class GICallable(GIBase):
	_callable_info = None
	
	def __init__(self, *args, **kwargs):
		try:
			_callable_info = kwargs.pop('_callable_info')
			_base_info = _girepository.cast(_callable_info, _girepository.POINTER(_girepository.GIBaseInfo))
			GIBase.__init__(self, _base_info=_base_info, *args, **kwargs)
			self._callable_info = _callable_info
		except KeyError:
			GIBase.__init__(self, *args, **kwargs)

class GIFunction(GICallable):
	_function_info = None
	
	def __init__(self, *args, **kwargs):
		try:
			_function_info = kwargs.pop('_function_info')
			_callable_info = _girepository.cast(_function_info, _girepository.POINTER(_girepository.GICallableInfo))
			GICallable.__init__(self, _callable_info=_callable_info, *args, **kwargs)
			self._function_info = _function_info
		except KeyError:
			GICallable.__init__(self, *args, **kwargs)
	
	def __repr__(self):
		_function_info_symbol = _girepository.g_function_info_get_symbol(self._function_info)
		function_info_symbol_bytes = _function_info_symbol.value
		if PY2: function_info_symbol = function_info_symbol_bytes
		elif PY3: function_info_symbol = function_info_symbol_bytes.decode()
		_function_info_name = _girepository.g_base_info_get_name(self._base_info)
		function_info_name_bytes = _function_info_name.value
		if PY2: function_info_name = function_info_name_bytes
		elif PY3: function_info_name = function_info_name_bytes.decode()
		
		return ''.join((
			'<',
			self.__class__.__name__,
			' ',
			function_info_symbol if function_info_symbol else function_info_name,
			' at ',
			hex(id(self)),
			'>',
		))
	
	def __get__(self, obj, type_=None):
		_function_info_flags = _girepository.g_function_info_get_flags(self._function_info)
		_base_info_name = _girepository.g_base_info_get_name(self._base_info)
		base_info_name_bytes = _base_info_name.value
		if PY2: base_info_name = base_info_name_bytes
		elif PY3: base_info_name = base_info_name_bytes.decode()
		
		if isinstance(obj, type_):
			if _function_info_flags.value & _girepository.GI_FUNCTION_IS_METHOD.value:
				func = lambda *args, **kwargs: self(obj._self, *args, _pytype=type_, **kwargs)
			elif _function_info_flags.value & _girepository.GI_FUNCTION_IS_CONSTRUCTOR.value:
				func = lambda cls, *args, **kwargs: self(*args, _pytype=type_, **kwargs)
				if PY2: func.func_name = base_info_name
				elif PY3: func.__name__ = base_info_name
				func = classmethod(func)
			else:
				raise GIError('usupported function info flag "%i"' % _function_info_flags.value)
		else:
			if _function_info_flags.value & _girepository.GI_FUNCTION_IS_METHOD.value:
				func = lambda *args, **kwargs: self(*args, _pytype=type_, **kwargs)
				if PY2: func.func_name = base_info_name
				elif PY3: func.__name__ = base_info_name
			elif _function_info_flags.value & _girepository.GI_FUNCTION_IS_CONSTRUCTOR.value:
				func = lambda cls, *args, **kwargs: self(*args, _pytype=cls, **kwargs)
				if PY2: func.func_name = base_info_name
				elif PY3: func.__name__ = base_info_name
				func = classmethod(func)
			else:
				raise GIError('usupported function info flag "%i"' % _function_info_flags.value)
		
		return func
	
	def __call__(self, *args, **kwargs):
		print('GIFunction.__call__', args, kwargs)
		
		# prepare args for g_function_info_invoke
		_callable_info = self._callable_info
		_function_info = self._function_info
		_function_info_flags = _girepository.g_function_info_get_flags(_function_info)
		_return_type_type_info = _girepository.g_callable_info_get_return_type(_callable_info)
		_return_type_type_tag = _girepository.g_type_info_get_tag(_return_type_type_info)
		_return_transfer = _girepository.g_callable_info_get_caller_owns(_callable_info)
		_may_return_null_type_info = _girepository.g_callable_info_may_return_null(_callable_info)
		
		# prepare in/out args
		_arg_info_ins = []
		_arg_info_outs = []
		_arg_ins = []
		_arg_outs = []
		
		# function info flags?
		if _function_info_flags.value & _girepository.GI_FUNCTION_IS_METHOD.value:
			# preserve instance
			_self_arg = _girepository.GIArgument()
			_self_arg.v_pointer = args[0]
			
			# pop first (instance)
			args = args[1:]
		
		# args
		_n_args = _girepository.g_callable_info_get_n_args(_callable_info)
		
		for i in range(_n_args.value):
			# arg
			_arg_info = _girepository.g_callable_info_get_arg(_callable_info, _girepository.gint(i))
			_direction = _girepository.g_arg_info_get_direction(_arg_info)
			arg = args[i]
			_arg = _convert_pyobject_to_giargument_with_arginfo(arg, _arg_info)
			
			# arg in or out according to direction
			if _direction.value == _girepository.GI_DIRECTION_IN.value:
				_arg_info_ins.append(_arg_info)
				_arg_ins.append(_arg)
			elif _direction.value == _girepository.GI_DIRECTION_OUT.value:
				_arg_info_outs.append(_arg_info)
				_arg_outs.append(_arg)
			elif _direction.value == _girepository.GI_DIRECTION_INOUT.value:
				_arg_info_ins.append(_arg_info)
				_arg_info_outs.append(_arg_info)
				_arg_ins.append(_arg)
				_arg_outs.append(_arg)
		
		# function info flags?
		if _function_info_flags.value & _girepository.GI_FUNCTION_IS_METHOD.value:
			# prepend instance
			_arg_ins[0:0] = [_self_arg]
		
		print('GIFunction.__call__', _arg_info_ins, _arg_info_outs)
		print('GIFunction.__call__', _arg_ins, _arg_outs)
		
		# final preparation of args for g_function_info_invoke
		_inargs = (_girepository.GIArgument * len(_arg_ins))(*_arg_ins)
		_ninargs = _girepository.gint(len(_inargs))
		_outargs = (_girepository.GIArgument * len(_arg_outs))(*_arg_outs)
		_noutargs = _girepository.gint(len(_outargs))
		_retarg = (_girepository.GIArgument * 1)(_girepository.GIArgument())
		_error = _girepository.cast(
			_girepository.gpointer(),
			_girepository.POINTER(
				_girepository.GError
			)
		)
		
		# invoke function
		_result = _girepository.g_function_info_invoke(
			_function_info,
			_inargs,
			_ninargs,
			_outargs,
			_noutargs,
			_retarg,
			_error,
		)
		
		# did error occur?
		if not _result.value:
			# error occured, raise an exception with GError message
			error_message = _error.contents.message.value
			raise GIError(error_message)
		
		# function info flags?
		if _function_info_flags.value == _girepository.GI_FUNCTION_IS_METHOD.value:
			_type_info_return = _girepository.g_callable_info_get_return_type(_callable_info)
			_transfer_return = _girepository.g_callable_info_get_caller_owns(_callable_info)
			obj = _convert_giargument_to_pyobject_with_typeinfo_transfer(_retarg[0], _type_info_return, _transfer_return)
			
			if _arg_outs:
				# return as list
				return_ = [obj]
				
				for _arg, _arg_info in zip(_arg_outs, _arg_info_outs):
					obj_ = _convert_giargument_to_pyobject_with_arginfo(_arg, _arg_info)
					return_.append(obj_)
			else:
				# return as single object
				return_ = obj
		elif _function_info_flags.value == _girepository.GI_FUNCTION_IS_CONSTRUCTOR.value:
			pytype = kwargs.pop('_pytype')
			return_ = pytype(_self=_retarg[0].v_pointer)
		elif _function_info_flags.value == _girepository.GI_FUNCTION_IS_GETTER.value:
			raise GIError('unsupported GIFunctionInfoFlags "%i"' % _function_info_flags.value)
			return_ = None
		elif _function_info_flags.value == _girepository.GI_FUNCTION_IS_SETTER.value:
			raise GIError('unsupported GIFunctionInfoFlags "%i"' % _function_info_flags.value)
			return_ = None
		elif _function_info_flags.value == _girepository.GI_FUNCTION_WRAPS_VFUNC.value:
			raise GIError('unsupported GIFunctionInfoFlags "%i"' % _function_info_flags.value)
			return_ = None
		elif _function_info_flags.value == _girepository.GI_FUNCTION_THROWS.value:
			raise GIError('unsupported GIFunctionInfoFlags "%i"' % _function_info_flags.value)
			return_ = None
		else:
			return_ = _convert_giargument_to_pyobject_with_typeinfo_transfer(_retarg[0], _return_type_type_info, _return_transfer)
		
		return return_

class GISignal(GICallable):
	_signal_info = None
	
	def __init__(self, *args, **kwargs):
		try:
			_signal_info = kwargs.pop('_signal_info')
			_callable_info = _girepository.cast(_signal_info, _girepository.POINTER(_girepository.GICallableInfo))
			GICallable.__init__(self, _callable_info=_callable_info, *args, **kwargs)
			self._signal_info = _signal_info
		except KeyError:
			GICallable.__init__(self, *args, **kwargs)

class GIVFunc(GICallable):
	_vfunc_info = None
	
	def __init__(self, *args, **kwargs):
		try:
			_vfunc_info = kwargs.pop('_vfunc_info')
			_callable_info = _girepository.cast(_vfunc_info, _girepository.POINTER(_girepository.GICallableInfo))
			GICallable.__init__(self, _callable_info=_callable_info, *args, **kwargs)
			self._vfunc_info = _vfunc_info
		except KeyError:
			GICallable.__init__(self, *args, **kwargs)

class GIRegisteredType(GIBase):
	_registered_info = None
	
	def __init__(self, _registered_info=None, *args, **kwargs):
		try:
			_registered_info = kwargs.pop('_registered_info')
			_base_info = _girepository.cast(_registered_info, _girepository.POINTER(_girepository.GIBaseInfo))
			GIBase.__init__(self, _base_info=_base_info, *args, **kwargs)
			self._registered_info = _registered_info
		except KeyError:
			GIBase.__init__(self, *args, **kwargs)
		
		try:
			self._transfer = kwargs.pop('_transfer')
		except KeyError:
			self._transfer = _girepository.GI_TRANSFER_NOTHING

class GIEnum(GIRegisteredType):
	_enum_info = None
	
	def __init__(self, _enum_info=None, *args, **kwargs):
		try:
			_enum_info = kwargs.pop('_enum_info')
			_registered_type_info = _girepository.cast(_enum_info, _girepository.POINTER(_girepository.GIRegisteredTypeInfo))
			GIRegisteredType.__init__(self, _registered_type_info=_registered_type_info, *args, **kwargs)
			self._enum_info = _enum_info
		except KeyError:
			GIRegisteredType.__init__(self, *args, **kwargs)

class GIInterface(GIRegisteredType):
	_interface_info = None
	
	def __init__(self, _interface_info=None, *args, **kwargs):
		try:
			_interface_info = kwargs.pop('_interface_info')
			_registered_type_info = _girepository.cast(_interface_info, _girepository.POINTER(_girepository.GIRegisteredTypeInfo))
			GIRegisteredType.__init__(self, _registered_type_info=_registered_type_info, *args, **kwargs)
			self._interface_info = _interface_info
		except KeyError:
			GIRegisteredType.__init__(self, *args, **kwargs)

class GIObject(GIRegisteredType):
	_object_info = None
	
	def __init__(self, *args, **kwargs):
		try:
			_object_info = kwargs.pop('_object_info')
			_registered_type_info = _girepository.cast(_object_info, _girepository.POINTER(_girepository.GIRegisteredTypeInfo))
			GIRegisteredType.__init__(self, _registered_type_info=_registered_type_info, *args, **kwargs)
			self._object_info = _object_info
		except KeyError:
			GIRegisteredType.__init__(self, *args, **kwargs)

class GIStruct(GIRegisteredType):
	_struct_info = None
	
	def __init__(self, *args, **kwargs):
		try:
			_struct_info = kwargs.pop('_struct_info')
			_registered_type_info = _girepository.cast(_struct_info, _girepository.POINTER(_girepository.GIRegisteredTypeInfo))
			GIRegisteredType.__init__(self, _registered_type_info=_registered_type_info, *args, **kwargs)
			self._struct_info = _struct_info
		except KeyError:
			GIRegisteredType.__init__(self, *args, **kwargs)

class GIUnion(GIRegisteredType):
	_union_info = None
	
	def __init__(self, *args, **kwargs):
		try:
			_union_info = kwargs.pop('_union_info')
			_registered_type_info = _girepository.cast(_union_info, _girepository.POINTER(_girepository.GIRegisteredTypeInfo))
			GIRegisteredType.__init__(self, _registered_type_info=_registered_type_info, *args, **kwargs)
			self._union_info = _union_info
		except KeyError:
			GIRegisteredType.__init__(self, *args, **kwargs)

class GIArg(GIBase):
	_arg_info = None
	
	def __init__(self, *args, **kwargs):
		try:
			_arg_info = kwargs.pop('_arg_info')
			_base_info = _girepository.cast(_arg_info, _girepository.POINTER(_girepository.GIBaseInfo))
			GIBase.__init__(self, _base_info=_base_info, *args, **kwargs)
			self._arg_info = _arg_info
		except KeyError:
			GIBase.__init__(self, *args, **kwargs)

class GIConstant(GIBase):
	_constant_info = None
	
	def __init__(self, *args, **kwargs):
		try:
			_constant_info = kwargs.pop('_constant_info')
			_base_info = _girepository.cast(_constant_info, _girepository.POINTER(_girepository.GIBaseInfo))
			GIBase.__init__(self, _base_info=_base_info, *args, **kwargs)
			self._constant_info = _constant_info
		except KeyError:
			GIBase.__init__(self, *args, **kwargs)

class GIErrorDomain(GIBase):
	_error_domain_info = None
	
	def __init__(self, *args, **kwargs):
		try:
			_error_domain_info = kwargs.pop('_error_domain_info')
			_base_info = _girepository.cast(_error_domain_info, _girepository.POINTER(_girepository.GIBaseInfo))
			GIBase.__init__(self, _base_info=_base_info, *args, **kwargs)
			self._error_domain_info = _error_domain_info
		except KeyError:
			GIBase.__init__(self, *args, **kwargs)

class GIField(GIBase):
	_field_info = None
	
	def __init__(self, *args, **kwargs):
		try:
			_field_info = kwargs.pop('_field_info')
			_base_info = _girepository.cast(_field_info, _girepository.POINTER(_girepository.GIBaseInfo))
			GIBase.__init__(self, _base_info=_base_info, *args, **kwargs)
			self._field_info = _field_info
		except KeyError:
			GIBase.__init__(self, *args, **kwargs)

class GIProperty(GIBase):
	_property_info = None
	
	def __init__(self, *args, **kwargs):
		try:
			_property_info = kwargs.pop('_property_info')
			_base_info = _girepository.cast(_property_info, _girepository.POINTER(_girepository.GIBaseInfo))
			GIBase.__init__(self, _base_info=_base_info, *args, **kwargs)
			self._property_info = _property_info
		except KeyError:
			GIBase.__init__(self, *args, **kwargs)

class GIType(GIBase):
	_type_info = None
	
	def __init__(self, *args, **kwargs):
		try:
			_type_info = kwargs.pop('_type_info')
			_base_info = _girepository.cast(_type_info, _girepository.POINTER(_girepository.GIBaseInfo))
			GIBase.__init__(self, _base_info=_base_info, *args, **kwargs)
			self._type_info = _type_info
		except KeyError:
			GIBase.__init__(self, *args, **kwargs)

########################################################################

def _merge_mro(seqs):
	res = []
	i = 0
	
	while 1:
		nonemptyseqs = [seq for seq in seqs if seq]
		
		if not nonemptyseqs:
			return res
		
		i += 1
		
		for seq in nonemptyseqs:
			cand = seq[0]
			nothead = [s for s in nonemptyseqs if cand in s[1:]]
			
			if nothead:
				cand = None
			else:
				break
		
		if not cand:
			raise GIError("Inconsistent hierarchy")
		
		res.append(cand)
		
		for seq in nonemptyseqs:
			if seq[0] == cand:
				del seq[0]

def _calc_mro(C):
	return _merge_mro([[C]] + [_calc_mro(base) for base in C.__bases__] + [list(C.__bases__)])

def _mro(bases):
	segs = []
	
	for base in bases:
		segs.append(_calc_mro(base))
	
	segs = _merge_mro(segs)
	return tuple(segs)

########################################################################

def _convert_giargument_to_pyobject_with_arginfo(_arg, _arg_info):
	_type_info = _girepository.g_arg_info_get_type(_arg_info)
	_transfer = _girepository.g_arg_info_get_ownership_transfer(_arg_info)
	return _convert_giargument_to_pyobject_with_typeinfo_transfer(_arg, _type_info, _transfer)

def _convert_pyobject_to_giargument_with_arginfo(obj, _arg_info):
	_type_info = _girepository.g_arg_info_get_type(_arg_info)
	_transfer = _girepository.g_arg_info_get_ownership_transfer(_arg_info)
	return _convert_pyobject_to_giargument_with_typeinfo_transfer(obj, _type_info, _transfer)

def _convert_giargument_to_pyobject_with_typeinfo_transfer(_arg, _type_info, _transfer):
	_type_tag = _girepository.g_type_info_get_tag(_type_info)
	obj = None
	
	if _type_tag.value == _girepository.GI_TYPE_TAG_VOID.value:
		_is_pointer = _girepository.g_type_info_is_pointer(_type_info)
		
		if _is_pointer.value:
			obj = _arg.v_pointer
	elif _type_tag.value == _girepository.GI_TYPE_TAG_BOOLEAN.value:
		obj = bool(_arg.v_boolean.value)
	elif _type_tag.value == _girepository.GI_TYPE_TAG_INT8.value:
		obj = int(_arg.v_int8.value)
	elif _type_tag.value == _girepository.GI_TYPE_TAG_UINT8.value:
		obj = int(_arg.v_uint8.value)
	elif _type_tag.value == _girepository.GI_TYPE_TAG_INT16.value:
		obj = int(_arg.v_int16.value)
	elif _type_tag.value == _girepository.GI_TYPE_TAG_UINT16.value:
		obj = int(_arg.v_uint16.value)
	elif _type_tag.value == _girepository.GI_TYPE_TAG_INT32.value:
		obj = int(_arg.v_int32.value)
	elif _type_tag.value == _girepository.GI_TYPE_TAG_UINT32.value:
		obj = int(_arg.v_uint32.value)
	elif _type_tag.value == _girepository.GI_TYPE_TAG_INT64.value:
		obj = int(_arg.v_int64.value)
	elif _type_tag.value == _girepository.GI_TYPE_TAG_UINT64.value:
		obj = int(_arg.v_uint64.value)
	elif _type_tag.value == _girepository.GI_TYPE_TAG_FLOAT.value:
		obj = float(_arg.v_float.value)
	elif _type_tag.value == _girepository.GI_TYPE_TAG_DOUBLE.value:
		obj = float(_arg.v_double.value)
	elif _type_tag.value == _girepository.GI_TYPE_TAG_GTYPE.value:
		obj = int(_arg.v_long.value)
	elif _type_tag.value == _girepository.GI_TYPE_TAG_UTF8.value:
		obj = str(_arg.v_string.value)
	elif _type_tag.value == _girepository.GI_TYPE_TAG_FILENAME.value:
		obj = str(_arg.v_string.value)
	elif _type_tag.value == _girepository.GI_TYPE_TAG_ARRAY.value:
		# array
		if not _arg.v_pointer:
			obj = []
		else:
			_array = cast(_arg.v_pointer, POINTER(_girepository.GArray))
			_param_type_info = _girepository.g_type_info_get_param_type(_type_info, _girepository.gint(0))
			_param_base_info = _girepository.cast(_param_type_info, POINTER(_girepository.GIBaseInfo))
			_param_type_tag = _girepository.g_type_info_get_tag(_param_type_info)
			_param_transfer = _girepository.GI_TRANSFER_NOTHING if _transfer.value == _girepository.GI_TRANSFER_CONTAINER.value else _transfer
			obj = []
			
			for i in range(_array.contents.len):
				is_struct = False
				
				if _param_type_tag.value == _girepository.GI_TYPE_TAG_INTERFACE.value:
					_item_base_info = _girepository.g_type_info_get_interface(_param_type_info)
					_item_interface_info = cast(_item_base_info, POINTER(_girepository.GIInterfaceInfo))
					_item_type_tag = _girepository.g_base_info_get_type(_item_base_info)
					
					if _item_type_tag.value in (
						_girepository.GI_INFO_TYPE_STRUCT.value,
						_girepository.GI_INFO_TYPE_BOXED.value,
					):
						is_struct = True
					
					_girepository.g_base_info_unref(_item_base_info)
				
				if is_struct:
					_item = _girepository.GIArgument()
					_item.v_pointer = _girepository.g_array_index(_array, GIArgument, _girepository.gint(i))
				else:
					_item = _girepository.g_array_index(_array, GIArgument, _girepository.gint(i))
				
				item = _convert_giargument_to_pyobject_with_typeinfo_transfer(_item, _param_type_info, _param_transfer)
				obj.append(item)
			
			_girepository.g_base_info_unref(_param_base_info)
	elif _type_tag.value == _girepository.GI_TYPE_TAG_INTERFACE.value:
		# interface
		_base_info = _girepository.g_type_info_get_interface(_type_info)
		_registered_type_info = _girepository.cast(_base_info, _girepository.POINTER(_girepository.GIRegisteredTypeInfo))
		_struct_info = _girepository.cast(_base_info, _girepository.POINTER(_girepository.GIStructInfo))
		_interface_info = _girepository.cast(_base_info, _girepository.POINTER(_girepository.GIInterfaceInfo))
		_type_tag = _girepository.g_base_info_get_type(_base_info)
		
		if _type_tag.value == _girepository.GI_INFO_TYPE_CALLBACK.value:
			# FIXME: implement
			# obj = lambda *args: None
			raise GIError('unsupported type tag %i' % _type_tag.value)
		elif _type_tag.value in (
			_girepository.GI_INFO_TYPE_BOXED.value,
			_girepository.GI_INFO_TYPE_STRUCT.value,
			_girepository.GI_INFO_TYPE_UNION.value,
		):
			if _arg.v_pointer:
				_type = _girepository.g_registered_type_info_get_g_type(_registered_type_info)
				
				if _type.value == _girepository.G_TYPE_VALUE.value:
					# FIXME: implement
					obj = _convert_gvalue_to_pyobject(_arg.v_pointer, False)
					raise GIError('structure type "%s" is not supported yet' % _girepository.g_type_name(_type).value)
				elif _type.value in (
					_girepository.G_TYPE_BOXED.value,
					_girepository.G_TYPE_POINTER.value,
					_girepository.G_TYPE_NONE.value
				):
					type_ = _convert_gtype_to_pytype(_type)
					obj = type_(_self=_arg.v_pointer, _transfer=_transfer)
				else:
					raise GIError('structure type "%s" is not supported yet' % _girepository.g_type_name(_type).value)
		elif _type_tag.value in (
			_girepository.GI_INFO_TYPE_ENUM.value,
			_girepository.GI_INFO_TYPE_FLAGS.value,
		):
			_type = _girepository.g_registered_type_info_get_g_type(_registered_type_info)
			type_ = _convert_gibaseinfo_to_pytype(_base_info)
			obj = type_(_arg.v_long)
		elif _type_tag.value in (
			_girepository.GI_INFO_TYPE_INTERFACE.value,
			_girepository.GI_INFO_TYPE_OBJECT.value,
		):
			if _arg.v_pointer:
				type_ = _convert_gibaseinfo_to_pytype(_base_info)
				obj = type_(_self=_arg.v_pointer)
			else:
				obj = None
		else:
			raise GIError('unsupported type tag %i' % _type_tag.value)
		
		_girepository.g_base_info_unref(_base_info)
	elif _type_tag.value == _girepository.GI_TYPE_TAG_GLIST.value:
		# glist
		_list = cast(_arg.v_pointer, POINTER(_girepository.GList))
		_param_type_info = _girepository.g_type_info_get_param_type(_type_info, _girepository.gint(0))
		_param_base_info = _girepository.cast(_param_type_info, POINTER(_girepository.GIBaseInfo))
		_param_transfer = _girepository.GI_TRANSFER_NOTHING if _transfer.value == _girepository.GI_TRANSFER_CONTAINER.value else _transfer
		obj = []
		
		while _list:
			_item = _girepository.GIArgument()
			_item.v_pointer = _list.contents.data
			item = _convert_giargument_to_pyobject_with_typeinfo_transfer(_item, _param_type_info, _param_transfer)
			obj.append(item)
			_list = _list.contents.next
		
		_girepository.g_base_info_unref(_param_base_info)
	elif _type_tag.value == _girepository.GI_TYPE_TAG_GSLIST.value:
		# gslist
		_list = cast(_arg.v_pointer, POINTER(_girepository.GSList))
		_param_type_info = _girepository.g_type_info_get_param_type(_type_info, _girepository.gint(0))
		_param_base_info = _girepository.cast(_param_type_info, POINTER(_girepository.GIBaseInfo))
		_param_transfer = _girepository.GI_TRANSFER_NOTHING if _transfer.value == _girepository.GI_TRANSFER_CONTAINER.value else _transfer
		obj = []
		
		while _list:
			_item = _girepository.GIArgument()
			_item.v_pointer = _list.contents.data
			item = _convert_giargument_to_pyobject_with_typeinfo_transfer(_item, _param_type_info, _param_transfer)
			obj.append(item)
			_list = _list.contents.next
		
		_girepository.g_base_info_unref(_param_base_info)
	elif _type_tag.value == _girepository.GI_TYPE_TAG_GHASH.value:
		# ghash
		if not _arg.v_pointer:
			obj = None
		else:
			obj = {}
			_key_type_info = _girepository.g_type_info_get_param_type(_type_info, _girepository.gint(0))
			_key_base_info = _girepository.cast(_key_type_info, POINTER(_girepository.GIBaseInfo))
			_value_type_info = _girepository.g_type_info_get_param_type(_type_info, _girepository.gint(1))
			_value_base_info = _girepository.cast(_value_type_info, POINTER(_girepository.GIBaseInfo))
			_param_transfer = _girepository.GI_TRANSFER_NOTHING if _transfer.value == _girepository.GI_TRANSFER_CONTAINER.value else _transfer
			
			# FIXME: implement hash table iteration
			# ...
			
			_girepository.g_base_info_unref(_key_base_info)
			_girepository.g_base_info_unref(_value_base_info)
	elif _type_tag.value == _girepository.GI_TYPE_TAG_ERROR.value:
		# FIXME: implement
		raise GIError('unsupported type tag %i' % _type_tag.value)
	else:
		raise GIError('unsupported type tag %i' % _type_tag.value)
	
	return obj

def _convert_pyobject_to_giargument_with_typeinfo_transfer(obj, _type_info, _transfer):
	_arg = _girepository.GIArgument()
	_type_tag = _girepository.g_type_info_get_tag(_type_info)
	
	if _type_tag.value == _girepository.GI_TYPE_TAG_VOID.value:
		_arg.v_pointer = obj._self
	elif _type_tag.value == _girepository.GI_TYPE_TAG_BOOLEAN.value:
		_arg.v_boolean = _girepository.gboolean(obj)
	elif _type_tag.value == _girepository.GI_TYPE_TAG_INT8.value:
		_arg.v_int8 = _girepository.gint8(obj)
	elif _type_tag.value == _girepository.GI_TYPE_TAG_UINT8.value:
		_arg.v_uint8 = _girepository.guint8(obj)
	elif _type_tag.value == _girepository.GI_TYPE_TAG_INT16.value:
		_arg.v_int16 = _girepository.gint16(obj)
	elif _type_tag.value == _girepository.GI_TYPE_TAG_UINT16.value:
		_arg.v_uint16 = _girepository.guint16(obj)
	elif _type_tag.value == _girepository.GI_TYPE_TAG_INT32.value:
		_arg.v_int32 = _girepository.gint32(obj)
	elif _type_tag.value == _girepository.GI_TYPE_TAG_UINT32.value:
		_arg.v_uint32 = _girepository.guint32(obj)
	elif _type_tag.value == _girepository.GI_TYPE_TAG_INT64.value:
		_arg.v_int64 = _girepository.gint64(obj)
	elif _type_tag.value == _girepository.GI_TYPE_TAG_UINT64.value:
		_arg.v_uint64 = _girepository.guint64(obj)
	elif _type_tag.value == _girepository.GI_TYPE_TAG_FLOAT.value:
		_arg.v_float = _girepository.gfloat(obj)
	elif _type_tag.value == _girepository.GI_TYPE_TAG_DOUBLE.value:
		_arg.v_double = _girepository.gdouble(obj)
	elif _type_tag.value == _girepository.GI_TYPE_TAG_GTYPE.value:
		_arg.v_long = _girepository.glong(obj)
	elif _type_tag.value == _girepository.GI_TYPE_TAG_UTF8.value:
		if PY2:
			_arg.v_string = _girepository.gchar_p(obj)
		elif PY3:
			obj_bytes = obj.encode()
			_arg.v_string = _girepository.gchar_p(obj_bytes)
	elif _type_tag.value == _girepository.GI_TYPE_TAG_FILENAME.value:
		if PY2:
			_arg.v_string = _girepository.gchar_p(obj)
		elif PY3:
			obj_bytes = obj.encode()
			_arg.v_string = _girepository.gchar_p(obj_bytes)
	elif _type_tag.value == _girepository.GI_TYPE_TAG_ARRAY.value:
		# raise GIError('unsupported type tag %i' % _type_tag.value)
		# FIXME: implement
		pass
	elif _type_tag.value == _girepository.GI_TYPE_TAG_INTERFACE.value:
		_base_info = _girepository.g_type_info_get_interface(_type_info)
		_registered_type_info = _girepository.cast(_base_info, _girepository.POINTER(_girepository.GIRegisteredTypeInfo))
		_info_type = _girepository.g_base_info_get_type(_base_info)
		
		if _info_type.value == _girepository.GI_INFO_TYPE_CALLBACK.value:
			# FIXME: implement
			raise GIError('unsupported info type %i' % _info_type.value)
		elif _info_type.value in (
			_girepository.GI_INFO_TYPE_BOXED.value,
			_girepository.GI_INFO_TYPE_STRUCT.value,
			_girepository.GI_INFO_TYPE_UNION.value,
		):
			if obj is None:
				_arg.v_pointer = _girepository.gpointer(0)
			else:
				_type = _girepository.g_registered_type_info_get_g_type(_registered_type_info)
				
				if _type.value == _girepository.G_TYPE_VALUE.value:
					# FIXME: implement
					raise GIError('unsupported type %i' % _type.value)
				elif _type.value == _girepository.G_TYPE_CLOSURE.value:
					_arg.v_pointer = obj._self
				elif _type.value == _girepository.G_TYPE_BOXED.value:
					# FIXME: implement
					raise GIError('unsupported type %i' % _type.value)
				elif _type.value == _girepository.G_TYPE_VALUE.value:
					# FIXME: implement
					raise GIError('unsupported type %i' % _type.value)
				else:
					raise GIError('unsupported type %i' % _type.value)
		elif _info_type.value in (
			_girepository.GI_INFO_TYPE_ENUM.value,
			_girepository.GI_INFO_TYPE_FLAGS.value,
		):
			_arg.v_int = _girepository.gint(obj)
		elif _info_type.value in (
			_girepository.GI_INFO_TYPE_INTERFACE.value,
			_girepository.GI_INFO_TYPE_OBJECT.value,
		):
			_arg.v_pointer = obj._self
		else:
			raise GIError('unsupported info type %i' % _info_type.value)
	elif _type_tag.value == _girepository.GI_TYPE_TAG_GLIST.value:
		# FIXME: implement
		raise GIError('unsupported type tag %i' % _type_tag.value)
	elif _type_tag.value == _girepository.GI_TYPE_TAG_GSLIST.value:
		# FIXME: implement
		raise GIError('unsupported type tag %i' % _type_tag.value)
	elif _type_tag.value == _girepository.GI_TYPE_TAG_GHASH.value:
		# FIXME: implement
		raise GIError('unsupported type tag %i' % _type_tag.value)
	elif _type_tag.value == _girepository.GI_TYPE_TAG_ERROR.value:
		# FIXME: implement
		raise GIError('unsupported type tag %i' % _type_tag.value)
	else:
		raise GIError('unsupported type tag %i' % _type_tag.value)
	
	return _arg

def _convert_gibaseinfo_to_pytype(_gibaseinfo):
	global _girepository_instance
	_namespace = _girepository.g_base_info_get_namespace(_gibaseinfo)
	namespace_bytes = _namespace.value
	
	if PY2:
		namespace = namespace_bytes
	elif PY3:
		namespace = namespace_bytes.decode()
	
	_name = _girepository.g_base_info_get_name(_gibaseinfo)
	name_bytes = _name.value
	
	if PY2:
		name = name_bytes
	elif PY3:
		name = name_bytes.decode()
	
	girepository = GIRepository()
	gitypelib = getattr(girepository, namespace)
	pytype = getattr(gitypelib, name)
	return pytype
