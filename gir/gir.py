import os
import sys
from ctypes import *
from ctypes.util import find_library

# dynamic libs
libgo = CDLL(find_library('gobject-2.0'))
libgir = CDLL(find_library('girepository-1.0'))

# ctypes utils
def ctypes_get_func(lib, name, restype=None, *argtypes):
	func = getattr(lib, name)
	func.restype = restype
	func.argtypes = argtypes
	return func

#
# Glib/GObject - C types
#
typedef_gboolean = c_int
typedef_gint8 = c_byte
typedef_guint8 = c_ubyte
typedef_gint16 = c_short
typedef_guint16 = c_ushort
typedef_gint32 = c_int
typedef_guint32 = c_uint
typedef_gint64 = c_longlong
typedef_guint64 = c_ulonglong
typedef_gfloat = c_float
typedef_gdouble = c_double
typedef_gshort = c_short
typedef_gushort = c_ushort
typedef_gint = c_int
typedef_guint = c_uint
typedef_glong = c_long
typedef_gulong = c_ulong
typedef_gssize = c_long
typedef_gsize = c_ulong
typedef_gchar = c_char
# NOTE: gchar_p represents "[const] gchar*" but not an actual typedef
typedef_gchar_p = c_char_p
typedef_gpointer = c_void_p

class struct_GObject(Structure): pass
typedef_GType = c_int
class struct_GError(Structure): pass
class struct_GList(Structure): pass
class struct_GSList(Structure): pass
class struct_GOptionGroup(Structure): pass
class struct_GMappedFile(Structure): pass
class struct_GValue(Structure): pass
typedef_GType = typedef_gsize

# GParam
class struct_GParamSpec(Structure): pass
class struct_GParamSpecClass(Structure): pass

enum_GParamFlags = c_int
enum_G_PARAM_READABLE = c_int(1 << 0)
enum_G_PARAM_WRITABLE = c_int(1 << 1)
enum_G_PARAM_CONSTRUCT = c_int(1 << 2)
enum_G_PARAM_CONSTRUCT_ONLY = c_int(1 << 3)
enum_G_PARAM_LAX_VALIDATION = c_int(1 << 4)
enum_G_PARAM_STATIC_NAME = c_int(1 << 5)
enum_G_PARAM_PRIVATE = enum_G_PARAM_STATIC_NAME
enum_G_PARAM_STATIC_NICK = c_int(1 << 6)
enum_G_PARAM_STATIC_BLURB = c_int(1 << 7)
enum_G_PARAM_DEPRECATED = c_int(1 << 31)

# GCClosure
class struct_GClosure(Structure): pass
class struct_GCClosure(Structure): pass

proto_GClosureMarshal = CFUNCTYPE(
	POINTER(struct_GClosure),
	POINTER(struct_GValue),
	typedef_guint,
	POINTER(struct_GValue),
	typedef_gpointer,
	typedef_gpointer,
)

# GSignal
class struct_GSignalInvocationHint(Structure): pass
proto_GSignalCMarshaller = proto_GClosureMarshal

proto_GSignalEmissionHook = CFUNCTYPE(
	POINTER(struct_GSignalInvocationHint),
	typedef_guint,
	POINTER(struct_GValue),
	typedef_gpointer,
)

enum_GSignalFlags = c_int
enum_G_SIGNAL_RUN_FIRST = c_int(1 << 0)
enum_G_SIGNAL_RUN_LAST = c_int(1 << 1)
enum_G_SIGNAL_RUN_CLEANUP = c_int(1 << 2)
enum_G_SIGNAL_NO_RECURSE = c_int(1 << 3)
enum_G_SIGNAL_DETAILED = c_int(1 << 4)
enum_G_SIGNAL_ACTION = c_int(1 << 5)
enum_G_SIGNAL_NO_HOOKS = c_int(1 << 6)

enum_GSignalMatchType = c_int
enum_G_SIGNAL_MATCH_ID = c_int(1 << 0)
enum_G_SIGNAL_MATCH_DETAIL = c_int(1 << 1)
enum_G_SIGNAL_MATCH_CLOSURE = c_int(1 << 2)
enum_G_SIGNAL_MATCH_FUNC = c_int(1 << 3)
enum_G_SIGNAL_MATCH_DATA = c_int(1 << 4)
enum_G_SIGNAL_MATCH_UNBLOCKED = c_int(1 << 5)

class struct_GSignalQuery(Structure): pass

#
# Glib/GObject - C functions
#
func_g_type_init = ctypes_get_func(
	libgo,
	'g_type_init',
)

#
# GIRepository - C types
#

# GIBaseInfo
class struct_GIBaseInfo(Structure): pass

class struct_GIAttributeIter(Structure): pass 

enum_GIInfoType = c_int
(
	enum_GI_INFO_TYPE_INVALID,
	enum_GI_INFO_TYPE_FUNCTION,
	enum_GI_INFO_TYPE_CALLBACK,
	enum_GI_INFO_TYPE_STRUCT,
	enum_GI_INFO_TYPE_BOXED,
	enum_GI_INFO_TYPE_ENUM,
	enum_GI_INFO_TYPE_FLAGS,
	enum_GI_INFO_TYPE_OBJECT,
	enum_GI_INFO_TYPE_INTERFACE,
	enum_GI_INFO_TYPE_CONSTANT,
	enum_GI_INFO_TYPE_ERROR_DOMAIN,
	enum_GI_INFO_TYPE_UNION,
	enum_GI_INFO_TYPE_VALUE,
	enum_GI_INFO_TYPE_SIGNAL,
	enum_GI_INFO_TYPE_VFUNC,
	enum_GI_INFO_TYPE_PROPERTY,
	enum_GI_INFO_TYPE_FIELD,
	enum_GI_INFO_TYPE_ARG,
	enum_GI_INFO_TYPE_TYPE,
	enum_GI_INFO_TYPE_UNRESOLVED
) = map(c_int, range(20))

name_GIInfoType = (
	'enum_GI_INFO_TYPE_INVALID',
	'enum_GI_INFO_TYPE_FUNCTION',
	'enum_GI_INFO_TYPE_CALLBACK',
	'enum_GI_INFO_TYPE_STRUCT',
	'enum_GI_INFO_TYPE_BOXED',
	'enum_GI_INFO_TYPE_ENUM',
	'enum_GI_INFO_TYPE_FLAGS',
	'enum_GI_INFO_TYPE_OBJECT',
	'enum_GI_INFO_TYPE_INTERFACE',
	'enum_GI_INFO_TYPE_CONSTANT',
	'enum_GI_INFO_TYPE_ERROR_DOMAIN',
	'enum_GI_INFO_TYPE_UNION',
	'enum_GI_INFO_TYPE_VALUE',
	'enum_GI_INFO_TYPE_SIGNAL',
	'enum_GI_INFO_TYPE_VFUNC',
	'enum_GI_INFO_TYPE_PROPERTY',
	'enum_GI_INFO_TYPE_FIELD',
	'enum_GI_INFO_TYPE_ARG',
	'enum_GI_INFO_TYPE_TYPE',
	'enum_GI_INFO_TYPE_UNRESOLVED',
)

