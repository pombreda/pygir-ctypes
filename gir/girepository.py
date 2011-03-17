import os
import sys
import types
from . import _girepository
_modules = {}
_clases = {}

class GIError(Exception):
	pass

class GIRepository(object):
	_self = None
	
	def __new__(cls):
		# act as singleton
		if not cls._self:
			cls._self = object.__new__(cls)
			cls.__init__(cls._self)
		
		return cls._self
	
	def __init__(self):
		_girepository.g_type_init()
		self._repository = _girepository.g_irepository_get_default()
	
	def require(self, namespace, version=None):
		# prepare function args
		_repository = self._repository
		_namespace = _girepository.gchar_p(namespace)
		_version = _girepository.gchar_p(version)
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
		
		# if version not present, get default version
		if not version:
			_version = _girepository.g_irepository_get_version(_repository, _namespace)
			version = _version.value
		
		# module
		if namespace in _modules:
			module = _modules[namespace]
		else:
			module = GIModule(namespace, '', _typelib)
			_modules[namespace] = module
		
		# dependencies
		_dependencies = _girepository.g_irepository_get_dependencies(_repository, _namespace)
		
		if _dependencies:
			i = 0
			
			while True:
				_dependency = _dependencies[i]
				
				if _dependency.value:
					dependency = _dependency.value
					_namespace, _version = dependency.split('-')
					_module = self.require(_namespace, _version)
				else:
					break
				
				i += 1
		
		return module

class GIModule(types.ModuleType):
	def __init__(self, modulename, moduledoc, _typelib):
		types.ModuleType.__init__(self, modulename, moduledoc)
		self._typelib = _typelib
		self._attrs = {}
	
	def __del__(self):
		if self._typelib:
			_girepository.g_typelib_free(self._typelib)
	
	def __getattr__(self, attr):
		_namespace = _girepository.g_typelib_get_namespace(self._typelib)
		_attr = _girepository.gchar_p(attr)
		_base_info = _girepository.g_irepository_find_by_name(None, _namespace, _attr)
		if not _base_info: raise AttributeError('missing attribute "%s"' % attr)
		_info_type = _girepository.info_get_type(_base_info)
		
		if _info_type == _girepository.GIFunctionInfo:
			# function
			_function_info = _girepository.cast(_base_info, _girepository.POINTER(_girepository.GIFunctionInfo))
			function = GIFunction(_function_info=_function_info)
			return function
		elif _info_type == _girepository.GIObjectInfo:
			# object
			_object_info = _girepository.cast(_base_info, _girepository.POINTER(_girepository.GIObjectInfo))
			
			# namespace
			_namespace = _girepository.g_base_info_get_namespace(_base_info)
			namespace = _namespace.value
			
			nsclsname = '%s.%s'	% (namespace, attr)
			
			try:
				class_ = _clases[nsclsname]
			except KeyError:
				# parent
				_object_info_parent = _girepository.g_object_info_get_parent(_object_info)
				_base_info_parent = _girepository.cast(_object_info_parent, _girepository.POINTER(_girepository.GIBaseInfo))
				
				# parent namespace
				_base_info_parent_namespace = _girepository.g_base_info_get_namespace(_base_info_parent)
				base_info_parent_namespace = _base_info_parent_namespace.value
				
				# parent name
				_base_info_parent_name = _girepository.g_base_info_get_name(_base_info_parent)
				base_info_parent_name = _base_info_parent_name.value
				
				if namespace == base_info_parent_namespace and attr == base_info_parent_name:
					clsbases = [GIObject]
				else:
					# bases = [parent] + interfaces
					clsbases = []
					
					# parent
					module_parent = _modules[base_info_parent_namespace]
					clsbases.append(module_parent.__getattr__(base_info_parent_name))
					
					# interfaces
					_object_info_n_interfaces = _girepository.g_object_info_get_n_interfaces(_object_info)
					object_info_n_interfaces = _object_info_n_interfaces.value
					
					for i in range(object_info_n_interfaces):
						# interface
						_object_info_interface = _girepository.g_object_info_get_interface(_object_info, _girepository.gint(i))
						_base_info_interface = _girepository.cast(_object_info_interface, _girepository.POINTER(_girepository.GIBaseInfo))
						
						# interface namespace
						_base_info_interface_namespace = _girepository.g_base_info_get_namespace(_base_info_interface)
						base_info_interface_namespace = _base_info_interface_namespace.value
						
						# interface name
						_base_info_interface_name = _girepository.g_base_info_get_name(_base_info_interface)
						base_info_interface_name = _base_info_interface_name.value
						
						# add interface to clsbasses
						module_interface = _modules[base_info_interface_namespace]
						interface = module_interface.__getattr__(base_info_interface_name)
						clsbases.append(interface)
				
				# class struct
				_struct_info_class = _girepository.g_object_info_get_class_struct(_object_info)
				
				# create class
				clsname = attr
				mrobases = _mro(clsbases)
				clsbases = [clsbase for clsbase in mrobases if clsbase in clsbases]
				clsbases = tuple(clsbases)
				clsdict = {}
				clsdict['_object_info'] = _object_info
				clsdict['_struct_info_class'] = _struct_info_class
				
				# number of methods
				_object_info_n_methods = _girepository.g_object_info_get_n_methods(_object_info)
				object_info_n_methods = _object_info_n_methods.value
				
				# methods
				for i in range(object_info_n_methods):
					# method
					_function_info_method = _girepository.g_object_info_get_method(_object_info, _girepository.gint(i))
					_base_info_method = _girepository.cast(_function_info_method, _girepository.POINTER(_girepository.GIBaseInfo))
					
					# method name
					_base_info_method_name = _girepository.g_base_info_get_name(_base_info_method)
					base_info_method_name = _base_info_method_name.value
					
					# attach method to class dict
					method = GIFunction(_function_info=_function_info_method)
					clsdict[base_info_method_name] = method
					
					# check if constructor
					_function_info_flags = _girepository.g_function_info_get_flags(_function_info_method)
					if _function_info_flags.value == _girepository.GI_FUNCTION_IS_CONSTRUCTOR.value:
						clsdict['_function_info_constructor'] = method
				
				# new class
				class_ = type(clsname, clsbases, clsdict)
				class_.__module__ = self
				_clases[nsclsname] = class_
			
			return class_
		elif _info_type == _girepository.GIInterfaceInfo:
			# interface
			_interface_info = _girepository.cast(_base_info, _girepository.POINTER(_girepository.GIInterfaceInfo))
			
			# namespace
			_namespace = _girepository.g_base_info_get_namespace(_base_info)
			namespace = _namespace.value
			
			nsclsname = '%s.%s'	% (namespace, attr)
			
			try:
				class_ = _clases[nsclsname]
			except KeyError:
				# interface bases
				clsbases = []
				
				# number of prerequisites
				_interface_info_n_prerequisites = _girepository.g_interface_info_get_n_prerequisites(_interface_info)
				interface_info_n_prerequisites = _interface_info_n_prerequisites.value
				
				# prerequisites
				if interface_info_n_prerequisites:
					# if any prerequisite
					for i in range(interface_info_n_prerequisites):
						# prerequisite
						_base_info_prerequisite = _girepository.g_interface_info_get_prerequisite(_interface_info, _girepository.gint(i))
						
						# prerequisite namespace
						_base_info_prerequisite_namespace = _girepository.g_base_info_get_namespace(_base_info_prerequisite)
						base_info_prerequisite_namespace = _base_info_prerequisite_namespace.value
						
						# prerequisite name
						_base_info_prerequisite_name = _girepository.g_base_info_get_name(_base_info_prerequisite)
						base_info_prerequisite_name = _base_info_prerequisite_name.value
						
						# append prerequisite (parent interface) to clsbases
						module_prerequisite = _modules[base_info_prerequisite_namespace]
						prerequisite = module_prerequisite.__getattr__(base_info_prerequisite_name)
						clsbases.append(prerequisite)
				else:
					# other, base class is GIInterface
					clsbases.append(GIInterface)
				
				# create class
				clsname = attr
				mrobases = _mro(clsbases)
				clsbases = [clsbase for clsbase in mrobases if clsbase in clsbases]
				clsbases = tuple(clsbases)
				clsdict = {'_interface_info': _interface_info}
				class_ = type(clsname, clsbases, clsdict)
				class_.__module__ = self
				_clases[nsclsname] = class_
			
			return class_
		else:
			raise GIError('unknown info type "%s"' % _girepository.info_get_type_name(_base_info))

