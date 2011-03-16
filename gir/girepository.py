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
	def __init__(self, modulename, moduledoc, ctypelib):
		types.ModuleType.__init__(self, modulename, moduledoc)
		self._ctypelib = ctypelib
		self._attrs = {}
	
	def __del__(self):
		if self._ctypelib:
			_girepository.g_typelib_free(self._ctypelib)
	
	def __getattr__(self, attr):
		cnamespace = _girepository.g_typelib_get_namespace(self._ctypelib)
		cattr = _girepository.gchar_p(attr)
		cinfo = _girepository.g_irepository_find_by_name(None, cnamespace, cattr)
		if not cinfo: raise AttributeError('missing attribute "%s"' % attr)
		cinfotype = _girepository.info_get_type(cinfo)
		
		if cinfotype == _girepository.GIFunctionInfo:
			# function
			cfunctioninfo = _girepository.cast(
				cinfo,
				_girepository.POINTER(_girepository.GIFunctionInfo)
			)
			
			return GIFunction(cfunctioninfo)
		elif cinfotype == _girepository.GIObjectInfo:
			# object
			cobjectinfo = _girepository.cast(
				cinfo,
				_girepository.POINTER(_girepository.GIObjectInfo)
			)
			
			# namespace
			cnamespace = _girepository.g_base_info_get_namespace(cinfo)
			namespace = cnamespace.value
			
			nsclsname = '%s.%s'	% (namespace, attr)
			
			try:
				class_ = _clases[nsclsname]
			except KeyError:
				# parent
				cobjectinfo_parent = _girepository.g_object_info_get_parent(cobjectinfo)
				cinfo_parent = _girepository.cast(
					cobjectinfo_parent,
					_girepository.POINTER(_girepository.GIBaseInfo)
				)
				
				# parent namespace
				cinfo_parent_namespace = _girepository.g_base_info_get_namespace(cinfo_parent)
				info_parent_namespace = cinfo_parent_namespace.value
				
				# parent name
				cinfo_parent_name = _girepository.g_base_info_get_name(cinfo_parent)
				info_parent_name = cinfo_parent_name.value
				
				if namespace == info_parent_namespace and attr == info_parent_name:
					clsbases = [GIObject]
				else:
					# bases = [parent] + interfaces
					clsbases = []
					
					# parent
					module_parent = _modules[info_parent_namespace]
					clsbases.append(module_parent.__getattr__(info_parent_name))
					
					# interfaces
					cobjectinfo_n_interfaces = _girepository.g_object_info_get_n_interfaces(cobjectinfo)
					objectinfo_n_interfaces = cobjectinfo_n_interfaces.value
					
					for i in range(objectinfo_n_interfaces):
						# interface
						cobjectinfo_interface = _girepository.g_object_info_get_interface(cobjectinfo, _girepository.gint(i))
						cinfo_interface = _girepository.cast(
							cobjectinfo_interface,
							_girepository.POINTER(_girepository.GIBaseInfo)
						)
						
						# interface namespace
						cinfo_interface_namespace = _girepository.g_base_info_get_namespace(cinfo_interface)
						info_interface_namespace = cinfo_interface_namespace.value
						
						# interface name
						cinfo_interface_name = _girepository.g_base_info_get_name(cinfo_interface)
						info_interface_name = cinfo_interface_name.value
						
						module_interface = _modules[info_interface_namespace]
						interface = module_interface.__getattr__(info_interface_name)
						clsbases.append(interface)
				
				# class struct
				cobjectinfo_class_struct = _girepository.g_object_info_get_class_struct(cobjectinfo)
				
				# create class
				clsname = attr
				mrobases = _mro(clsbases)
				clsbases = [clsbase for clsbase in mrobases if clsbase in clsbases]
				clsdict = {}
				clsdict['_cinfo'] = cobjectinfo
				clsdict['_object_info_class_struct'] = cobjectinfo_class_struct
				
				# number of methods
				cobjectinfo_n_methods = _girepository.g_object_info_get_n_methods(cobjectinfo)
				objectinfo_n_methods = cobjectinfo_n_methods.value
				
				# methods
				for i in range(objectinfo_n_methods):
					# method
					cfunctioninfo_method = _girepository.g_object_info_get_method(cobjectinfo, _girepository.gint(i))
					cinfo_method = _girepository.cast(
						cfunctioninfo_method,
						_girepository.POINTER(_girepository.GIBaseInfo)
					)
					
					# method name
					cinfo_method_name = _girepository.g_base_info_get_name(cinfo_method)
					info_method_name = cinfo_method_name.value
					
					# attach method to class dict
					function = GIFunction(cfunctioninfo_method)
					method = lambda self, *args, **kwargs: function(self, *args, **kwargs)
					clsdict[info_method_name] = method
					
					# check if constructor
					cfunctioninfo_flags = _girepository.g_function_info_get_flags(cfunctioninfo_method)
					
					if cfunctioninfo_flags.value == _girepository.GI_FUNCTION_IS_CONSTRUCTOR.value:
						clsdict['_constructor'] = method
				
				# new class
				class_ = type(clsname, clsbases, clsdict)
				class_.__module__ = self
				_clases[nsclsname] = class_
			
			return class_
		elif cinfotype == _girepository.GIInterfaceInfo:
			# interface
			cinterfaceinfo = _girepository.cast(
				cinfo,
				_girepository.POINTER(_girepository.GIInterfaceInfo)
			)
			
			# namespace
			cnamespace = _girepository.g_base_info_get_namespace(cinfo)
			namespace = cnamespace.value
			
			nsclsname = '%s.%s'	% (namespace, attr)
			
			try:
				class_ = _clases[nsclsname]
			except KeyError:
				# interface bases
				clsbases = []
				
				# number of prerequisites
				cinterfaceinfo_n_prerequisites = _girepository.g_interface_info_get_n_prerequisites(cinterfaceinfo)
				interfaceinfo_n_prerequisites = cinterfaceinfo_n_prerequisites.value
				
				# prerequisites
				if interfaceinfo_n_prerequisites:
					# if any prerequisite
					for i in range(interfaceinfo_n_prerequisites):
						# prerequisite
						cinfo_prerequisite = _girepository.g_interface_info_get_prerequisite(cinterfaceinfo, _girepository.gint(i))
						
						# prerequisite namespace
						cinfo_prerequisite_namespace = _girepository.g_base_info_get_namespace(cinfo_prerequisite)
						info_prerequisite_namespace = cinfo_prerequisite_namespace.value
						
						# prerequisite name
						cinfo_prerequisite_name = _girepository.g_base_info_get_name(cinfo_prerequisite)
						info_prerequisite_name = cinfo_prerequisite_name.value
						
						module_prerequisite = _modules[info_prerequisite_namespace]
						prerequisite = module_prerequisite.__getattr__(info_prerequisite_name)
						clsbases.append(prerequisite)
				else:
					# other, base class is GIInterface
					clsbases.append(GIInterface)
				
				# create class
				clsname = attr
				mrobases = _mro(clsbases)
				clsbases = [clsbase for clsbase in mrobases if clsbase in clsbases]
				clsdict = {'_cinfo': cinterfaceinfo}
				class_ = type(clsname, clsbases, clsdict)
				class_.__module__ = self
				_clases[nsclsname] = class_
			
			return class_
		else:
			raise GIError('unknown info type "%s"' % _girepository.info_get_type_name(cinfo))