# GICallableInfo
class struct_GICallableInfo(struct_GIBaseInfo): pass

# GIFunctionInfo
class struct_GIFunctionInfo(struct_GICallableInfo): pass

enum_GInvokeError = c_int
(
	enum_G_INVOKE_ERROR_FAILED,
	enum_G_INVOKE_ERROR_SYMBOL_NOT_FOUND,
	enum_G_INVOKE_ERROR_ARGUMENT_MISMATCH
) = map(c_int, range(3))

enum_GIFunctionInfoFlags = c_int
enum_GI_FUNCTION_IS_METHOD = c_int(1 << 0)
enum_GI_FUNCTION_IS_CONSTRUCTOR = c_int(1 << 1)
enum_GI_FUNCTION_IS_GETTER = c_int(1 << 2)
enum_GI_FUNCTION_IS_SETTER = c_int(1 << 3)
enum_GI_FUNCTION_WRAPS_VFUNC = c_int(1 << 4)
enum_GI_FUNCTION_THROWS = c_int(1 << 5)

name_GIFunctionInfoFlags = {
	1 << 0: 'enum_GI_FUNCTION_IS_METHOD',
	1 << 1: 'enum_GI_FUNCTION_IS_CONSTRUCTOR',
	1 << 2: 'enum_GI_FUNCTION_IS_GETTER',
	1 << 3: 'enum_GI_FUNCTION_IS_SETTER',
	1 << 4: 'enum_GI_FUNCTION_WRAPS_VFUNC',
	1 << 5: 'enum_GI_FUNCTION_THROWS',
}

# GISignalInfo
class struct_GISignalInfo(struct_GICallableInfo): pass

# GIVFuncInfo
class struct_GIVFuncInfo(struct_GICallableInfo): pass

enum_GIVFuncInfoFlags = c_int
enum_GI_VFUNC_MUST_CHAIN_UP = c_int(1 << 0)
enum_GI_VFUNC_MUST_OVERRIDE = c_int(1 << 1)
enum_GI_VFUNC_MUST_NOT_OVERRIDE = c_int(1 << 2)

name_GIVFuncInfoFlags =  {
	1 << 0: 'enum_GI_VFUNC_MUST_CHAIN_UP',
	1 << 1: 'enum_GI_VFUNC_MUST_OVERRIDE',
	1 << 2: 'enum_GI_VFUNC_MUST_NOT_OVERRIDE',
}

# GIRegisteredTypeInfo
class struct_GIRegisteredTypeInfo(struct_GIBaseInfo): pass

# GIEnumInfo
class struct_GIEnumInfo(struct_GIRegisteredTypeInfo): pass
class struct_GIValueInfo(Structure): pass

# GIInterfaceInfo
class struct_GIInterfaceInfo(struct_GIRegisteredTypeInfo): pass

# GIObjectInfo
class struct_GIObjectInfo(struct_GIRegisteredTypeInfo): pass

# GIStructInfo
class struct_GIStructInfo(struct_GIRegisteredTypeInfo): pass

# GIUnionInfo
class struct_GIUnionInfo(struct_GIRegisteredTypeInfo): pass

# GIArgInfo
class struct_GIArgInfo(struct_GIBaseInfo): pass

enum_GIDirection = c_int
(
	enum_GI_DIRECTION_IN,
	enum_GI_DIRECTION_OUT,
	enum_GI_DIRECTION_INOUT,
) = map(c_int, range(3))

name_GIDirection = [
	'enum_GI_DIRECTION_IN',
	'enum_GI_DIRECTION_OUT',
	'enum_GI_DIRECTION_INOUT',
]

enum_GIScopeType = c_int
(
	enum_GI_SCOPE_TYPE_INVALID,
	enum_GI_SCOPE_TYPE_CALL,
	enum_GI_SCOPE_TYPE_ASYNC,
	enum_GI_SCOPE_TYPE_NOTIFIED,
) = map(c_int, range(4))

name_GIScopeType = [
	'enum_GI_SCOPE_TYPE_INVALID',
	'enum_GI_SCOPE_TYPE_CALL',
	'enum_GI_SCOPE_TYPE_ASYNC',
	'enum_GI_SCOPE_TYPE_NOTIFIED',
]

enum_GITransfer = c_int
(
	enum_GI_TRANSFER_NOTHING,
	enum_GI_TRANSFER_CONTAINER,
	enum_GI_TRANSFER_EVERYTHING,
) = map(c_int, range(3))

name_GITransfer = [
	'enum_GI_TRANSFER_NOTHING',
	'enum_GI_TRANSFER_CONTAINER',
	'enum_GI_TRANSFER_EVERYTHING',
]

# GIArgument
class union_GIArgument(Union):
	_fields_ = [
		('v_boolean', typedef_gboolean),
		('v_int8', typedef_gint8),
		('v_uint8', typedef_guint8),
		('v_int16', typedef_gint16),
		('v_uint16', typedef_guint16),
		('v_int32', typedef_gint32),
		('v_uint32', typedef_guint32),
		('v_int64', typedef_gint64),
		('v_uint64', typedef_guint64),
		('v_float', typedef_gfloat),
		('v_double', typedef_gdouble),
		('v_short', typedef_gshort),
		('v_ushort', typedef_gushort),
		('v_int', typedef_gint),
		('v_uint', typedef_guint),
		('v_long', typedef_glong),
		('v_ulong', typedef_gulong),
		('v_ssize', typedef_gssize),
		('v_size', typedef_gsize),
		('v_string', typedef_gchar),
		('v_pointer', typedef_gpointer),
	]

# GIConstantInfo
class struct_GIConstantInfo(struct_GIBaseInfo): pass

# GIErrorDomainInfo
class struct_GIErrorDomainInfo(struct_GIBaseInfo): pass

# GIFieldInfo
class struct_GIFieldInfo(struct_GIBaseInfo): pass

enum_GIFieldInfoFlags = c_int
enum_GI_FIELD_IS_READABLE = c_int(1 << 0)
enum_GI_FIELD_IS_WRITABLE = c_int(1 << 1)

name_GIFieldInfoFlags = {
	1 << 0: 'enum_GI_FIELD_IS_READABLE',
	1 << 1: 'enum_GI_FIELD_IS_WRITABLE',
}

# GIPropertyInfo
class struct_GIPropertyInfo(struct_GIBaseInfo): pass

# GITypeInfo
class struct_GITypeInfo(struct_GIBaseInfo): pass

enum_GIArrayType = c_int
(
	enum_GI_ARRAY_TYPE_C,
	enum_GI_ARRAY_TYPE_ARRAY,
	enum_GI_ARRAY_TYPE_PTR_ARRAY,
	enum_GI_ARRAY_TYPE_BYTE_ARRAY
) = map(c_int, range(4))

