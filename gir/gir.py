#
# High-level Python API
#
import _gir

#
# GIRepository
#
class GIRepository(object):
	def __init__(self):
		_gir.g_type_init()
		self._gir = _gir.g_irepository_get_default()

class GICallbackInfo(object):
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
class GIBaseInfo(object):
	def __init__(self):
		pass

class GIAttributeIter(object):
	def __init__(self):
		pass

class GIInfoType(object):
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
class GICallableInfo(object):
	def __init__(self):
		pass

#
# GIFunctionInfo
#
class GIFunctionInfo(object):
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
class GISignalInfo(object):
	def __init__(self):
		pass

#
# GIVFuncInfo
#
class GIVFuncInfo(object):
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
class GIRegisteredTypeInfo(object):
	def __init__(self):
		pass

#
# GIEnumInfo
#
class GIEnumInfo(object):
	def __init__(self):
		pass

class GIValueInfo(object):
	def __init__(self):
		pass

#
# GIInterfaceInfo
#
class GIInterfaceInfo(object):
	def __init__(self):
		pass

#
# GIObjectInfo
#
class GIObjectInfo(object):
	def __init__(self):
		pass

#
# GIStructInfo
#
class GIStructInfo(object):
	def __init__(self):
		pass

#
# GIUnionInfo
#
class GIUnionInfo(object):
	def __init__(self):
		pass

#
# GIArgInfo
#
class GIArgInfo(object):
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
class GIConstantInfo(object):
	def __init__(self):
		pass

#
# GIErrorDomainInfo
#
class GIErrorDomainInfo(object):
	def __init__(self):
		pass

#
# GIFieldInfo
#
class GIFieldInfo(object):
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
class GIPropertyInfo(object):
	def __init__(self):
		pass

#
# GITypeInfo
#
class GITypeInfo(object):
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
class GITypelib(object):
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

class Header(object):
	def __init__(self):
		pass

class DirEntry(object):
	def __init__(self):
		pass

class ArgBlob(object):
	def __init__(self):
		pass

class SignatureBlob(object):
	def __init__(self):
		pass

class CommonBlob(object):
	def __init__(self):
		pass

class FunctionBlob(object):
	def __init__(self):
		pass

class CallbackBlob(object):
	def __init__(self):
		pass

class InterfaceTypeBlob(object):
	def __init__(self):
		pass

class ParamTypeBlob(object):
	def __init__(self):
		pass

class ErrorTypeBlob(object):
	def __init__(self):
		pass

class ErrorDomainBlob(object):
	def __init__(self):
		pass

class ValueBlob(object):
	def __init__(self):
		pass

class FieldBlob(object):
	def __init__(self):
		pass

class RegisteredTypeBlob(object):
	def __init__(self):
		pass

class StructBlob(object):
	def __init__(self):
		pass

class UnionBlob(object):
	def __init__(self):
		pass

class EnumBlob(object):
	def __init__(self):
		pass

class PropertyBlob(object):
	def __init__(self):
		pass

class SignalBlob(object):
	def __init__(self):
		pass

class VFuncBlob(object):
	def __init__(self):
		pass

class ObjectBlob(object):
	def __init__(self):
		pass

class InterfaceBlob(object):
	def __init__(self):
		pass

class ConstantBlob(object):
	def __init__(self):
		pass

class AttributeBlob(object):
	def __init__(self):
		pass

class Dimensions(object):
	def __init__(self):
		pass