########################################################################

class GIBase(object):
	def __init__(self, _base_info):
		self._base_info = _base_info

class GICallable(GIBase):
	def __init__(self, _callable_info):
		_base_info = _girepository.cast(_callable_info, _girepository.POINTER(_girepository.GIBaseInfo))
		GIBase.__init__(self, _base_info)
		self._callable_info = _callable_info

class GIFunction(GICallable):
	def __init__(self, _function_info):
		_callable_info = _girepository.cast(_function_info, _girepository.POINTER(_girepository.GICallableInfo))
		GICallable.__init__(self, _callable_info)
		self._function_info = _function_info
	
	def __call__(self, *args, **kwargs):
		cinfo = self._cinfo
		cinargs = None
		cninargs = 0
		coutargs = None
		cnoutargs = 0
		creturn = _girepository.GIArgument()
		cerror = _girepository.cast(
			_girepository.gpointer(),
			_girepository.POINTER(
				_girepository.GError
			)
		)
		
		# print(_girepository.g_function_info_get_symbol(cinfo).value)
		
		cresult = _girepository.g_function_info_invoke(
			cinfo,
			cinargs,
			cninargs,
			coutargs,
			cnoutargs,
			creturn,
			cerror,
		)

class GISignal(GICallable):
	def __init__(self, _signal_info):
		_callable_info = _girepository.cast(_signal_info, _girepository.POINTER(_girepository.GICallableInfo))
		GICallable.__init__(self, _callable_info)
		self._signal_info = _signal_info