name_GIArrayType = [
	'enum_GI_ARRAY_TYPE_C',
	'enum_GI_ARRAY_TYPE_ARRAY',
	'enum_GI_ARRAY_TYPE_PTR_ARRAY',
	'enum_GI_ARRAY_TYPE_BYTE_ARRAY',
]

enum_GITypeTag = c_int
enum_GI_TYPE_TAG_VOID = c_int(0)
enum_GI_TYPE_TAG_BOOLEAN = c_int(1)
enum_GI_TYPE_TAG_INT8 =  c_int(2)
enum_GI_TYPE_TAG_UINT8 =  c_int(3)
enum_GI_TYPE_TAG_INT16 =  c_int(4)
enum_GI_TYPE_TAG_UINT16 =  c_int(5)
enum_GI_TYPE_TAG_INT32 =  c_int(6)
enum_GI_TYPE_TAG_UINT32 =  c_int(7)
enum_GI_TYPE_TAG_INT64 =  c_int(8)
enum_GI_TYPE_TAG_UINT64 = c_int(9)
enum_GI_TYPE_TAG_FLOAT = c_int(10)
enum_GI_TYPE_TAG_DOUBLE = c_int(11)
enum_GI_TYPE_TAG_GTYPE = c_int(12)
enum_GI_TYPE_TAG_UTF8 = c_int(13)
enum_GI_TYPE_TAG_FILENAME = c_int(14)
enum_GI_TYPE_TAG_ARRAY = c_int(15)
enum_GI_TYPE_TAG_INTERFACE = c_int(16)
enum_GI_TYPE_TAG_GLIST = c_int(17)
enum_GI_TYPE_TAG_GSLIST = c_int(18)
enum_GI_TYPE_TAG_GHASH = c_int(19)
enum_GI_TYPE_TAG_ERROR = c_int(20)

name_GITypeTag = {
	0: 'enum_GI_TYPE_TAG_VOID',
	1: 'enum_GI_TYPE_TAG_BOOLEAN',
	2: 'enum_GI_TYPE_TAG_INT8',
	3: 'enum_GI_TYPE_TAG_UINT8',
	4: 'enum_GI_TYPE_TAG_INT16',
	5: 'enum_GI_TYPE_TAG_UINT16',
	6: 'enum_GI_TYPE_TAG_INT32',
	7: 'enum_GI_TYPE_TAG_UINT32',
	8: 'enum_GI_TYPE_TAG_INT64',
	9: 'enum_GI_TYPE_TAG_UINT64',
	10: 'enum_GI_TYPE_TAG_FLOAT',
	11: 'enum_GI_TYPE_TAG_DOUBLE',
	12: 'enum_GI_TYPE_TAG_GTYPE',
	13: 'enum_GI_TYPE_TAG_UTF8',
	14: 'enum_GI_TYPE_TAG_FILENAME',
	15: 'enum_GI_TYPE_TAG_ARRAY',
	16: 'enum_GI_TYPE_TAG_INTERFACE',
	17: 'enum_GI_TYPE_TAG_GLIST',
	18: 'enum_GI_TYPE_TAG_GSLIST',
	19: 'enum_GI_TYPE_TAG_GHASH',
	20: 'enum_GI_TYPE_TAG_ERROR',
}

# GIRepository
class struct_GICallbackInfo(struct_GIBaseInfo): pass
class struct_GIRepository(struct_GObject): pass

# GIRepositoryError
enum_GIRepositoryError = c_int
(
	enum_G_IREPOSITORY_ERROR_TYPELIB_NOT_FOUND,
	enum_G_IREPOSITORY_ERROR_NAMESPACE_MISMATCH,
	enum_G_IREPOSITORY_ERROR_NAMESPACE_VERSION_CONFLICT,
	enum_G_IREPOSITORY_ERROR_LIBRARY_NOT_FOUND,
) = map(c_int, range(4))

name_GIRepositoryError = [
	'enum_G_IREPOSITORY_ERROR_TYPELIB_NOT_FOUND',
	'enum_G_IREPOSITORY_ERROR_NAMESPACE_MISMATCH',
	'enum_G_IREPOSITORY_ERROR_NAMESPACE_VERSION_CONFLICT',
	'enum_G_IREPOSITORY_ERROR_LIBRARY_NOT_FOUND',
]

# GIRepositoryLoadFlags
enum_GIRepositoryLoadFlags = c_int
enum_G_IREPOSITORY_LOAD_FLAG_LAZY = c_int(1 << 0)

name_GIRepositoryLoadFlags = {
	1 << 0: 'enum_G_IREPOSITORY_LOAD_FLAG_LAZY',
}

# GITypelib
class struct_GITypelib(Structure): pass
	
# Typelib binary format
enum_GTypelibBlobType = c_int
(
	enum_BLOB_TYPE_INVALID,
	enum_BLOB_TYPE_FUNCTION,
	enum_BLOB_TYPE_CALLBACK,
	enum_BLOB_TYPE_STRUCT,
	enum_BLOB_TYPE_BOXED,
	enum_BLOB_TYPE_ENUM,
	enum_BLOB_TYPE_FLAGS,
	enum_BLOB_TYPE_OBJECT,
	enum_BLOB_TYPE_INTERFACE,
	enum_BLOB_TYPE_CONSTANT,
	enum_BLOB_TYPE_ERROR_DOMAIN,
	enum_BLOB_TYPE_UNION,
) = map(c_int, range(12))

name_GTypelibBlobType = [
	'enum_BLOB_TYPE_INVALID',
	'enum_BLOB_TYPE_FUNCTION',
	'enum_BLOB_TYPE_CALLBACK',
	'enum_BLOB_TYPE_STRUCT',
	'enum_BLOB_TYPE_BOXED',
	'enum_BLOB_TYPE_ENUM',
	'enum_BLOB_TYPE_FLAGS',
	'enum_BLOB_TYPE_OBJECT',
	'enum_BLOB_TYPE_INTERFACE',
	'enum_BLOB_TYPE_CONSTANT',
	'enum_BLOB_TYPE_ERROR_DOMAIN',
	'enum_BLOB_TYPE_UNION',
]

class struct_Header(Structure): pass
class struct_DirEntry(Structure): pass
class struct_ArgBlob(Structure): pass
class struct_SignatureBlob(Structure): pass
class struct_CommonBlob(Structure): pass
class struct_FunctionBlob(Structure): pass
class struct_CallbackBlob(Structure): pass
class struct_InterfaceTypeBlob(Structure): pass
class struct_ParamTypeBlob(Structure): pass
class struct_ErrorTypeBlob(Structure): pass
class struct_ErrorDomainBlob(Structure): pass
class struct_ValueBlob(Structure): pass
class struct_FieldBlob(Structure): pass
class struct_RegisteredTypeBlob(Structure): pass
class struct_StructBlob(Structure): pass
class struct_UnionBlob(Structure): pass
class struct_EnumBlob(Structure): pass
class struct_PropertyBlob(Structure): pass
class struct_SignalBlob(Structure): pass
class struct_VFuncBlob(Structure): pass
class struct_ObjectBlob(Structure): pass
class struct_InterfaceBlob(Structure): pass
class struct_ConstantBlob(Structure): pass
class struct_AttributeBlob(Structure): pass
class struct_dimensions(Structure): pass

