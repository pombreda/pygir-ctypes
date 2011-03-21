import os
import sys
import types
from . import _girepository

_girepository_instance = None
_modules = {}
_classes = {}

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
		self._attrs = {}
	
	def __getattr__(self, attr):
		try:
			return self.require(attr, None)
		except GIError:
			raise AttributeError('missing attribute "%s"' % attr)
	
	def require(self, namespace, version=None):
		# check if already loaded
		try:
			return self._attrs[namespace]
		except KeyError:
			pass
		
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
		global _modules
		
		if namespace in _modules:
			module = _modules[namespace]
		else:
			# new module
			module = GIModule(namespace, '', _typelib)
			
			# dependencies
			_dependencies = _girepository.g_irepository_get_dependencies(_repository, _namespace)
			
			if _dependencies:
				i = 0
				
				while True:
					# dependency
					_dependency = _dependencies[i]
					
					if _dependency.value:
						# require (import) dependency
						dependency = _dependency.value
						_namespace, _version = dependency.split('-')
						_module = self.require(_namespace, _version)
					else:
						break
					
					i += 1
			
			_modules[namespace] = module
			self._attrs[namespace] = module
		
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
		try:
			return self._wrap(attr)
		except GIError:
			raise AttributeError('missing attribute "%s"' % attr)
	
	def _wrap(self, attr):
		# check if already loaded
		try:
			return self._attrs[attr]
		except KeyError:
			pass
		
		_namespace = _girepository.g_typelib_get_namespace(self._typelib)
		namespace = _namespace.value
		namespace_class_name = '%s.%s'	% (namespace, attr)
		_attr = _girepository.gchar_p(attr)
		_base_info = _girepository.g_irepository_find_by_name(None, _namespace, _attr)
		if not _base_info: raise GIError('missing attribute "%s"' % attr)
		_info_type = _girepository.g_base_info_get_type(_base_info)
		
		if _info_type.value == _girepository.GI_INFO_TYPE_INVALID.value:
			raise GIError('Unsupported info type: %i' % _info_type.value)
		elif _info_type.value == _girepository.GI_INFO_TYPE_FUNCTION.value:
			# function
			_function_info = _girepository.cast(_base_info, _girepository.POINTER(_girepository.GIFunctionInfo))
			function = GIFunction(_function_info=_function_info)
			self._attrs[attr] = function
			return function
		elif _info_type.value == _girepository.GI_INFO_TYPE_CALLBACK.value:
			# callback == function
			_function_info = _girepository.cast(_base_info, _girepository.POINTER(_girepository.GIFunctionInfo))
			function = GIFunction(_function_info=_function_info)
			self._attrs[attr] = function
			return function
		elif _info_type.value == _girepository.GI_INFO_TYPE_STRUCT.value:
			raise GIError('unknown info type "%s" for %s' % (_info_type.value, attr))
		elif _info_type.value == _girepository.GI_INFO_TYPE_BOXED.value:
			raise GIError('unknown info type "%s" for %s' % (_info_type.value, attr))
		elif _info_type.value == _girepository.GI_INFO_TYPE_ENUM.value:
			# enum
			_enum_info = _girepository.cast(_base_info, _girepository.POINTER(_girepository.GIEnumInfo))
			
			# class args
			clsname = attr
			clsbases = (GIEnum,)
			clsdict = {}
			clsdict['_enum_info'] = _enum_info
			
			# n values
			_n_values = _girepository.g_enum_info_get_n_values(_enum_info)
			n_values = _n_values.value
			
			# values
			for i in range(n_values):
				# value
				_value_info = _girepository.g_enum_info_get_value(_enum_info, _girepository.gint(i))
				_value_info_base_info = _girepository.cast(_value_info, _girepository.POINTER(_girepository.GIBaseInfo))
				
				# value name
				_value_info_name = _girepository.g_base_info_get_name(_value_info_base_info)
				value_info_name = _value_info_name.value
				
				# value value
				_value_info_value = _girepository.g_value_info_get_value(_value_info)
				value_info_value = _value_info_value.value
				
				# enum member
				clsdict[value_info_name] = value_info_value
			
			# create new class
			class_ = type(clsname, clsbases, clsdict)
			class_.__module__ = self
			_classes[namespace_class_name] = class_
			self._attrs[attr] = class_
			return class_
		elif _info_type.value == _girepository.GI_INFO_TYPE_FLAGS.value:
			raise GIError('unknown info type "%s" for %s' % (_info_type.value, attr))
		elif _info_type.value == _girepository.GI_INFO_TYPE_OBJECT.value:
			# object
			_object_info = _girepository.cast(_base_info, _girepository.POINTER(_girepository.GIObjectInfo))
			
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
			_classes[namespace_class_name] = class_
			self._attrs[attr] = class_
			
			return class_
		elif _info_type.value == _girepository.GI_INFO_TYPE_INTERFACE.value:
			# interface
			_interface_info = _girepository.cast(_base_info, _girepository.POINTER(_girepository.GIInterfaceInfo))
			
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
			_classes[namespace_class_name] = class_
			self._attrs[attr] = class_
			return class_
		elif _info_type.value == _girepository.GI_INFO_TYPE_CONSTANT.value:
			_constant_info = _girepository.cast(_base_info, _girepository.POINTER(_girepository.GIConstantInfo))
			_constant_info_type_info = _girepository.g_constant_info_get_type(_constant_info)
			_argument = _girepository.GIArgument()
			_size = _girepository.g_constant_info_get_value(_constant_info, _argument)
			argument = _convert_giargument_to_pyobject(_argument, _type_info=_constant_info_type_info)
			self._attrs[attr] = argument
			return argument
		elif _info_type.value == _girepository.GI_INFO_TYPE_ERROR_DOMAIN.value:
			raise GIError('unknown info type "%s" for %s' % (_info_type.value, attr))
		elif _info_type.value == _girepository.GI_INFO_TYPE_UNION.value:
			raise GIError('unknown info type "%s" for %s' % (_info_type.value, attr))
		elif _info_type.value == _girepository.GI_INFO_TYPE_VALUE.value:
			raise GIError('unknown info type "%s" for %s' % (_info_type.value, attr))
		elif _info_type.value == _girepository.GI_INFO_TYPE_SIGNAL.value:
			raise GIError('unknown info type "%s" for %s' % (_info_type.value, attr))
		elif _info_type.value == _girepository.GI_INFO_TYPE_VFUNC.value:
			raise GIError('unknown info type "%s" for %s' % (_info_type.value, attr))
		elif _info_type.value == _girepository.GI_INFO_TYPE_PROPERTY.value:
			raise GIError('unknown info type "%s" for %s' % (_info_type.value, attr))
		elif _info_type.value == _girepository.GI_INFO_TYPE_FIELD.value:
			raise GIError('unknown info type "%s" for %s' % (_info_type.value, attr))
		elif _info_type.value == _girepository.GI_INFO_TYPE_ARG.value:
			raise GIError('unknown info type "%s" for %s' % (_info_type.value, attr))
		elif _info_type.value == _girepository.GI_INFO_TYPE_TYPE.value:
			raise GIError('unknown info type "%s" for %s' % (_info_type.value, attr))
		elif _info_type.value == _girepository.GI_INFO_TYPE_UNRESOLVED.value:
			raise GIError('unknown info type "%s" for %s' % (_info_type.value, attr))
		else:
			raise GIError('unknown info type "%s" for %s' % (_info_type.value, attr))
	
	def _wrap_all(self):
		# repository
		_repository = _girepository_instance._repository
		
		# namespace
		_namespace = _girepository.g_typelib_get_namespace(self._typelib)
		
		# number of infos
		_n_infos = _girepository.g_irepository_get_n_infos(_repository, _namespace)
		n_infos = _n_infos.value
		
		# infos
		for i in range(n_infos):
			# info
			_base_info = _girepository.g_irepository_get_info(_repository, _namespace, _girepository.gint(i))
			_name = _girepository.g_base_info_get_name(_base_info)
			name = _name.value
			o = self._wrap(name)