class GIVFunc(GICallable):
	def __init__(self, _vfunc_info):
		_callable_info = _girepository.cast(_vfunc_info, _girepository.POINTER(_girepository.GICallableInfo))
		GICallable.__init__(self, _callable_info)
		self._vfunc_info = _vfunc_info

class GIRegisteredType(GIBase):
	def __init__(self, _registered_info):
		_base_info = _girepository.cast(_registered_info, _girepository.POINTER(_girepository.GIBaseInfo))
		GIBase.__init__(self, _base_info)
		self._registered_info = _registered_info

class GIEnum(GIRegisteredType):
	def __init__(self, _enum_info):
		_registered_type_info = _girepository.cast(_enum_info, _girepository.POINTER(_girepository.GIRegisteredTypeInfo))
		GIRegisteredType.__init__(self, _registered_type_info)
		self._enum_info = _enum_info

class GIInterface(GIRegisteredType):
	def __init__(self, _interface_info):
		_registered_type_info = _girepository.cast(_interface_info, _girepository.POINTER(_girepository.GIRegisteredTypeInfo))
		GIRegisteredType.__init__(self, _registered_type_info)
		self._interface_info = _interface_info

class GIObject(GIRegisteredType):
	_class_struct_info = None
	
	def __init__(self, _object_info):
		_registered_type_info = _girepository.cast(_object_info, _girepository.POINTER(_girepository.GIRegisteredTypeInfo))
		GIRegisteredType.__init__(self, _registered_type_info)
		self._object_info = _object_info
		self._instance = None

class GIStruct(GIRegisteredType):
	def __init__(self, _struct_info):
		_registered_type_info = _girepository.cast(_struct_info, _girepository.POINTER(_girepository.GIRegisteredTypeInfo))
		GIRegisteredType.__init__(self, _registered_type_info)
		self._struct_info = _struct_info

class GIUnion(GIRegisteredType):
	def __init__(self, _union_info):
		_registered_type_info = _girepository.cast(_union_info, _girepository.POINTER(_girepository.GIRegisteredTypeInfo))
		GIRegisteredType.__init__(self, _registered_type_info)
		self._union_info = _union_info

class GIArg(GIBase):
	def __init__(self, _arg_info):
		_base_info = _girepository.cast(_arg_info, _girepository.POINTER(_girepository.GIBaseInfo))
		GIBase.__init__(self, _base_info)
		self._arg_info = _arg_info

class GIConstant(GIBase):
	def __init__(self, _constant_info):
		_base_info = _girepository.cast(_constant_info, _girepository.POINTER(_girepository.GIBaseInfo))
		GIBase.__init__(self, _base_info)
		self._constant_info = _constant_info

class GIErrorDomain(GIBase):
	def __init__(self, _error_domain_info):
		_base_info = _girepository.cast(_error_domain_info, _girepository.POINTER(_girepository.GIBaseInfo))
		GIBase.__init__(self, _base_info)
		self._error_domain_info = _error_domain_info

class GIField(GIBase):
	def __init__(self, _field_info):
		_base_info = _girepository.cast(_field_info, _girepository.POINTER(_girepository.GIBaseInfo))
		GIBase.__init__(self, _base_info)
		self._field_info = _field_info

class GIProperty(GIBase):
	def __init__(self, _property_info):
		_base_info = _girepository.cast(_property_info, _girepository.POINTER(_girepository.GIBaseInfo))
		GIBase.__init__(self, _base_info)
		self._property_info = _property_info

class GIType(GIBase):
	def __init__(self, _type_info):
		_base_info = _girepository.cast(_type_info, _girepository.POINTER(_girepository.GIBaseInfo))
		GIBase.__init__(self, _base_info)
		self._type_info = _type_info

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