#
# GIRepository - ctypes functions
#
func_g_irepository_get_default = ctypes_get_func(
	libgir,
	'g_irepository_get_default',
	POINTER(struct_GIRepository),
)

func_g_irepository_prepend_search_path = ctypes_get_func(
	libgir,
	'g_irepository_prepend_search_path',
	None,
	c_char_p,
)

func_g_irepository_get_search_path = ctypes_get_func(
	libgir,
	'g_irepository_get_search_path',
	POINTER(struct_GSList),
)

func_g_irepository_load_typelib = ctypes_get_func(
	libgir,
	'g_irepository_load_typelib',
	c_char_p,
	POINTER(struct_GIRepository),
	POINTER(struct_GITypelib),
	enum_GIRepositoryLoadFlags,
	POINTER(POINTER(struct_GError)),
)

func_g_irepository_is_registered = ctypes_get_func(
	libgir,
	'g_irepository_is_registered',
	c_int,
	POINTER(struct_GIRepository),
	c_char_p,
	c_char_p,
)

func_g_irepository_find_by_name = ctypes_get_func(
	libgir,
	'g_irepository_find_by_name',
	POINTER(struct_GIBaseInfo),
	POINTER(struct_GIRepository),
	c_char_p,
	c_char_p,
)

func_g_irepository_require = ctypes_get_func(
	libgir,
	'g_irepository_require',
	POINTER(struct_GITypelib),
	POINTER(struct_GIRepository),
	c_char_p,
	c_char_p,
	enum_GIRepositoryLoadFlags,
	POINTER(POINTER(struct_GError)),
)

func_g_irepository_require_private = ctypes_get_func(
	libgir,
	'g_irepository_require_private',
	POINTER(struct_GITypelib),
	POINTER(struct_GIRepository),
	c_char_p,
	c_char_p,
	c_char_p,
	enum_GIRepositoryLoadFlags,
	POINTER(POINTER(struct_GError)),
)

func_g_irepository_get_dependencies = ctypes_get_func(
	libgir,
	'g_irepository_get_dependencies',
	POINTER(c_char_p),
	POINTER(struct_GIRepository),
	c_char_p,
)

func_g_irepository_get_loaded_namespaces = ctypes_get_func(
	libgir,
	'g_irepository_get_loaded_namespaces',
	POINTER(c_char_p),
	POINTER(struct_GIRepository),
)

func_g_irepository_find_by_gtype = ctypes_get_func(
	libgir,
	'g_irepository_find_by_gtype',
	POINTER(struct_GIBaseInfo),
	POINTER(struct_GIRepository),
	typedef_GType
)

func_g_irepository_get_n_infos = ctypes_get_func(
	libgir,
	'g_irepository_get_n_infos',
	c_int,
	POINTER(struct_GIRepository),
	c_char_p,
)

func_g_irepository_get_info = ctypes_get_func(
	libgir,
	'g_irepository_get_info',
	POINTER(struct_GIBaseInfo),
	POINTER(struct_GIRepository),
	c_char_p,
	c_int,
)

func_g_irepository_get_typelib_path = ctypes_get_func(
	libgir,
	'g_irepository_get_typelib_path',
	c_char_p,
	POINTER(struct_GIRepository),
	c_char_p,
)

func_g_irepository_get_shared_library = ctypes_get_func(
	libgir,
	'g_irepository_get_shared_library',
	c_char_p,
	POINTER(struct_GIRepository),
	c_char_p,
)

func_g_irepository_get_version = ctypes_get_func(
	libgir,
	'g_irepository_get_version',
	c_char_p,
	POINTER(struct_GIRepository),
	c_char_p,
)

func_g_irepository_get_option_group = ctypes_get_func(
	libgir,
	'g_irepository_get_option_group',
	POINTER(struct_GOptionGroup),
)

func_g_irepository_get_c_prefix = ctypes_get_func(
	libgir,
	'g_irepository_get_c_prefix',
	c_char_p,
	POINTER(struct_GIRepository),
	c_char_p,
)

func_g_irepository_dump = ctypes_get_func(
	libgir,
	'g_irepository_dump',
	c_int,
	c_char_p,
	POINTER(POINTER(struct_GError)),
)

func_g_irepository_enumerate_versions = ctypes_get_func(
	libgir,
	'g_irepository_enumerate_versions',
	POINTER(struct_GList),
	POINTER(struct_GIRepository),
	c_char_p,
)

func_g_typelib_new_from_memory = ctypes_get_func(
	libgir,
	'g_typelib_new_from_memory',
	POINTER(struct_GITypelib),
	POINTER(c_ubyte),
	c_ulong,
	POINTER(POINTER(struct_GError)),
)

func_g_typelib_new_from_const_memory = ctypes_get_func(
	libgir,
	'g_typelib_new_from_const_memory',
	POINTER(struct_GITypelib),
	POINTER(c_ubyte),
	c_ulong,
	POINTER(POINTER(struct_GError)),
)

func_g_typelib_new_from_mapped_file = ctypes_get_func(
	libgir,
	'g_typelib_new_from_mapped_file',
	POINTER(struct_GITypelib),
	POINTER(struct_GMappedFile),
	POINTER(POINTER(struct_GError)),
)

func_g_typelib_free = ctypes_get_func(
	libgir,
	'g_typelib_free',
	None,
	POINTER(struct_GITypelib),
)

func_g_typelib_symbol = ctypes_get_func(
	libgir,
	'g_typelib_symbol',
	c_int,
	POINTER(struct_GITypelib),
	c_char_p,
	c_void_p,
)

func_g_typelib_get_namespace = ctypes_get_func(
	libgir,
	'g_typelib_get_namespace',
	c_char_p,
	POINTER(struct_GITypelib),
)

#
# GIBaseInfo
#
func_g_info_type_to_string = ctypes_get_func(
	libgir,
	'g_info_type_to_string',
	c_char_p,
	enum_GIInfoType,
)

func_g_base_info_ref = ctypes_get_func(
	libgir,
	'g_base_info_ref',
	POINTER(struct_GIBaseInfo),
	POINTER(struct_GIBaseInfo),
)

func_g_base_info_unref = ctypes_get_func(
	libgir,
	'g_base_info_unref',
	None,
	POINTER(struct_GIBaseInfo),
)

func_g_base_info_get_type = ctypes_get_func(
	libgir,
	'g_base_info_get_type',
	enum_GIInfoType,
	POINTER(struct_GIBaseInfo),
)

func_g_base_info_get_name = ctypes_get_func(
	libgir,
	'g_base_info_get_name',
	c_char_p,
	POINTER(struct_GIBaseInfo),
)