########################################################################

class GIBase(object):
	_base_info = None
	
	def __init__(self, *args, **kwargs):
		try:
			_base_info = kwargs.pop('_base_info')
			self._base_info = _base_info
		except KeyError:
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
	
	def __get__(self, obj, type_=None):
		if isinstance(obj, type_):
			func = lambda *args, **kwargs: self(obj, *args, **kwargs)
			_base_info_name = _girepository.g_base_info_get_name(self._base_info)
			base_info_name = _base_info_name.value
			func.func_name = base_info_name
			return func
		else:
			return self
	
	def __call__(self, *args, **kwargs):
		print('*', self, args, kwargs)
		_function_info = self._function_info
		_inargs = None
		_ninargs = _girepository.gint(0)
		_outargs = None
		_noutargs = _girepository.gint(0)
		_return = _girepository.GIArgument()
		_error = _girepository.cast(
			_girepository.gpointer(),
			_girepository.POINTER(
				_girepository.GError
			)
		)
		
		# print(_girepository.g_function_info_get_symbol(cinfo).value)
		
		_result = _girepository.g_function_info_invoke(
			_function_info,
			_inargs,
			_ninargs,
			_outargs,
			_noutargs,
			_return,
			_error,
		)
		
		return _result

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
	_struct_info_class = None
	_function_info_constructor = None
	
	def __init__(self, *args, **kwargs):
		try:
			_object_info = kwargs.pop('_object_info')
			_registered_type_info = _girepository.cast(_object_info, _girepository.POINTER(_girepository.GIRegisteredTypeInfo))
			GIRegisteredType.__init__(self, _registered_type_info=_registered_type_info, *args, **kwargs)
			self._object_info = _object_info
		except KeyError:
			GIRegisteredType.__init__(self, *args, **kwargs)
		
		try:
			_struct_info_class = kwargs.pop('_struct_info_class')
			self._struct_info_class = _struct_info_class
		except KeyError:
			pass
		
		try:
			_function_info_constructor = kwargs.pop('_function_info_constructor')
			self._function_info_constructor = _function_info_constructor
		except KeyError:
			pass
		
		if self._function_info_constructor:
			self._instance = self._function_info_constructor(*args, **kwargs)
		else:
			self._instance = None

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
	return _merge_mro([[C]] + map(_calc_mro, C.__bases__) + [list(C.__bases__)])

def _mro(bases):
	segs = []
	
	for base in bases:
		segs.append(_calc_mro(base))
	
	segs = _merge_mro(segs)
	return tuple(segs)
