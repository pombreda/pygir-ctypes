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
			
			# number of infos
			_n_infos = _girepository.g_irepository_get_n_infos(_repository, _namespace)
			n_infos = _n_infos.value
			
			# infos
			for i in range(n_infos):
				# info
				_base_info = _girepository.g_irepository_get_info(_repository, _namespace, _girepository.gint(i))
				_name = _girepository.g_base_info_get_name(_base_info)
				name = _name.value
				_info_type = _girepository.g_base_info_get_type(_base_info)
				
				if _info_type.value == _girepository.GI_INFO_TYPE_INVALID.value:
					raise GIError('Unsupported info type: %i' % _info_type.value)
				elif _info_type.value == _girepository.GI_INFO_TYPE_FUNCTION.value:
					_function_info = _girepository.cast(_base_info, _girepository.POINTER(_girepository.GIFunctionInfo))
					function = GIFunction(_function_info=_function_info)
					setattr(module, name, function)
				elif _info_type.value == _girepository.GI_INFO_TYPE_CALLBACK.value:
					_callback_info = _girepository.cast(_base_info, _girepository.POINTER(_girepository.GICallbackInfo))
					callback = GICallback(_callback_info=_callback_info)
					setattr(module, name, callback)
				elif _info_type.value == _girepository.GI_INFO_TYPE_STRUCT.value:
					_struct_info = _girepository.cast(_base_info, _girepository.POINTER(_girepository.GIStructInfo))
					struct = GIStruct(_struct_info=_struct_info)
					setattr(module, name, struct)
				elif _info_type.value == _girepository.GI_INFO_TYPE_BOXED.value:
					_struct_info = _girepository.cast(_base_info, _girepository.POINTER(_girepository.GIStructInfo))
					struct = GIStruct(_struct_info=_struct_info)
					setattr(module, name, struct)
				elif _info_type.value == _girepository.GI_INFO_TYPE_ENUM.value:
					_enum_info = _girepository.cast(_base_info, _girepository.POINTER(_girepository.GIEnumInfo))
					enum = GIEnum(_enum_info=_enum_info)
					setattr(module, name, enum)
				elif _info_type.value == _girepository.GI_INFO_TYPE_FLAGS.value:
					_enum_info = _girepository.cast(_base_info, _girepository.POINTER(_girepository.GIEnumInfo))
					enum = GIEnum(_enum_info=_enum_info)
					setattr(module, name, enum)
				elif _info_type.value == _girepository.GI_INFO_TYPE_OBJECT.value:
					pass
				elif _info_type.value == _girepository.GI_INFO_TYPE_INTERFACE.value:
					pass
				elif _info_type.value == _girepository.GI_INFO_TYPE_CONSTANT.value:
					pass
				elif _info_type.value == _girepository.GI_INFO_TYPE_ERROR_DOMAIN.value:
					pass
				elif _info_type.value == _girepository.GI_INFO_TYPE_UNION.value:
					pass
				elif _info_type.value == _girepository.GI_INFO_TYPE_VALUE.value:
					pass
				elif _info_type.value == _girepository.GI_INFO_TYPE_SIGNAL.value:
					pass
				elif _info_type.value == _girepository.GI_INFO_TYPE_VFUNC.value:
					pass
				elif _info_type.value == _girepository.GI_INFO_TYPE_PROPERTY.value:
					pass
				elif _info_type.value == _girepository.GI_INFO_TYPE_FIELD.value:
					pass
				elif _info_type.value == _girepository.GI_INFO_TYPE_ARG.value:
					pass
				elif _info_type.value == _girepository.GI_INFO_TYPE_TYPE.value:
					pass
				elif _info_type.value == _girepository.GI_INFO_TYPE_UNRESOLVED.value:
					pass
			
			# import module (hack)
			_modules[namespace] = module
		
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
		elif _info_type == _girepository.GIEnumInfo:
			# enum
			_enum_info = _girepository.cast(_base_info, _girepository.POINTER(_girepository.GIEnumInfo))
			
			# namespace
			_namespace = _girepository.g_base_info_get_namespace(_base_info)
			namespace = _namespace.value
			
			nsclsname = '%s.%s'	% (namespace, attr)
			
			try:
				class_ = _clases[nsclsname]
			except KeyError:
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
			_direction = _girepository.g_arg_info_get_direction(_arg_info)
			direction = _direction.value
			
			# argument
			arg = args[i]
			_argument = _pyobject_to_giargument(arg, _arg_info)
			
			# arg in or out according to direction
			if direction == _girepository.GI_DIRECTION_IN.value:
				_arg_info_ins.append(_arg_info)
				_argument_ins.append(_argument)
				argument_ins.append(arg)
			elif direction == _girepository.GI_DIRECTION_OUT.value:
				_arg_info_outs.append(_arg_info)
				_argument_outs.append(_argument)
				argument_outs.append(arg)
			elif direction == _girepository.GI_DIRECTION_INOUT.value:
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
		_outargs = None
		_noutargs = _girepository.gint(0)
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
		
		# return
		_type_info_return = _girepository.g_callable_info_get_return_type(_callable_info)
		_ret = [_type_info_return] + _arg_info_outs
		_return = [_returnarg] + _argument_outs
		return_ = []
		
		for _type_info, _argument in zip(_ret, _return):
			_type_tag = _girepository.g_type_info_get_tag(_type_info)
			
			if _type_tag.value == _girepository.GI_TYPE_TAG_VOID.value:
				r = None
			elif _type_tag.value == _girepository.GI_TYPE_TAG_BOOLEAN.value:
				r = bool(_argument.v_boolean.value)
			elif _type_tag.value == _girepository.GI_TYPE_TAG_INT8.value:
				r = int(_argument.v_int8.value)
			elif _type_tag.value == _girepository.GI_TYPE_TAG_UINT8.value:
				r = int(_argument.v_uint8.value)
			elif _type_tag.value == _girepository.GI_TYPE_TAG_INT16.value:
				r = int(_argument.v_int16.value)
			elif _type_tag.value == _girepository.GI_TYPE_TAG_UINT16.value:
				r = int(_argument.v_uint16.value)
			elif _type_tag.value == _girepository.GI_TYPE_TAG_INT32.value:
				r = int(_argument.v_int32.value)
			elif _type_tag.value == _girepository.GI_TYPE_TAG_UINT32.value:
				r = int(_argument.v_uint32.value)
			elif _type_tag.value == _girepository.GI_TYPE_TAG_INT64.value:
				r = int(_argument.v_int64.value)
			elif _type_tag.value == _girepository.GI_TYPE_TAG_UINT64.value:
				r = int(_argument.v_uint64.value)
			elif _type_tag.value == _girepository.GI_TYPE_TAG_FLOAT.value:
				r = float(_argument.v_float.value)
			elif _type_tag.value == _girepository.GI_TYPE_TAG_DOUBLE.value:
				r = float(_argument.v_double.value)
			elif _type_tag.value == _girepository.GI_TYPE_TAG_GTYPE.value:
				r = int(_argument.v_size.value)
			elif _type_tag.value == _girepository.GI_TYPE_TAG_UTF8.value:
				r = str(_argument.v_string.value)
			elif _type_tag.value == _girepository.GI_TYPE_TAG_FILENAME.value:
				r = str(_argument.v_string.value)
			elif _type_tag.value == _girepository.GI_TYPE_TAG_ARRAY.value:
				# raise GIError('Unsupported type tag: %i' % _type_tag.value)
				r = []
			elif _type_tag.value == _girepository.GI_TYPE_TAG_INTERFACE.value:
				_base_info_interface = _girepository.g_type_info_get_interface(_type_info)
				_base_info_info_type = _girepository.g_base_info_get_type(_base_info_interface)
				_base_info_interface_namespace = _girepository.g_base_info_get_namespace(_base_info_interface)
				base_info_interface_namespace = _base_info_interface_namespace.value
				_base_info_interface_name = _girepository.g_base_info_get_name(_base_info_interface)
				base_info_interface_name = _base_info_interface_name.value
				nsclsname = '%s.%s' % (base_info_interface_namespace, base_info_interface_name)
				
				if _base_info_info_type.value == _girepository.GI_INFO_TYPE_STRUCT.value:
					raise GIError('Unsupported interface type: %i' % _base_info_info_type.value)
				elif _base_info_info_type.value == _girepository.GI_INFO_TYPE_ENUM.value:
					_argument.v_int = _girepository.gint(arg)
				elif _base_info_info_type.value == _girepository.GI_INFO_TYPE_OBJECT.value:
					_function_info_flags = _girepository.g_function_info_get_flags(_function_info)
					
					if _function_info_flags.value == _girepository.GI_FUNCTION_IS_CONSTRUCTOR.value:
						r = kwargs.pop('_self')
						r._instance = _argument.v_pointer
					else:
						cls = _classes[nsclsname]
						r = cls(_instance=_argument.v_pointer)
				elif _base_info_info_type.value == _girepository.GI_INFO_TYPE_INTERFACE.value:
					_function_info_flags = _girepository.g_function_info_get_flags(_function_info)
					
					if _function_info_flags.value == _girepository.GI_FUNCTION_IS_CONSTRUCTOR.value:
						r = kwargs.pop('_self')
						r._instance = _argument.v_pointer
					else:
						cls = _classes[nsclsname]
						r = cls(_instance=_argument.v_pointer)
				elif _base_info_info_type.value == _girepository.GI_INFO_TYPE_UNION.value:
					raise GIError('Unsupported interface type: %i' % _base_info_info_type.value)
				else:
					raise GIError('Unsupported interface type: %i' % _base_info_info_type.value)
			elif _type_tag.value == _girepository.GI_TYPE_TAG_GLIST.value:
				raise GIError('Unsupported type tag: %i' % _type_tag.value)
			elif _type_tag.value == _girepository.GI_TYPE_TAG_GSLIST.value:
				raise GIError('Unsupported type tag: %i' % _type_tag.value)
			elif _type_tag.value == _girepository.GI_TYPE_TAG_GHASH.value:
				raise GIError('Unsupported type tag: %i' % _type_tag.value)
			elif _type_tag.value == _girepository.GI_TYPE_TAG_ERROR.value:
				raise GIError('Unsupported type tag: %i' % _type_tag.value)
			else:
				raise GIError('Unsupported type tag: %i' % _type_tag.value)
			
			return_.append(r)
		
		return return_ if _argument_outs else (return_[0] if return_ else None)

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