func_g_base_info_get_namespace = ctypes_get_func(
	libgir,
	'g_base_info_get_namespace',
	c_char_p,
	POINTER(struct_GIBaseInfo),
)

func_g_base_info_is_deprecated = ctypes_get_func(
	libgir,
	'g_base_info_is_deprecated',
	c_int,
	POINTER(struct_GIBaseInfo),
)

func_g_base_info_get_attribute = ctypes_get_func(
	libgir,
	'g_base_info_get_attribute',
	c_char_p,
	POINTER(struct_GIBaseInfo),
	c_char_p,
)

func_g_base_info_iterate_attributes = ctypes_get_func(
	libgir,
	'g_base_info_iterate_attributes',
	c_int,
	POINTER(struct_GIBaseInfo),
	POINTER(struct_GIAttributeIter),
	c_char_p,
	c_char_p,
)

func_g_base_info_get_container = ctypes_get_func(
	libgir,
	'g_base_info_get_container',
	POINTER(struct_GIBaseInfo),
	POINTER(struct_GIBaseInfo),
)

func_g_base_info_get_typelib = ctypes_get_func(
	libgir,
	'g_base_info_get_typelib',
	POINTER(struct_GITypelib),
	POINTER(struct_GIBaseInfo),
)

func_g_base_info_equal = ctypes_get_func(
	libgir,
	'g_base_info_equal',
	c_int,
	POINTER(struct_GIBaseInfo),
	POINTER(struct_GIBaseInfo),
)

#
# GIFunctionInfo
#
func_g_function_info_get_symbol = ctypes_get_func(
	libgir,
	'g_function_info_get_symbol',
	c_char_p,
	POINTER(struct_GIFunctionInfo),
)

func_g_function_info_get_flags = ctypes_get_func(
	libgir,
	'g_function_info_get_flags',
	enum_GIFunctionInfoFlags,
	POINTER(struct_GIFunctionInfo),
)

func_g_function_info_get_property = ctypes_get_func(
	libgir,
	'g_function_info_get_property',
	POINTER(struct_GIPropertyInfo),
	POINTER(struct_GIFunctionInfo),
)

func_g_function_info_get_vfunc = ctypes_get_func(
	libgir,
	'g_function_info_get_vfunc',
	POINTER(struct_GIVFuncInfo),
	POINTER(struct_GIFunctionInfo),
)

func_g_function_info_invoke = ctypes_get_func(
	libgir,
	'g_function_info_invoke',
	c_int,
	POINTER(struct_GIFunctionInfo),
	POINTER(union_GIArgument),
	c_int,
	POINTER(union_GIArgument),
	c_int,
	POINTER(union_GIArgument),
	POINTER(POINTER(struct_GError)),
)

#
# GICallableInfo
#
func_g_callable_info_get_return_type = ctypes_get_func(
	libgir,
	'g_callable_info_get_return_type',
	POINTER(struct_GITypeInfo),
	POINTER(struct_GICallableInfo),
)

func_g_callable_info_get_caller_owns = ctypes_get_func(
	libgir,
	'g_callable_info_get_caller_owns',
	enum_GITransfer,
	POINTER(struct_GICallableInfo),
)

func_g_callable_info_may_return_null = ctypes_get_func(
	libgir,
	'g_callable_info_may_return_null',
	c_int,
	POINTER(struct_GICallableInfo),
)

func_g_callable_info_get_return_attribute = ctypes_get_func(
	libgir,
	'g_callable_info_get_return_attribute',
	c_char_p,
	POINTER(struct_GICallableInfo),
	c_char_p,
)

func_g_callable_info_iterate_return_attributes = ctypes_get_func(
	libgir,
	'g_callable_info_iterate_return_attributes',
	c_char_p,
	POINTER(struct_GICallableInfo),
	POINTER(struct_GIAttributeIter),
	POINTER(c_char_p),
	POINTER(c_char_p),
)

func_g_callable_info_get_n_args = ctypes_get_func(
	libgir,
	'g_callable_info_get_n_args',
	c_int,
	POINTER(struct_GICallableInfo),
)

func_g_callable_info_get_arg = ctypes_get_func(
	libgir,
	'g_callable_info_get_arg',
	POINTER(struct_GIArgInfo),
	POINTER(struct_GICallableInfo),
	c_int,
)

func_g_callable_info_load_arg = ctypes_get_func(
	libgir,
	'g_callable_info_load_arg',
	None,
	POINTER(struct_GICallableInfo),
	c_int,
	POINTER(struct_GIArgInfo),
)

func_g_callable_info_load_return_type = ctypes_get_func(
	libgir,
	'g_callable_info_load_return_type',
	None,
	POINTER(struct_GICallableInfo),
	POINTER(struct_GITypeInfo),
)

#
# GIArgInfo
#
func_g_arg_info_get_direction = ctypes_get_func(
	libgir,
	'g_arg_info_get_direction',
	enum_GIDirection,
	POINTER(struct_GIArgInfo),
)

func_g_arg_info_is_caller_allocates = ctypes_get_func(
	libgir,
	'g_arg_info_is_caller_allocates',
	c_int,
	POINTER(struct_GIArgInfo),
)

func_g_arg_info_is_return_value = ctypes_get_func(
	libgir,
	'g_arg_info_is_return_value',
	c_int,
	POINTER(struct_GIArgInfo),
)

func_g_arg_info_is_optional = ctypes_get_func(
	libgir,
	'g_arg_info_is_optional',
	c_int,
	POINTER(struct_GIArgInfo),
)

func_g_arg_info_may_be_null = ctypes_get_func(
	libgir,
	'g_arg_info_may_be_null',
	c_int,
	POINTER(struct_GIArgInfo),
)

func_g_arg_info_get_ownership_transfer = ctypes_get_func(
	libgir,
	'g_arg_info_get_ownership_transfer',
	enum_GITransfer,
	POINTER(struct_GIArgInfo),
)

func_g_arg_info_get_scope = ctypes_get_func(
	libgir,
	'g_arg_info_get_scope',
	enum_GIScopeType,
	POINTER(struct_GIArgInfo),
)

func_g_arg_info_get_closure = ctypes_get_func(
	libgir,
	'g_arg_info_get_closure',
	c_int,
	POINTER(struct_GIArgInfo),
)

func_g_arg_info_get_destroy = ctypes_get_func(
	libgir,
	'g_arg_info_get_destroy',
	c_int,
	POINTER(struct_GIArgInfo),
)

func_g_arg_info_get_type = ctypes_get_func(
	libgir,
	'g_arg_info_get_type',
	POINTER(struct_GITypeInfo),
	POINTER(struct_GIArgInfo),
)

func_g_arg_info_get_type = ctypes_get_func(
	libgir,
	'g_arg_info_get_type',
	None,
	POINTER(struct_GIArgInfo),
	POINTER(struct_GITypeInfo),
)

