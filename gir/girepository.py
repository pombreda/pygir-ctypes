from . import _girepository

class GIError(Exception): pass

class GIModule(object):
	def __init__(self, ctypelib):
		self._ctypelib = ctypelib
		self._attrs = {}
	
	def __del__(self):
		if self._ctypelib:
			_girepository.g_typelib_free(self._ctypelib)
	
	def __getattr__(self, attr):
		cnamespace = _girepository.g_typelib_get_namespace(self._ctypelib)
		cattr = _girepository.gchar_p(attr)
		cinfo = _girepository.g_irepository_find_by_name(None, cnamespace, cattr)
		
		if cinfo:
			cinfotype = _girepository.info_get_type(cinfo)
			
			if cinfotype == _girepository.GIFunctionInfo:
				cfunctioninfo = _girepository.cast(
					cinfo,
					_girepository.POINTER(_girepository.GIFunctionInfo)
				)
				return GIFunction(cfunctioninfo)
			else:
				raise GIError('unknown info type "%s"' % _girepository.name_GIInfoType[cinfotype.value])
		else:
			raise AttributeError('missing attribute "%s"' % attr)

class GIRepository(object):
	_self = None
	_modules = {}
	_clases = {}
	
	def __new__(cls):
		# act as singleton
		if not cls._self:
			cls._self = object.__new__(cls)
			cls.__init__(cls._self)
		
		return cls._self
	
	def __init__(self):
		_girepository.g_type_init()
		crepository = _girepository.g_irepository_get_default()
		self._crepository = crepository
	
	def require(self, namespace, version=None):
		# prepare function args
		crepository = self._crepository
		cnamespace = _girepository.gchar_p(namespace)
		cversion = _girepository.gchar_p(version)
		cflags = _girepository.G_IREPOSITORY_LOAD_FLAG_LAZY
		cerror = _girepository.cast(
			_girepository.gpointer(),
			_girepository.POINTER(
				_girepository.GError
			)
		)
		
		# ctypelib
		ctypelib = _girepository.g_irepository_require(crepository, cnamespace, cversion, cflags, cerror)
		
		if not ctypelib and cerror.contents:
			raise GIError(cerror.contents.message.value)
		
		# if version not present, get default version
		if not version:
			cversion = _girepository.g_irepository_get_version(crepository, cnamespace)
			version = cversion.value
		
		# module
		if (namespace, version) in self._modules:
			module = self._modules[(namespace, version)]
		else:
			module = GIModule(ctypelib)
			self._modules[(namespace, version)] = module
		
		# dependencies
		cdependencies = _girepository.g_irepository_get_dependencies(crepository, cnamespace)
		
		if cdependencies:
			i = 0
			
			while True:
				cdependency = cdependencies[i]
				
				if cdependency.value:
					dependency = cdependency.value
					_namespace, _version = dependency.split('-')
					_module = self.require(_namespace, _version)
				else:
					break
				
				i += 1
		
		return module

########################################################################

class GIBase(object):
	def __init__(self, cinfo):
		self._cinfo = cinfo

class GICallable(GIBase):
	def __init__(self, cinfo):
		GIBase.__init__(self, cinfo)

class GIFunction(GICallable):
	def __init__(self, cinfo):
		GICallable.__init__(self, cinfo)
	
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
	def __init__(self, cinfo):
		GICallable.__init__(self, cinfo)

class GIVFunc(GICallable):
	def __init__(self, cinfo):
		GICallable.__init__(self, cinfo)

class GIRegisteredType(GIBase):
	def __init__(self, cinfo):
		GIBase.__init__(self, cinfo)

class GIEnum(GIRegisteredType):
	def __init__(self, cinfo):
		GIRegisteredType.__init__(self, cinfo)

class GIInterface(GIRegisteredType):
	def __init__(self, cinfo):
		GIRegisteredType.__init__(self, cinfo)

class GIObject(GIRegisteredType):
	def __init__(self, cinfo):
		GIRegisteredType.__init__(self, cinfo)

class GIStruct(GIRegisteredType):
	def __init__(self, cinfo):
		GIRegisteredType.__init__(self, cinfo)

class GIUnion(GIRegisteredType):
	def __init__(self, cinfo):
		GIRegisteredType.__init__(self, cinfo)

class GIArg(GIBase):
	def __init__(self, cinfo):
		GIBase.__init__(self, cinfo)

class GIConstant(GIBase):
	def __init__(self, cinfo):
		GIBase.__init__(self, cinfo)

class GIErrorDomain(GIBase):
	def __init__(self, cinfo):
		GIBase.__init__(self, cinfo)

class GIField(GIBase):
	def __init__(self, cinfo):
		GIBase.__init__(self, cinfo)

class GIProperty(GIBase):
	def __init__(self, cinfo):
		GIBase.__init__(self, cinfo)

class GIType(GIBase):
	def __init__(self, cinfo):
		GIBase.__init__(self, cinfo)