def _pyobject_to_giargument(arg, _arg_info):
	# direction
	_direction = _girepository.g_arg_info_get_direction(_arg_info)
	direction = _direction.value
	
	# is_return_value
	_is_return_value = _girepository.g_arg_info_is_return_value(_arg_info)
	is_return_value = _is_return_value.value
	
	# is_optional
	_is_optional = _girepository.g_arg_info_is_optional(_arg_info)
	is_optional = _is_optional.value
	
	# may_be_null
	_may_be_null = _girepository.g_arg_info_may_be_null(_arg_info)
	may_be_null = _may_be_null.value
	
	# transfer
	_transfer = _girepository.g_arg_info_get_ownership_transfer(_arg_info)
	transfer = _transfer.value
	
	# scope_type
	_scope_type = _girepository.g_arg_info_get_scope(_arg_info)
	scope_type = _scope_type.value
	
	# closure
	_closure = _girepository.g_arg_info_get_closure(_arg_info)
	closure = _closure.value
	
	# destroy
	_destroy = _girepository.g_arg_info_get_destroy(_arg_info)
	destroy = _destroy.value
	
	# type_info
	_type_info = _girepository.g_arg_info_get_type(_arg_info)
	
	# is_pointer
	_is_pointer = _girepository.g_type_info_is_pointer(_type_info)
	is_pointer = _is_pointer.value
	
	# type_tag
	_type_tag = _girepository.g_type_info_get_tag(_type_info)
	type_tag = _type_tag.value
	
	# interface, namespace, name
	if type_tag == _girepository.GI_TYPE_TAG_INTERFACE.value:
		_base_info_interface = _girepository.g_type_info_get_interface(_type_info)
		
		_base_info_interface_namespace = _girepository.g_base_info_get_namespace(_base_info_interface)
		base_info_interface_namespace = _base_info_interface_namespace.value
		
		_base_info_interface_name = _girepository.g_base_info_get_name(_base_info_interface)
		base_info_interface_name = _base_info_interface_name.value
	else:
		_base_info_interface = None
		
		_base_info_interface_namespace = None
		base_info_interface_namespace = None
		
		_base_info_interface_name = None
		base_info_interface_name = None
	
	# array_length
	_array_length = _girepository.g_type_info_get_array_length(_type_info)
	array_length = _array_length.value
	
	# array_fixed_size
	_array_fixed_size = _girepository.g_type_info_get_array_fixed_size(_type_info)
	array_fixed_size = _array_fixed_size.value
	
	# is_zero_terminated
	_is_zero_terminated = _girepository.g_type_info_is_zero_terminated(_type_info)
	is_zero_terminated = _is_zero_terminated.value
	
	# array_type
	if type_tag == _girepository.GI_TYPE_TAG_ARRAY.value:
		_array_type = _girepository.g_type_info_get_array_type(_type_info)
		array_type = _array_type.value
	else:
		_array_type = None
		array_type = None
	
	# debug
	print(
		'_pyobject_to_giargument:',
		_arg_info,
		direction,
		is_return_value,
		is_optional,
		may_be_null,
		transfer,
		scope_type,
		closure,
		destroy,
		_type_info,
		is_pointer,
		type_tag,
		_base_info_interface,
		base_info_interface_namespace,
		base_info_interface_name,
		array_length,
		array_fixed_size,
		is_zero_terminated,
		array_type,
	)
	
	# giargument
	_argument = _girepository.GIArgument()
	
	if _type_tag.value == _girepository.GI_TYPE_TAG_VOID.value:
		_argument.v_pointer = None
	elif _type_tag.value == _girepository.GI_TYPE_TAG_BOOLEAN.value:
		_argument.v_boolean = _girepository.gboolean(arg)
	elif _type_tag.value == _girepository.GI_TYPE_TAG_INT8.value:
		_argument.v_int8 = _girepository.gint8(arg)
	elif _type_tag.value == _girepository.GI_TYPE_TAG_UINT8.value:
		_argument.v_uint8 = _girepository.guint8(arg)
	elif _type_tag.value == _girepository.GI_TYPE_TAG_INT16.value:
		_argument.v_int16 = _girepository.gint16(arg)
	elif _type_tag.value == _girepository.GI_TYPE_TAG_UINT16.value:
		_argument.v_uint16 = _girepository.guint16(arg)
	elif _type_tag.value == _girepository.GI_TYPE_TAG_INT32.value:
		_argument.v_int32 = _girepository.gint32(arg)
	elif _type_tag.value == _girepository.GI_TYPE_TAG_UINT32.value:
		_argument.v_uint32 = _girepository.guint32(arg)
	elif _type_tag.value == _girepository.GI_TYPE_TAG_INT64.value:
		_argument.v_int64 = _girepository.gint64(arg)
	elif _type_tag.value == _girepository.GI_TYPE_TAG_UINT64.value:
		_argument.v_uint64 = _girepository.guint64(arg)
	elif _type_tag.value == _girepository.GI_TYPE_TAG_FLOAT.value:
		_argument.v_float = _girepository.gfloat(arg)
	elif _type_tag.value == _girepository.GI_TYPE_TAG_DOUBLE.value:
		_argument.v_double = _girepository.gdouble(arg)
	elif _type_tag.value == _girepository.GI_TYPE_TAG_GTYPE.value:
		_argument.v_size = _girepository.gsize(arg)
	elif _type_tag.value == _girepository.GI_TYPE_TAG_UTF8.value:
		_argument.v_string = _girepository.gchar_p(arg.encode())
	elif _type_tag.value == _girepository.GI_TYPE_TAG_FILENAME.value:
		_argument.v_string = _girepository.gchar_p(arg.encode())
	elif _type_tag.value == _girepository.GI_TYPE_TAG_ARRAY.value:
		pass
	elif _type_tag.value == _girepository.GI_TYPE_TAG_INTERFACE.value:
		# interface info type
		_base_info_interface_info_type = _girepository.g_base_info_get_type(_base_info_interface)
		base_info_interface_info_type = _base_info_interface_info_type.value
		
		_registered_type_info_interface = _girepository.cast(_base_info_interface, _girepository.POINTER(_girepository.GIRegisteredTypeInfo))
		
		if base_info_interface_info_type in (
			_girepository.GI_INFO_TYPE_STRUCT.value,
			_girepository.GI_INFO_TYPE_ENUM.value,
			_girepository.GI_INFO_TYPE_OBJECT.value,
			_girepository.GI_INFO_TYPE_INTERFACE.value,
			_girepository.GI_INFO_TYPE_UNION.value,
			_girepository.GI_INFO_TYPE_BOXED.value
		):
			_g_type = _girepository.g_registered_type_info_get_g_type(_registered_type_info_interface)
		elif base_info_info_type == _girepository.GI_INFO_TYPE_VALUE.value:
			_g_type = _girepository.G_TYPE_VALUE
		else:
			_g_type = _girepository.G_TYPE_NONE
		
		if _g_type == _girepository.G_TYPE_VALUE:
			_value = _girepository.GValue()
			
			
	elif _type_tag.value == _girepository.GI_TYPE_TAG_GLIST.value:
		pass
	elif _type_tag.value == _girepository.GI_TYPE_TAG_GSLIST.value:
		pass
	elif _type_tag.value == _girepository.GI_TYPE_TAG_GHASH.value:
		pass
	elif _type_tag.value == _girepository.GI_TYPE_TAG_ERROR.value:
		pass
	else:
		raise GIError('Unsupported type tag: %i' % _type_tag.value)
	
	return _argument

def _giargument_to_pyobject(_argument, _arg_info):
	pass