#
# GIStructInfo
#
func_g_struct_info_get_n_fields = ctypes_get_func(
	libgir,
	'g_struct_info_get_n_fields',
	c_int,
	POINTER(struct_GIStructInfo),
)

func_g_struct_info_get_field = ctypes_get_func(
	libgir,
	'g_struct_info_get_field',
	POINTER(struct_GIFieldInfo),
	POINTER(struct_GIStructInfo),
	c_int,
)

func_g_struct_info_get_n_methods = ctypes_get_func(
	libgir,
	'g_struct_info_get_n_methods',
	c_int,
	POINTER(struct_GIStructInfo),
)

func_g_struct_info_get_method = ctypes_get_func(
	libgir,
	'g_struct_info_get_method',
	POINTER(struct_GIFunctionInfo),
	POINTER(struct_GIStructInfo),
	c_int,
)

func_g_struct_info_find_method = ctypes_get_func(
	libgir,
	'g_struct_info_find_method',
	POINTER(struct_GIFunctionInfo),
	POINTER(struct_GIStructInfo),
	c_char_p,
)

func_g_struct_info_get_size = ctypes_get_func(
	libgir,
	'g_struct_info_get_size',
	typedef_gsize,
	POINTER(struct_GIStructInfo),
)

func_g_struct_info_get_alignment = ctypes_get_func(
	libgir,
	'g_struct_info_get_alignment',
	typedef_gsize,
	POINTER(struct_GIStructInfo),
)

func_g_struct_info_is_gtype_struct = ctypes_get_func(
	libgir,
	'g_struct_info_is_gtype_struct',
	typedef_gboolean,
	POINTER(struct_GIStructInfo),
)

func_g_struct_info_is_foreign = ctypes_get_func(
	libgir,
	'g_struct_info_is_foreign',
	typedef_gboolean,
	POINTER(struct_GIStructInfo),
)

#
# GIUnionInfo
#
func_g_union_info_get_n_fields = ctypes_get_func(
	libgir,
	'g_union_info_get_n_fields',
	typedef_gint,
	POINTER(struct_GIUnionInfo),
)

func_g_union_info_get_field = ctypes_get_func(
	libgir,
	'g_union_info_get_field',
	POINTER(struct_GIFieldInfo),
	POINTER(struct_GIUnionInfo),
	typedef_gint,
)

func_g_union_info_get_n_methods = ctypes_get_func(
	libgir,
	'g_union_info_get_n_methods',
	typedef_gint,
	POINTER(struct_GIUnionInfo),
)

func_g_union_info_get_method = ctypes_get_func(
	libgir,
	'g_union_info_get_method',
	POINTER(struct_GIFunctionInfo),
	POINTER(struct_GIUnionInfo),
	typedef_gint,
)

func_g_union_info_is_discriminated = ctypes_get_func(
	libgir,
	'g_union_info_is_discriminated',
	typedef_gboolean,
	POINTER(struct_GIUnionInfo),
)

func_g_union_info_get_discriminator_offset = ctypes_get_func(
	libgir,
	'g_union_info_get_discriminator_offset',
	typedef_gint,
	POINTER(struct_GIUnionInfo),
)

func_g_union_info_get_discriminator_type = ctypes_get_func(
	libgir,
	'g_union_info_get_discriminator_type',
	POINTER(struct_GITypeInfo),
	POINTER(struct_GIUnionInfo),
)

func_g_union_info_get_discriminator = ctypes_get_func(
	libgir,
	'g_union_info_get_discriminator',
	POINTER(struct_GIConstantInfo),
	POINTER(struct_GIUnionInfo),
	typedef_gint,
)

func_g_union_info_find_method = ctypes_get_func(
	libgir,
	'g_union_info_find_method',
	POINTER(struct_GIFunctionInfo),
	POINTER(struct_GIUnionInfo),
	typedef_gchar_p,
)

func_g_union_info_get_size = ctypes_get_func(
	libgir,
	'g_union_info_get_size',
	typedef_gsize,
	POINTER(struct_GIUnionInfo),
)

func_g_union_info_get_alignment = ctypes_get_func(
	libgir,
	'g_union_info_get_alignment',
	typedef_gsize,
	POINTER(struct_GIUnionInfo),
)

#
# GIFieldInfo
#
func_g_field_info_get_flags = ctypes_get_func(
	libgir,
	'g_field_info_get_flags',
	enum_GIFieldInfoFlags,
	POINTER(struct_GIFieldInfo),
)

func_g_field_info_get_size = ctypes_get_func(
	libgir,
	'g_field_info_get_size',
	typedef_gint,
	POINTER(struct_GIFieldInfo),
)

func_g_field_info_get_offset = ctypes_get_func(
	libgir,
	'g_field_info_get_offset',
	typedef_gint,
	POINTER(struct_GIFieldInfo),
)

func_g_field_info_get_type = ctypes_get_func(
	libgir,
	'g_field_info_get_type',
	POINTER(struct_GITypeInfo),
	POINTER(struct_GIFieldInfo),
)

func_g_field_info_get_field = ctypes_get_func(
	libgir,
	'g_field_info_get_field',
	typedef_gboolean,
	POINTER(struct_GIFieldInfo),
	typedef_gpointer,
	POINTER(union_GIArgument),
)

func_g_field_info_set_field = ctypes_get_func(
	libgir,
	'g_field_info_set_field',
	typedef_gboolean,
	POINTER(struct_GIFieldInfo),
	typedef_gpointer,
	POINTER(union_GIArgument),
)

#
# GIPropertyInfo
#
func_g_property_info_get_flags = ctypes_get_func(
	libgir,
	'g_property_info_get_flags',
	enum_GParamFlags,
	POINTER(struct_GIPropertyInfo),
)

func_g_property_info_get_type = ctypes_get_func(
	libgir,
	'g_property_info_get_type',
	POINTER(struct_GITypeInfo),
	POINTER(struct_GIPropertyInfo),
)

func_g_property_info_get_ownership_transfer = ctypes_get_func(
	libgir,
	'g_property_info_get_ownership_transfer',
	enum_GITransfer,
	POINTER(struct_GIPropertyInfo),
)

#
# GIVFuncInfo
#
func_g_vfunc_info_get_flags = ctypes_get_func(
	libgir,
	'g_vfunc_info_get_flags',
	enum_GIVFuncInfoFlags,
	POINTER(struct_GIVFuncInfo),
)

func_g_vfunc_info_get_offset = ctypes_get_func(
	libgir,
	'g_vfunc_info_get_offset',
	typedef_gint,
	POINTER(struct_GIVFuncInfo),
)

func_g_vfunc_info_get_signal = ctypes_get_func(
	libgir,
	'g_vfunc_info_get_signal',
	POINTER(struct_GISignalInfo),
	POINTER(struct_GIVFuncInfo),
)

func_g_vfunc_info_get_invoker = ctypes_get_func(
	libgir,
	'g_vfunc_info_get_invoker',
	POINTER(struct_GIFunctionInfo),
	POINTER(struct_GIVFuncInfo),
)

