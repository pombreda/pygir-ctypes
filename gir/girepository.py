from . import _girepository

class GIError(Exception): pass

class GIObject(object):
	pass

class GIModule(GIObject):
	def __init__(self, ctypelib):
		GIObject.__init__(self)
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
				return GIFunction(cinfo)
			else:
				raise GIError('unknown info type "%s"' % _girepository.name_GIInfoType[cinfotype.value])
		else:
			raise AttributeError('missing attribute "%s"' % attr)

class GIClass(GIObject):
	pass

class GIFunction(GIObject):
	def __init__(self, cinfo):
		GIObject.__init__(self)
		self._cinfo = cinfo
	
	def __call__(self, *args, **kwargs):
		cinfo = _girepository.cast(
			self._cinfo,
			_girepository.POINTER(_girepository.GIFunctionInfo)
		)
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
		
		cresult = _girepository.g_function_info_invoke(
			cinfo,
			cinargs,
			cninargs,
			coutargs,
			cnoutargs,
			creturn,
			cerror,
		)

class GIMethod(GIObject):
	pass

class GIRepository(GIObject):
	_self = None
	_modules = {}
	_clases = {}
	
	def __new__(cls):
		# act as singleton
		if not cls._self:
			cls._self = super(GIObject, cls).__new__(cls)
			cls.__init__(cls._self)
		
		return cls._self
	
	def __init__(self):
		GIObject.__init__(self)
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
