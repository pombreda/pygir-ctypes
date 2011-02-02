#
# High-level Python API
#
import _gir

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
		GI_INFO_TYPE_INVALID,
		GI_INFO_TYPE_FUNCTION,
		GI_INFO_TYPE_CALLBACK,
		GI_INFO_TYPE_STRUCT,
		GI_INFO_TYPE_BOXED,
		GI_INFO_TYPE_ENUM,
		GI_INFO_TYPE_FLAGS,
		GI_INFO_TYPE_OBJECT,
		GI_INFO_TYPE_INTERFACE,
		GI_INFO_TYPE_CONSTANT,
		GI_INFO_TYPE_ERROR_DOMAIN,
		GI_INFO_TYPE_UNION,
		GI_INFO_TYPE_VALUE,
		GI_INFO_TYPE_SIGNAL,
		GI_INFO_TYPE_VFUNC,
		GI_INFO_TYPE_PROPERTY,
		GI_INFO_TYPE_FIELD,
		GI_INFO_TYPE_ARG,
		GI_INFO_TYPE_TYPE,
		GI_INFO_TYPE_UNRESOLVED
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
		G_INVOKE_ERROR_FAILED,
		G_INVOKE_ERROR_SYMBOL_NOT_FOUND,
		G_INVOKE_ERROR_ARGUMENT_MISMATCH
	) = range(3)
	
	def __init__(self):
		pass

class GIFunctionInfoFlags(object):
	GI_FUNCTION_IS_METHOD = 1 << 0
	GI_FUNCTION_IS_CONSTRUCTOR = 1 << 1
	GI_FUNCTION_IS_GETTER = 1 << 2
	GI_FUNCTION_IS_SETTER = 1 << 3
	GI_FUNCTION_WRAPS_VFUNC = 1 << 4
	GI_FUNCTION_THROWS = 1 << 5
	
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
	GI_VFUNC_MUST_CHAIN_UP = 1 << 0
	GI_VFUNC_MUST_OVERRIDE = 1 << 1
	GI_VFUNC_MUST_NOT_OVERRIDE = 1 << 2
	
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
		GI_DIRECTION_IN,
		GI_DIRECTION_OUT,
		GI_DIRECTION_INOUT,
	) = range(3)
	
	def __init__(self):
		pass

class GIScopeType(object):
	(
		GI_SCOPE_TYPE_INVALID,
		GI_SCOPE_TYPE_CALL,
		GI_SCOPE_TYPE_ASYNC,
		GI_SCOPE_TYPE_NOTIFIED,
	) = range(4)

	def __init__(self):
		pass

class GITransfer(object):
	(
		GI_TRANSFER_NOTHING,
		GI_TRANSFER_CONTAINER,
		GI_TRANSFER_EVERYTHING,
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
	GI_FIELD_IS_READABLE = 1 << 0
	GI_FIELD_IS_WRITABLE = 1 << 1
	
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
		GI_ARRAY_TYPE_C,
		GI_ARRAY_TYPE_ARRAY,
		GI_ARRAY_TYPE_PTR_ARRAY,
		GI_ARRAY_TYPE_BYTE_ARRAY
	) = range(4)
	
	def __init__(self):
		pass

class GITypeTag(object):
	GI_TYPE_TAG_VOID = 0
	GI_TYPE_TAG_BOOLEAN = 1
	GI_TYPE_TAG_INT8 =  2
	GI_TYPE_TAG_UINT8 =  3
	GI_TYPE_TAG_INT16 =  4
	GI_TYPE_TAG_UINT16 =  5
	GI_TYPE_TAG_INT32 =  6
	GI_TYPE_TAG_UINT32 =  7
	GI_TYPE_TAG_INT64 =  8
	GI_TYPE_TAG_UINT64 = 9
	GI_TYPE_TAG_FLOAT = 10
	GI_TYPE_TAG_DOUBLE = 11
	GI_TYPE_TAG_GTYPE = 12
	GI_TYPE_TAG_UTF8 = 13
	GI_TYPE_TAG_FILENAME = 14
	GI_TYPE_TAG_ARRAY = 15
	GI_TYPE_TAG_INTERFACE = 16
	GI_TYPE_TAG_GLIST = 17
	GI_TYPE_TAG_GSLIST = 18
	GI_TYPE_TAG_GHASH = 19
	GI_TYPE_TAG_ERROR = 20
	
	def __init__(self):
		pass

#
# GIRepository
#
class GIRepository(object):
	def __init__(self):
		pass

class GICallbackInfo(object):
	def __init__(self):
		pass

#
# GIRepositoryError
#
class GIRepositoryError(object):
	(
		G_IREPOSITORY_ERROR_TYPELIB_NOT_FOUND,
		G_IREPOSITORY_ERROR_NAMESPACE_MISMATCH,
		G_IREPOSITORY_ERROR_NAMESPACE_VERSION_CONFLICT,
		G_IREPOSITORY_ERROR_LIBRARY_NOT_FOUND,
	) = range(4)

	def __init__(self):
		pass

#
# GIRepositoryLoadFlags
#
class GIRepositoryLoadFlags(object):
	G_IREPOSITORY_LOAD_FLAG_LAZY = 1 << 0
	
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
		BLOB_TYPE_INVALID,
		BLOB_TYPE_FUNCTION,
		BLOB_TYPE_CALLBACK,
		BLOB_TYPE_STRUCT,
		BLOB_TYPE_BOXED,
		BLOB_TYPE_ENUM,
		BLOB_TYPE_FLAGS,
		BLOB_TYPE_OBJECT,
		BLOB_TYPE_INTERFACE,
		BLOB_TYPE_CONSTANT,
		BLOB_TYPE_ERROR_DOMAIN,
		BLOB_TYPE_UNION,
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