#
# GISignalInfo
#
func_g_signal_info_get_flags = ctypes_get_func(
	libgir,
	'g_signal_info_get_flags',
	enum_GSignalFlags,
	POINTER(struct_GISignalInfo),
)

func_g_signal_info_get_class_closure = ctypes_get_func(
	libgir,
	'g_signal_info_get_class_closure',
	POINTER(struct_GIVFuncInfo),
	POINTER(struct_GISignalInfo),
)

func_g_signal_info_true_stops_emit = ctypes_get_func(
	libgir,
	'g_signal_info_true_stops_emit',
	typedef_gboolean,
	POINTER(struct_GISignalInfo),
)

#
# GIEnumInfo
#
func_g_enum_info_get_n_values = ctypes_get_func(
	libgir,
	'g_enum_info_get_n_values',
	typedef_gint,
	POINTER(struct_GIEnumInfo),
)

func_g_enum_info_get_value = ctypes_get_func(
	libgir,
	'g_enum_info_get_value',
	POINTER(struct_GIValueInfo),
	POINTER(struct_GIEnumInfo),
	typedef_gint,
)

func_g_enum_info_get_storage_type = ctypes_get_func(
	libgir,
	'g_enum_info_get_storage_type',
	enum_GITypeTag,
	POINTER(struct_GIEnumInfo),
)

func_g_value_info_get_value = ctypes_get_func(
	libgir,
	'g_value_info_get_value',
	typedef_glong,
	POINTER(struct_GIValueInfo),
)

#
# GIRegisteredTypeInfo
#
func_g_registered_type_info_get_type_name = ctypes_get_func(
	libgir,
	'g_registered_type_info_get_type_name',
	typedef_gchar_p,
	POINTER(struct_GIRegisteredTypeInfo),
)

func_g_registered_type_info_get_type_init = ctypes_get_func(
	libgir,
	'g_registered_type_info_get_type_init',
	typedef_gchar_p,
	POINTER(struct_GIRegisteredTypeInfo),
)

func_g_registered_type_info_get_g_type = ctypes_get_func(
	libgir,
	'g_registered_type_info_get_g_type',
	typedef_GType,
	POINTER(struct_GIRegisteredTypeInfo),
)

#
# GIObjectInfo
#
proto_GIObjectInfoGetValueFunction = CFUNCTYPE(c_void_p, POINTER(struct_GValue))
proto_GIObjectInfoRefFunction = CFUNCTYPE(c_void_p, c_void_p)
proto_GIObjectInfoSetValueFunction = CFUNCTYPE(None, POINTER(struct_GValue), c_void_p)
proto_GIObjectInfoUnrefFunction = CFUNCTYPE(None, c_void_p)

func_g_object_info_get_type_name = ctypes_get_func(
	libgir,
	'g_object_info_get_type_name',
	typedef_gchar_p,
	POINTER(struct_GIObjectInfo),
)

func_g_object_info_get_type_init = ctypes_get_func(
	libgir,
	'g_object_info_get_type_init',
	typedef_gchar_p,
	POINTER(struct_GIObjectInfo),
)

func_g_object_info_get_abstract = ctypes_get_func(
	libgir,
	'g_object_info_get_abstract',
	typedef_gboolean,
	POINTER(struct_GIObjectInfo),
)

func_g_object_info_get_fundamental = ctypes_get_func(
	libgir,
	'g_object_info_get_fundamental',
	typedef_gboolean,
	POINTER(struct_GIObjectInfo),
)

func_g_object_info_get_parent = ctypes_get_func(
	libgir,
	'g_object_info_get_parent',
	POINTER(struct_GIObjectInfo),
	POINTER(struct_GIObjectInfo),
)

func_g_object_info_get_n_interfaces = ctypes_get_func(
	libgir,
	'g_object_info_get_n_interfaces',
	typedef_gint,
	POINTER(struct_GIObjectInfo),
)

func_g_object_info_get_interface = ctypes_get_func(
	libgir,
	'g_object_info_get_interface',
	POINTER(struct_GIInterfaceInfo),
	POINTER(struct_GIObjectInfo),
	typedef_gint,
)

func_g_object_info_get_n_fields = ctypes_get_func(
	libgir,
	'g_object_info_get_n_fields',
	typedef_gint,
	POINTER(struct_GIObjectInfo),
)

func_g_object_info_get_field = ctypes_get_func(
	libgir,
	'g_object_info_get_field',
	POINTER(struct_GIFieldInfo),
	POINTER(struct_GIObjectInfo),
	typedef_gint,
)

func_g_object_info_get_n_properties = ctypes_get_func(
	libgir,
	'g_object_info_get_n_properties',
	typedef_gint,
	POINTER(struct_GIObjectInfo),
)

func_g_object_info_get_property = ctypes_get_func(
	libgir,
	'g_object_info_get_property',
	POINTER(struct_GIPropertyInfo),
	POINTER(struct_GIObjectInfo),
	typedef_gint,
)

func_g_object_info_get_n_methods = ctypes_get_func(
	libgir,
	'g_object_info_get_n_methods',
	typedef_gint,
	POINTER(struct_GIObjectInfo),
)

func_g_object_info_get_method = ctypes_get_func(
	libgir,
	'g_object_info_get_method',
	POINTER(struct_GIFunctionInfo),
	POINTER(struct_GIObjectInfo),
	typedef_gint,
)

func_g_object_info_find_method = ctypes_get_func(
	libgir,
	'g_object_info_find_method',
	POINTER(struct_GIFunctionInfo),
	POINTER(struct_GIObjectInfo),
	typedef_gchar_p,
)

func_g_object_info_get_n_signals = ctypes_get_func(
	libgir,
	'g_object_info_get_n_signals',
	typedef_gint,
	POINTER(struct_GIObjectInfo),
)

func_g_object_info_get_signal = ctypes_get_func(
	libgir,
	'g_object_info_get_signal',
	POINTER(struct_GISignalInfo),
	POINTER(struct_GIObjectInfo),
	typedef_gint,
)

func_g_object_info_get_n_vfuncs = ctypes_get_func(
	libgir,
	'g_object_info_get_n_vfuncs',
	typedef_gint,
	POINTER(struct_GIObjectInfo),
)

func_g_object_info_get_vfunc = ctypes_get_func(
	libgir,
	'g_object_info_get_vfunc',
	POINTER(struct_GIVFuncInfo),
	POINTER(struct_GIObjectInfo),
	typedef_gint,
)

func_g_object_info_get_n_constants = ctypes_get_func(
	libgir,
	'g_object_info_get_n_constants',
	typedef_gint,
	POINTER(struct_GIObjectInfo),
)

func_g_object_info_get_constant = ctypes_get_func(
	libgir,
	'g_object_info_get_constant',
	POINTER(struct_GIConstantInfo),
	POINTER(struct_GIObjectInfo),
	typedef_gint,
)