########################################################################

class GIBase(object):
	_base_info = None
	
	def __init__(self, *args, **kwargs):
		try:
			_base_info = kwargs.pop('_base_info')
			self._base_info = _base_info
		except KeyError:
			pass
	
	def _wrap(self, attr):
		pass
	
	def _wrap_all(self):
		pass
	
class GICallback(GIBase):
	_callback_info = None
	
	def __init__(self, *args, **kwargs):
		try:
			_callback_info = kwargs.pop('_callback_info')
			_base_info = _girepository.cast(_callback_info, _girepository.POINTER(_girepository.GIBaseInfo))
			GIBase.__init__(self, _base_info=_base_info, *args, **kwargs)
			self._callback_info = _callback_info
		except KeyError:
			GIBase.__init__(self, *args, **kwargs)
	
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
		function_info_symbol = _function_info_symbol.value
		
		return ''.join((
			'<',
			self.__class__.__name__,
			' ',
			function_info_symbol,
			' at ',
			hex(id(self)),
			'>',
		))
	
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
		print('GIFunction.__call__:', self, args, kwargs)
		
		# prepare args for g_function_info_invoke
		_callable_info = self._callable_info
		_function_info = self._function_info
		
		# prepare in/out args
		_arg_info_ins = []
		_arg_info_outs = []
		_argument_ins = []
		_argument_outs = []
		argument_ins = []
		argument_outs = []
		
		# number of args
		_n_args = _girepository.g_callable_info_get_n_args(_callable_info)
		n_args = _n_args.value
		
		# args
		for i in range(n_args):
			# arg
			_arg_info = _girepository.g_callable_info_get_arg(_callable_info, _girepository.gint(i))
			
			# direction
			_direction = _girepository.g_arg_info_get_direction(_arg_info)
			
			# transfer
			_transfer = _girepository.g_arg_info_get_ownership_transfer(_arg_info)
			
			# type_info
			_type_info = _girepository.g_arg_info_get_type(_arg_info)
			
			# argument
			arg = args[i]
			_argument = _convert_pyobject_to_giargument(arg, _type_info, _transfer)
			
			# arg in or out according to direction
			if direction.value == _girepository.GI_DIRECTION_IN.value:
				_arg_info_ins.append(_arg_info)
				_argument_ins.append(_argument)
				argument_ins.append(arg)
			elif direction.value == _girepository.GI_DIRECTION_OUT.value:
				_arg_info_outs.append(_arg_info)
				_argument_outs.append(_argument)
				argument_outs.append(arg)
			elif direction.value == _girepository.GI_DIRECTION_INOUT.value:
				_arg_info_ins.append(_arg_info)
				_arg_info_outs.append(_arg_info)
				_argument_ins.append(_argument)
				_argument_outs.append(_argument)
				argument_ins.append(arg)
				argument_outs.append(arg)
		
		print('GIFunction.__call__:', _arg_info_ins, _arg_info_outs)
		print('GIFunction.__call__:', _argument_ins, _argument_outs)
		print('GIFunction.__call__:', argument_ins, argument_outs)
		
		# final preparation of args for g_function_info_invoke
		_inargs = (_girepository.GIArgument * len(_argument_ins))(*_argument_ins)
		_ninargs = _girepository.gint(len(_inargs))
		_outargs = (_girepository.GIArgument * len(_argument_outs))(*_argument_outs)
		_noutargs = _girepository.gint(len(_outargs))
		_returnarg = _girepository.GIArgument()
		_error = _girepository.cast(
			_girepository.gpointer(),
			_girepository.POINTER(
				_girepository.GError
			)
		)
		
		return
		
		# invoke function
		_result = _girepository.g_function_info_invoke(
			_function_info,
			_inargs,
			_ninargs,
			_outargs,
			_noutargs,
			_returnarg,
			_error,
		)
		
		return
		
		# result
		result = _result.value
		
		if not result:
			# error occured, raise an exception
			error_message = _error.contents.message.value
			raise GIError(error_message)
		
		return
		
		#~ # return
		#~ _type_info_return = _girepository.g_callable_info_get_return_type(_callable_info)
		#~ _ret = [_type_info_return] + _arg_info_outs
		#~ _return = [_returnarg] + _argument_outs
		#~ return_ = []
		#~ 
		#~ for _type_info, _argument in zip(_ret, _return):
			#~ 
		#~ 
		#~ return return_ if _argument_outs else (return_[0] if return_ else None)
		
		#~ # return
		#~ _type_info_return = _girepository.g_callable_info_get_return_type(_callable_info)
		#~ _transfer_return = _girepository.g_callable_info_get_caller_owns(_callable_info)
		#~ _return = [(_type_info_return, _transfer_return)]
		#~ return_ = []
		
		# return
		
		
		return return_ if return_ else return_[0]

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
		
		try:
			_instance = kwargs.pop('_instance')
			self._instance = _instance
		except KeyError:
			if self._function_info_constructor:
				return_ = self.__class__._function_info_constructor(_self=self, *args, **kwargs)
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

########################################################################

def _convert_giargument_to_pyobject(_arg, _type_info, _transfer):
	pass

def _convert_pyobject_to_giargument(obj, _type_info, _transfer):
	pass