func_g_object_info_get_class_struct = ctypes_get_func(
	libgir,
	'g_object_info_get_class_struct',
	POINTER(struct_GIStructInfo),
	POINTER(struct_GIObjectInfo),
)

func_g_object_info_find_vfunc = ctypes_get_func(
	libgir,
	'g_object_info_find_vfunc',
	POINTER(struct_GIVFuncInfo),
	POINTER(struct_GIObjectInfo),
	typedef_gchar_p,
)

func_g_object_info_get_unref_function = ctypes_get_func(
	libgir,
	'g_object_info_get_unref_function',
	typedef_gchar_p,
	POINTER(struct_GIObjectInfo),
)

func_g_object_info_get_unref_function_pointer = ctypes_get_func(
	libgir,
	'g_object_info_get_unref_function_pointer',
	proto_GIObjectInfoUnrefFunction,
	POINTER(struct_GIObjectInfo),
)

func_g_object_info_get_ref_function = ctypes_get_func(
	libgir,
	'g_object_info_get_ref_function',
	typedef_gchar_p,
	POINTER(struct_GIObjectInfo),
)

func_g_object_info_get_ref_function_pointer = ctypes_get_func(
	libgir,
	'g_object_info_get_ref_function_pointer',
	proto_GIObjectInfoRefFunction,
	POINTER(struct_GIObjectInfo),
)

func_g_object_info_get_set_value_function = ctypes_get_func(
	libgir,
	'g_object_info_get_set_value_function',
	typedef_gchar_p,
	POINTER(struct_GIObjectInfo),
)

func_g_object_info_get_set_value_function_pointer = ctypes_get_func(
	libgir,
	'g_object_info_get_set_value_function_pointer',
	proto_GIObjectInfoSetValueFunction,
	POINTER(struct_GIObjectInfo),
)

func_g_object_info_get_get_value_function = ctypes_get_func(
	libgir,
	'g_object_info_get_get_value_function',
	typedef_gchar_p,
	POINTER(struct_GIObjectInfo),
)

func_g_object_info_get_get_value_function_pointer = ctypes_get_func(
	libgir,
	'g_object_info_get_get_value_function_pointer',
	proto_GIObjectInfoGetValueFunction,
	POINTER(struct_GIObjectInfo),
)

#
# GIInterfaceInfo
#
func_g_interface_info_get_n_prerequisites = ctypes_get_func(
	libgir,
	'g_interface_info_get_n_prerequisites',
	typedef_gint,
	POINTER(struct_GIInterfaceInfo),
)

func_g_interface_info_get_prerequisite = ctypes_get_func(
	libgir,
	'g_interface_info_get_prerequisite',
	POINTER(struct_GIBaseInfo),
	POINTER(struct_GIInterfaceInfo),
	typedef_gint,
)

func_g_interface_info_get_n_properties = ctypes_get_func(
	libgir,
	'g_interface_info_get_n_properties',
	typedef_gint,
	POINTER(struct_GIInterfaceInfo),
)

func_g_interface_info_get_property = ctypes_get_func(
	libgir,
	'g_interface_info_get_property',
	POINTER(struct_GIPropertyInfo),
	POINTER(struct_GIInterfaceInfo),
	typedef_gint,
)

func_g_interface_info_get_n_methods = ctypes_get_func(
	libgir,
	'g_interface_info_get_n_methods',
	typedef_gint,
	POINTER(struct_GIInterfaceInfo),
)

func_g_interface_info_get_method = ctypes_get_func(
	libgir,
	'g_interface_info_get_method',
	POINTER(struct_GIFunctionInfo),
	POINTER(struct_GIInterfaceInfo),
	typedef_gint,
)

func_g_interface_info_find_method = ctypes_get_func(
	libgir,
	'g_interface_info_find_method',
	POINTER(struct_GIFunctionInfo),
	POINTER(struct_GIInterfaceInfo),
	typedef_gchar_p,
)

func_g_interface_info_get_n_signals = ctypes_get_func(
	libgir,
	'g_interface_info_get_n_signals',
	typedef_gint,
	POINTER(struct_GIInterfaceInfo),
)

func_g_interface_info_get_signal = ctypes_get_func(
	libgir,
	'g_interface_info_get_signal',
	POINTER(struct_GISignalInfo),
	POINTER(struct_GIInterfaceInfo),
	typedef_gint,
)

func_g_interface_info_get_n_vfuncs = ctypes_get_func(
	libgir,
	'g_interface_info_get_n_vfuncs',
	typedef_gint,
	POINTER(struct_GIInterfaceInfo),
)

func_g_interface_info_get_vfunc = ctypes_get_func(
	libgir,
	'g_interface_info_get_vfunc',
	POINTER(struct_GIVFuncInfo),
	POINTER(struct_GIInterfaceInfo),
	typedef_gint,
)

func_g_interface_info_get_n_constants = ctypes_get_func(
	libgir,
	'g_interface_info_get_n_constants',
	typedef_gint,
	POINTER(struct_GIInterfaceInfo),
)

func_g_interface_info_get_constant = ctypes_get_func(
	libgir,
	'g_interface_info_get_constant',
	POINTER(struct_GIConstantInfo),
	POINTER(struct_GIInterfaceInfo),
	typedef_gint,
)

func_g_interface_info_get_iface_struct = ctypes_get_func(
	libgir,
	'g_interface_info_get_iface_struct',
	POINTER(struct_GIStructInfo),
	POINTER(struct_GIInterfaceInfo),
)

func_g_interface_info_find_vfunc = ctypes_get_func(
	libgir,
	'g_interface_info_find_vfunc',
	POINTER(struct_GIVFuncInfo),
	POINTER(struct_GIInterfaceInfo),
	typedef_gchar_p,
)

#
# GIConstantInfo
#
func_g_constant_info_get_type = ctypes_get_func(
	libgir,
	'g_constant_info_get_type',
	POINTER(struct_GITypeInfo),
	POINTER(struct_GIConstantInfo),
)

func_g_constant_info_get_value = ctypes_get_func(
	libgir,
	'g_constant_info_get_value',
	typedef_gint,
	POINTER(struct_GIConstantInfo),
	POINTER(union_GIArgument),
)

#
# GIErrorDomainInfo
#
func_g_error_domain_info_get_quark = ctypes_get_func(
	libgir,
	'g_error_domain_info_get_quark',
	typedef_gchar_p,
	POINTER(struct_GIErrorDomainInfo),
)

func_g_error_domain_info_get_codes = ctypes_get_func(
	libgir,
	'g_error_domain_info_get_codes',
	POINTER(struct_GIInterfaceInfo),
	POINTER(struct_GIErrorDomainInfo),
)

#
# Low-level C classes
#

# GIArgument - C <-> Python functions
def giargument_from_object(obj):
	pass

def object_from_giargument(arg):
	pass

def giargument_release(arg):
	pass

#
# High-level Python classes
#
