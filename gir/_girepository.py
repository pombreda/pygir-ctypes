exec('from ._gobject import *', globals(), locals())

# girepository - C library
libgirepository = CDLL(find_library('girepository-1.0'))

#
# GIBaseInfo
#
class _GIBaseInfoStub(Structure):
	_fields_ = [
		('dummy1', gint32),
		('dummy2', gint32),
		('dummy3', gpointer),
		('dummy4', gpointer),
		('dummy5', gpointer),
		('dummy6', guint32),
		('dummy7', guint32),
		('padding', gpointer * 4),
	]

class GIBaseInfo(Structure): pass

class GIAttributeIter(Structure): pass 

GIInfoType = gint
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
) = map(GIInfoType, range(20))

name_GIInfoType = (
	'GI_INFO_TYPE_INVALID',
	'GI_INFO_TYPE_FUNCTION',
	'GI_INFO_TYPE_CALLBACK',
	'GI_INFO_TYPE_STRUCT',
	'GI_INFO_TYPE_BOXED',
	'GI_INFO_TYPE_ENUM',
	'GI_INFO_TYPE_FLAGS',
	'GI_INFO_TYPE_OBJECT',
	'GI_INFO_TYPE_INTERFACE',
	'GI_INFO_TYPE_CONSTANT',
	'GI_INFO_TYPE_ERROR_DOMAIN',
	'GI_INFO_TYPE_UNION',
	'GI_INFO_TYPE_VALUE',
	'GI_INFO_TYPE_SIGNAL',
	'GI_INFO_TYPE_VFUNC',
	'GI_INFO_TYPE_PROPERTY',
	'GI_INFO_TYPE_FIELD',
	'GI_INFO_TYPE_ARG',
	'GI_INFO_TYPE_TYPE',
	'GI_INFO_TYPE_UNRESOLVED',
)

# GICallableInfo
class GICallableInfo(Structure): pass

# GIFunctionInfo
class GIFunctionInfo(Structure): pass

GInvokeError = gint
(
	G_INVOKE_ERROR_FAILED,
	G_INVOKE_ERROR_SYMBOL_NOT_FOUND,
	G_INVOKE_ERROR_ARGUMENT_MISMATCH
) = map(GInvokeError, range(3))

GIFunctionInfoFlags = gint
GI_FUNCTION_IS_METHOD = GIFunctionInfoFlags(1 << 0)
GI_FUNCTION_IS_CONSTRUCTOR = GIFunctionInfoFlags(1 << 1)
GI_FUNCTION_IS_GETTER = GIFunctionInfoFlags(1 << 2)
GI_FUNCTION_IS_SETTER = GIFunctionInfoFlags(1 << 3)
GI_FUNCTION_WRAPS_VFUNC = GIFunctionInfoFlags(1 << 4)
GI_FUNCTION_THROWS = GIFunctionInfoFlags(1 << 5)

name_GIFunctionInfoFlags = {
	1 << 0: 'GI_FUNCTION_IS_METHOD',
	1 << 1: 'GI_FUNCTION_IS_CONSTRUCTOR',
	1 << 2: 'GI_FUNCTION_IS_GETTER',
	1 << 3: 'GI_FUNCTION_IS_SETTER',
	1 << 4: 'GI_FUNCTION_WRAPS_VFUNC',
	1 << 5: 'GI_FUNCTION_THROWS',
}

# GISignalInfo
class GISignalInfo(Structure): pass

# GIVFuncInfo
class GIVFuncInfo(Structure): pass

GIVFuncInfoFlags = gint
GI_VFUNC_MUST_CHAIN_UP = GIVFuncInfoFlags(1 << 0)
GI_VFUNC_MUST_OVERRIDE = GIVFuncInfoFlags(1 << 1)
GI_VFUNC_MUST_NOT_OVERRIDE = GIVFuncInfoFlags(1 << 2)

name_GIVFuncInfoFlags =  {
	1 << 0: 'GI_VFUNC_MUST_CHAIN_UP',
	1 << 1: 'GI_VFUNC_MUST_OVERRIDE',
	1 << 2: 'GI_VFUNC_MUST_NOT_OVERRIDE',
}

# GIRegisteredTypeInfo
class GIRegisteredTypeInfo(Structure): pass

# GIEnumInfo
class GIEnumInfo(Structure): pass
class GIValueInfo(Structure): pass

# GIInterfaceInfo
class GIInterfaceInfo(Structure): pass

# GIObjectInfo
class GIObjectInfo(Structure): pass

# GIStructInfo
class GIStructInfo(Structure): pass

# GIUnionInfo
class GIUnionInfo(Structure): pass

# GIArgInfo
class GIArgInfo(Structure): pass

GIDirection = gint
(
	GI_DIRECTION_IN,
	GI_DIRECTION_OUT,
	GI_DIRECTION_INOUT,
) = map(GIDirection, range(3))

name_GIDirection = [
	'GI_DIRECTION_IN',
	'GI_DIRECTION_OUT',
	'GI_DIRECTION_INOUT',
]

GIScopeType = gint
(
	GI_SCOPE_TYPE_INVALID,
	GI_SCOPE_TYPE_CALL,
	GI_SCOPE_TYPE_ASYNC,
	GI_SCOPE_TYPE_NOTIFIED,
) = map(GIScopeType, range(4))

name_GIScopeType = [
	'GI_SCOPE_TYPE_INVALID',
	'GI_SCOPE_TYPE_CALL',
	'GI_SCOPE_TYPE_ASYNC',
	'GI_SCOPE_TYPE_NOTIFIED',
]

GITransfer = gint
(
	GI_TRANSFER_NOTHING,
	GI_TRANSFER_CONTAINER,
	GI_TRANSFER_EVERYTHING,
) = map(GITransfer, range(3))

name_GITransfer = [
	'GI_TRANSFER_NOTHING',
	'GI_TRANSFER_CONTAINER',
	'GI_TRANSFER_EVERYTHING',
]

# GIArgument
class GIArgument(Union):
	_fields_ = [
		('v_boolean', gboolean),
		('v_int8', gint8),
		('v_uint8', guint8),
		('v_int16', gint16),
		('v_uint16', guint16),
		('v_int32', gint32),
		('v_uint32', guint32),
		('v_int64', gint64),
		('v_uint64', guint64),
		('v_float', gfloat),
		('v_double', gdouble),
		('v_short', gshort),
		('v_ushort', gushort),
		('v_int', gint),
		('v_uint', guint),
		('v_long', glong),
		('v_ulong', gulong),
		('v_ssize', gssize),
		('v_size', gsize),
		('v_string', gchar_p),
		('v_pointer', gpointer),
	]

# GIConstantInfo
class GIConstantInfo(Structure): pass

# GIErrorDomainInfo
class GIErrorDomainInfo(Structure): pass

# GIFieldInfo
class GIFieldInfo(Structure): pass

GIFieldInfoFlags = gint
GI_FIELD_IS_READABLE = GIFieldInfoFlags(1 << 0)
GI_FIELD_IS_WRITABLE = GIFieldInfoFlags(1 << 1)

name_GIFieldInfoFlags = {
	1 << 0: 'GI_FIELD_IS_READABLE',
	1 << 1: 'GI_FIELD_IS_WRITABLE',
}

# GIPropertyInfo
class GIPropertyInfo(Structure): pass

# GITypeInfo
class GITypeInfo(Structure): pass

GIArrayType = gint
(
	GI_ARRAY_TYPE_C,
	GI_ARRAY_TYPE_ARRAY,
	GI_ARRAY_TYPE_PTR_ARRAY,
	GI_ARRAY_TYPE_BYTE_ARRAY
) = map(GIArrayType, range(4))

name_GIArrayType = [
	'GI_ARRAY_TYPE_C',
	'GI_ARRAY_TYPE_ARRAY',
	'GI_ARRAY_TYPE_PTR_ARRAY',
	'GI_ARRAY_TYPE_BYTE_ARRAY',
]

GITypeTag = gint
GI_TYPE_TAG_VOID = GITypeTag(0)
GI_TYPE_TAG_BOOLEAN = GITypeTag(1)
GI_TYPE_TAG_INT8 =  GITypeTag(2)
GI_TYPE_TAG_UINT8 =  GITypeTag(3)
GI_TYPE_TAG_INT16 =  GITypeTag(4)
GI_TYPE_TAG_UINT16 =  GITypeTag(5)
GI_TYPE_TAG_INT32 =  GITypeTag(6)
GI_TYPE_TAG_UINT32 =  GITypeTag(7)
GI_TYPE_TAG_INT64 =  GITypeTag(8)
GI_TYPE_TAG_UINT64 = GITypeTag(9)
GI_TYPE_TAG_FLOAT = GITypeTag(10)
GI_TYPE_TAG_DOUBLE = GITypeTag(11)
GI_TYPE_TAG_GTYPE = GITypeTag(12)
GI_TYPE_TAG_UTF8 = GITypeTag(13)
GI_TYPE_TAG_FILENAME = GITypeTag(14)
GI_TYPE_TAG_ARRAY = GITypeTag(15)
GI_TYPE_TAG_INTERFACE = GITypeTag(16)
GI_TYPE_TAG_GLIST = GITypeTag(17)
GI_TYPE_TAG_GSLIST = GITypeTag(18)
GI_TYPE_TAG_GHASH = GITypeTag(19)
GI_TYPE_TAG_ERROR = GITypeTag(20)

name_GITypeTag = {
	0: 'GI_TYPE_TAG_VOID',
	1: 'GI_TYPE_TAG_BOOLEAN',
	2: 'GI_TYPE_TAG_INT8',
	3: 'GI_TYPE_TAG_UINT8',
	4: 'GI_TYPE_TAG_INT16',
	5: 'GI_TYPE_TAG_UINT16',
	6: 'GI_TYPE_TAG_INT32',
	7: 'GI_TYPE_TAG_UINT32',
	8: 'GI_TYPE_TAG_INT64',
	9: 'GI_TYPE_TAG_UINT64',
	10: 'GI_TYPE_TAG_FLOAT',
	11: 'GI_TYPE_TAG_DOUBLE',
	12: 'GI_TYPE_TAG_GTYPE',
	13: 'GI_TYPE_TAG_UTF8',
	14: 'GI_TYPE_TAG_FILENAME',
	15: 'GI_TYPE_TAG_ARRAY',
	16: 'GI_TYPE_TAG_INTERFACE',
	17: 'GI_TYPE_TAG_GLIST',
	18: 'GI_TYPE_TAG_GSLIST',
	19: 'GI_TYPE_TAG_GHASH',
	20: 'GI_TYPE_TAG_ERROR',
}

#
# GIRepository
#
class GIRepository(Structure): pass
class GICallbackInfo(Structure): pass

# GIRepositoryError
GIRepositoryError = gint
(
	G_IREPOSITORY_ERROR_TYPELIB_NOT_FOUND,
	G_IREPOSITORY_ERROR_NAMESPACE_MISMATCH,
	G_IREPOSITORY_ERROR_NAMESPACE_VERSION_CONFLICT,
	G_IREPOSITORY_ERROR_LIBRARY_NOT_FOUND,
) = map(GIRepositoryError, range(4))

name_GIRepositoryError = [
	'G_IREPOSITORY_ERROR_TYPELIB_NOT_FOUND',
	'G_IREPOSITORY_ERROR_NAMESPACE_MISMATCH',
	'G_IREPOSITORY_ERROR_NAMESPACE_VERSION_CONFLICT',
	'G_IREPOSITORY_ERROR_LIBRARY_NOT_FOUND',
]

# GIRepositoryLoadFlags
GIRepositoryLoadFlags = gint
G_IREPOSITORY_LOAD_FLAG_LAZY = GIRepositoryLoadFlags(1 << 0)

name_GIRepositoryLoadFlags = {
	1 << 0: 'G_IREPOSITORY_LOAD_FLAG_LAZY',
}

#
# GITypelib
#
class GITypelib(Structure): pass
	
# Typelib binary format
GTypelibBlobType = gint
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
) = map(GTypelibBlobType, range(12))

name_GTypelibBlobType = [
	'BLOB_TYPE_INVALID',
	'BLOB_TYPE_FUNCTION',
	'BLOB_TYPE_CALLBACK',
	'BLOB_TYPE_STRUCT',
	'BLOB_TYPE_BOXED',
	'BLOB_TYPE_ENUM',
	'BLOB_TYPE_FLAGS',
	'BLOB_TYPE_OBJECT',
	'BLOB_TYPE_INTERFACE',
	'BLOB_TYPE_CONSTANT',
	'BLOB_TYPE_ERROR_DOMAIN',
	'BLOB_TYPE_UNION',
]

class Header(Structure): pass
class DirEntry(Structure): pass
class ArgBlob(Structure): pass
class SignatureBlob(Structure): pass
class CommonBlob(Structure): pass
class FunctionBlob(Structure): pass
class CallbackBlob(Structure): pass
class InterfaceTypeBlob(Structure): pass
class ParamTypeBlob(Structure): pass
class ErrorTypeBlob(Structure): pass
class ErrorDomainBlob(Structure): pass
class ValueBlob(Structure): pass
class FieldBlob(Structure): pass
class RegisteredTypeBlob(Structure): pass
class StructBlob(Structure): pass
class UnionBlob(Structure): pass
class EnumBlob(Structure): pass
class PropertyBlob(Structure): pass
class SignalBlob(Structure): pass
class VFuncBlob(Structure): pass
class ObjectBlob(Structure): pass
class InterfaceBlob(Structure): pass
class ConstantBlob(Structure): pass
class AttributeBlob(Structure): pass
class dimensions(Structure): pass

#
# GIRepository
#
g_irepository_get_default = ctypes_get_func(
	libgirepository,
	'g_irepository_get_default',
	POINTER(GIRepository),
)

g_irepository_prepend_search_path = ctypes_get_func(
	libgirepository,
	'g_irepository_prepend_search_path',
	None,
	gchar_p,
)

g_irepository_get_search_path = ctypes_get_func(
	libgirepository,
	'g_irepository_get_search_path',
	POINTER(GSList),
)

g_irepository_load_typelib = ctypes_get_func(
	libgirepository,
	'g_irepository_load_typelib',
	gchar_p,
	POINTER(GIRepository),
	POINTER(GITypelib),
	GIRepositoryLoadFlags,
	POINTER(POINTER(GError)),
)

g_irepository_is_registered = ctypes_get_func(
	libgirepository,
	'g_irepository_is_registered',
	gint,
	POINTER(GIRepository),
	gchar_p,
	gchar_p,
)

g_irepository_find_by_name = ctypes_get_func(
	libgirepository,
	'g_irepository_find_by_name',
	POINTER(GIBaseInfo),
	POINTER(GIRepository),
	gchar_p,
	gchar_p,
)

g_irepository_require = ctypes_get_func(
	libgirepository,
	'g_irepository_require',
	POINTER(GITypelib),
	POINTER(GIRepository),
	gchar_p,
	gchar_p,
	GIRepositoryLoadFlags,
	POINTER(POINTER(GError)),
)

g_irepository_require_private = ctypes_get_func(
	libgirepository,
	'g_irepository_require_private',
	POINTER(GITypelib),
	POINTER(GIRepository),
	gchar_p,
	gchar_p,
	gchar_p,
	GIRepositoryLoadFlags,
	POINTER(POINTER(GError)),
)

g_irepository_get_dependencies = ctypes_get_func(
	libgirepository,
	'g_irepository_get_dependencies',
	POINTER(gchar_p),
	POINTER(GIRepository),
	gchar_p,
)

g_irepository_get_loaded_namespaces = ctypes_get_func(
	libgirepository,
	'g_irepository_get_loaded_namespaces',
	POINTER(gchar_p),
	POINTER(GIRepository),
)

g_irepository_find_by_gtype = ctypes_get_func(
	libgirepository,
	'g_irepository_find_by_gtype',
	POINTER(GIBaseInfo),
	POINTER(GIRepository),
	GType
)

g_irepository_get_n_infos = ctypes_get_func(
	libgirepository,
	'g_irepository_get_n_infos',
	gint,
	POINTER(GIRepository),
	gchar_p,
)

g_irepository_get_info = ctypes_get_func(
	libgirepository,
	'g_irepository_get_info',
	POINTER(GIBaseInfo),
	POINTER(GIRepository),
	gchar_p,
	gint,
)

g_irepository_get_typelib_path = ctypes_get_func(
	libgirepository,
	'g_irepository_get_typelib_path',
	gchar_p,
	POINTER(GIRepository),
	gchar_p,
)

g_irepository_get_shared_library = ctypes_get_func(
	libgirepository,
	'g_irepository_get_shared_library',
	gchar_p,
	POINTER(GIRepository),
	gchar_p,
)

g_irepository_get_version = ctypes_get_func(
	libgirepository,
	'g_irepository_get_version',
	gchar_p,
	POINTER(GIRepository),
	gchar_p,
)

g_irepository_get_option_group = ctypes_get_func(
	libgirepository,
	'g_irepository_get_option_group',
	POINTER(GOptionGroup),
)

g_irepository_get_c_prefix = ctypes_get_func(
	libgirepository,
	'g_irepository_get_c_prefix',
	gchar_p,
	POINTER(GIRepository),
	gchar_p,
)

g_irepository_dump = ctypes_get_func(
	libgirepository,
	'g_irepository_dump',
	gint,
	gchar_p,
	POINTER(POINTER(GError)),
)

g_irepository_enumerate_versions = ctypes_get_func(
	libgirepository,
	'g_irepository_enumerate_versions',
	POINTER(GList),
	POINTER(GIRepository),
	gchar_p,
)

g_typelib_new_from_memory = ctypes_get_func(
	libgirepository,
	'g_typelib_new_from_memory',
	POINTER(GITypelib),
	POINTER(guint8),
	gulong,
	POINTER(POINTER(GError)),
)

g_typelib_new_from_const_memory = ctypes_get_func(
	libgirepository,
	'g_typelib_new_from_const_memory',
	POINTER(GITypelib),
	POINTER(guint8),
	gulong,
	POINTER(POINTER(GError)),
)

g_typelib_new_from_mapped_file = ctypes_get_func(
	libgirepository,
	'g_typelib_new_from_mapped_file',
	POINTER(GITypelib),
	POINTER(GMappedFile),
	POINTER(POINTER(GError)),
)

g_typelib_free = ctypes_get_func(
	libgirepository,
	'g_typelib_free',
	None,
	POINTER(GITypelib),
)

g_typelib_symbol = ctypes_get_func(
	libgirepository,
	'g_typelib_symbol',
	gint,
	POINTER(GITypelib),
	gchar_p,
	gpointer,
)

g_typelib_get_namespace = ctypes_get_func(
	libgirepository,
	'g_typelib_get_namespace',
	gchar_p,
	POINTER(GITypelib),
)

#
# GIBaseInfo
#
g_info_type_to_string = ctypes_get_func(
	libgirepository,
	'g_info_type_to_string',
	gchar_p,
	GIInfoType,
)

g_base_info_ref = ctypes_get_func(
	libgirepository,
	'g_base_info_ref',
	POINTER(GIBaseInfo),
	POINTER(GIBaseInfo),
)

g_base_info_unref = ctypes_get_func(
	libgirepository,
	'g_base_info_unref',
	None,
	POINTER(GIBaseInfo),
)

g_base_info_get_type = ctypes_get_func(
	libgirepository,
	'g_base_info_get_type',
	GIInfoType,
	POINTER(GIBaseInfo),
)

g_base_info_get_name = ctypes_get_func(
	libgirepository,
	'g_base_info_get_name',
	gchar_p,
	POINTER(GIBaseInfo),
)

g_base_info_get_namespace = ctypes_get_func(
	libgirepository,
	'g_base_info_get_namespace',
	gchar_p,
	POINTER(GIBaseInfo),
)

g_base_info_is_deprecated = ctypes_get_func(
	libgirepository,
	'g_base_info_is_deprecated',
	gint,
	POINTER(GIBaseInfo),
)

g_base_info_get_attribute = ctypes_get_func(
	libgirepository,
	'g_base_info_get_attribute',
	gchar_p,
	POINTER(GIBaseInfo),
	gchar_p,
)

g_base_info_iterate_attributes = ctypes_get_func(
	libgirepository,
	'g_base_info_iterate_attributes',
	gint,
	POINTER(GIBaseInfo),
	POINTER(GIAttributeIter),
	gchar_p,
	gchar_p,
)

g_base_info_get_container = ctypes_get_func(
	libgirepository,
	'g_base_info_get_container',
	POINTER(GIBaseInfo),
	POINTER(GIBaseInfo),
)

g_base_info_get_typelib = ctypes_get_func(
	libgirepository,
	'g_base_info_get_typelib',
	POINTER(GITypelib),
	POINTER(GIBaseInfo),
)

g_base_info_equal = ctypes_get_func(
	libgirepository,
	'g_base_info_equal',
	gint,
	POINTER(GIBaseInfo),
	POINTER(GIBaseInfo),
)

#
# GIFunctionInfo
#
g_function_info_get_symbol = ctypes_get_func(
	libgirepository,
	'g_function_info_get_symbol',
	gchar_p,
	POINTER(GIFunctionInfo),
)

g_function_info_get_flags = ctypes_get_func(
	libgirepository,
	'g_function_info_get_flags',
	GIFunctionInfoFlags,
	POINTER(GIFunctionInfo),
)

g_function_info_get_property = ctypes_get_func(
	libgirepository,
	'g_function_info_get_property',
	POINTER(GIPropertyInfo),
	POINTER(GIFunctionInfo),
)

g_function_info_get_vfunc = ctypes_get_func(
	libgirepository,
	'g_function_info_get_vfunc',
	POINTER(GIVFuncInfo),
	POINTER(GIFunctionInfo),
)

g_function_info_invoke = ctypes_get_func(
	libgirepository,
	'g_function_info_invoke',
	gint,
	POINTER(GIFunctionInfo),
	POINTER(GIArgument),
	gint,
	POINTER(GIArgument),
	gint,
	POINTER(GIArgument),
	POINTER(POINTER(GError)),
)

#
# GICallableInfo
#
g_callable_info_get_return_type = ctypes_get_func(
	libgirepository,
	'g_callable_info_get_return_type',
	POINTER(GITypeInfo),
	POINTER(GICallableInfo),
)

g_callable_info_get_caller_owns = ctypes_get_func(
	libgirepository,
	'g_callable_info_get_caller_owns',
	GITransfer,
	POINTER(GICallableInfo),
)

g_callable_info_may_return_null = ctypes_get_func(
	libgirepository,
	'g_callable_info_may_return_null',
	gint,
	POINTER(GICallableInfo),
)

g_callable_info_get_return_attribute = ctypes_get_func(
	libgirepository,
	'g_callable_info_get_return_attribute',
	gchar_p,
	POINTER(GICallableInfo),
	gchar_p,
)

g_callable_info_iterate_return_attributes = ctypes_get_func(
	libgirepository,
	'g_callable_info_iterate_return_attributes',
	gchar_p,
	POINTER(GICallableInfo),
	POINTER(GIAttributeIter),
	POINTER(gchar_p),
	POINTER(gchar_p),
)

g_callable_info_get_n_args = ctypes_get_func(
	libgirepository,
	'g_callable_info_get_n_args',
	gint,
	POINTER(GICallableInfo),
)

g_callable_info_get_arg = ctypes_get_func(
	libgirepository,
	'g_callable_info_get_arg',
	POINTER(GIArgInfo),
	POINTER(GICallableInfo),
	gint,
)

g_callable_info_load_arg = ctypes_get_func(
	libgirepository,
	'g_callable_info_load_arg',
	None,
	POINTER(GICallableInfo),
	gint,
	POINTER(GIArgInfo),
)

g_callable_info_load_return_type = ctypes_get_func(
	libgirepository,
	'g_callable_info_load_return_type',
	None,
	POINTER(GICallableInfo),
	POINTER(GITypeInfo),
)

#
# GIArgInfo
#
g_arg_info_get_direction = ctypes_get_func(
	libgirepository,
	'g_arg_info_get_direction',
	GIDirection,
	POINTER(GIArgInfo),
)

g_arg_info_is_caller_allocates = ctypes_get_func(
	libgirepository,
	'g_arg_info_is_caller_allocates',
	gint,
	POINTER(GIArgInfo),
)

g_arg_info_is_return_value = ctypes_get_func(
	libgirepository,
	'g_arg_info_is_return_value',
	gint,
	POINTER(GIArgInfo),
)

g_arg_info_is_optional = ctypes_get_func(
	libgirepository,
	'g_arg_info_is_optional',
	gint,
	POINTER(GIArgInfo),
)

g_arg_info_may_be_null = ctypes_get_func(
	libgirepository,
	'g_arg_info_may_be_null',
	gint,
	POINTER(GIArgInfo),
)

g_arg_info_get_ownership_transfer = ctypes_get_func(
	libgirepository,
	'g_arg_info_get_ownership_transfer',
	GITransfer,
	POINTER(GIArgInfo),
)

g_arg_info_get_scope = ctypes_get_func(
	libgirepository,
	'g_arg_info_get_scope',
	GIScopeType,
	POINTER(GIArgInfo),
)

g_arg_info_get_closure = ctypes_get_func(
	libgirepository,
	'g_arg_info_get_closure',
	gint,
	POINTER(GIArgInfo),
)

g_arg_info_get_destroy = ctypes_get_func(
	libgirepository,
	'g_arg_info_get_destroy',
	gint,
	POINTER(GIArgInfo),
)

g_arg_info_get_type = ctypes_get_func(
	libgirepository,
	'g_arg_info_get_type',
	POINTER(GITypeInfo),
	POINTER(GIArgInfo),
)

g_arg_info_load_type = ctypes_get_func(
	libgirepository,
	'g_arg_info_load_type',
	None,
	POINTER(GIArgInfo),
	POINTER(GITypeInfo),
)

#
# GITypeInfo
#
g_type_tag_to_string = ctypes_get_func(
	libgirepository,
	'g_type_tag_to_string',
	gchar_p,
	GITypeTag,
)

g_type_info_is_pointer = ctypes_get_func(
	libgirepository,
	'g_type_info_is_pointer',
	gboolean,
	POINTER(GITypeInfo),
)

g_type_info_get_tag = ctypes_get_func(
	libgirepository,
	'g_type_info_get_tag',
	GITypeTag,
	POINTER(GITypeInfo),
)

g_type_info_get_param_type = ctypes_get_func(
	libgirepository,
	'g_type_info_get_param_type',
	POINTER(GITypeInfo),
	POINTER(GITypeInfo),
	gint
)

g_type_info_get_interface = ctypes_get_func(
	libgirepository,
	'g_type_info_get_interface',
	POINTER(GIBaseInfo),
	POINTER(GITypeInfo),
)

g_type_info_get_array_length = ctypes_get_func(
	libgirepository,
	'g_type_info_get_array_length',
	gint,
	POINTER(GITypeInfo),
)

g_type_info_get_array_fixed_size = ctypes_get_func(
	libgirepository,
	'g_type_info_get_array_fixed_size',
	gint,
	POINTER(GITypeInfo),
)

g_type_info_is_zero_terminated = ctypes_get_func(
	libgirepository,
	'g_type_info_is_zero_terminated',
	gboolean,
	POINTER(GITypeInfo),
)

g_type_info_get_n_error_domains = ctypes_get_func(
	libgirepository,
	'g_type_info_get_n_error_domains',
	gint,
	POINTER(GITypeInfo),
)

g_type_info_get_error_domain = ctypes_get_func(
	libgirepository,
	'g_type_info_get_error_domain',
	POINTER(GIErrorDomainInfo),
	POINTER(GITypeInfo),
	gint,
)

g_type_info_get_array_type = ctypes_get_func(
	libgirepository,
	'g_type_info_get_array_type',
	GIArrayType,
	POINTER(GITypeInfo),
)

#
# GIStructInfo
#
g_struct_info_get_n_fields = ctypes_get_func(
	libgirepository,
	'g_struct_info_get_n_fields',
	gint,
	POINTER(GIStructInfo),
)

g_struct_info_get_field = ctypes_get_func(
	libgirepository,
	'g_struct_info_get_field',
	POINTER(GIFieldInfo),
	POINTER(GIStructInfo),
	gint,
)

g_struct_info_get_n_methods = ctypes_get_func(
	libgirepository,
	'g_struct_info_get_n_methods',
	gint,
	POINTER(GIStructInfo),
)

g_struct_info_get_method = ctypes_get_func(
	libgirepository,
	'g_struct_info_get_method',
	POINTER(GIFunctionInfo),
	POINTER(GIStructInfo),
	gint,
)

g_struct_info_find_method = ctypes_get_func(
	libgirepository,
	'g_struct_info_find_method',
	POINTER(GIFunctionInfo),
	POINTER(GIStructInfo),
	gchar_p,
)

g_struct_info_get_size = ctypes_get_func(
	libgirepository,
	'g_struct_info_get_size',
	gsize,
	POINTER(GIStructInfo),
)

g_struct_info_get_alignment = ctypes_get_func(
	libgirepository,
	'g_struct_info_get_alignment',
	gsize,
	POINTER(GIStructInfo),
)

g_struct_info_is_gtype_struct = ctypes_get_func(
	libgirepository,
	'g_struct_info_is_gtype_struct',
	gboolean,
	POINTER(GIStructInfo),
)

g_struct_info_is_foreign = ctypes_get_func(
	libgirepository,
	'g_struct_info_is_foreign',
	gboolean,
	POINTER(GIStructInfo),
)

#
# GIUnionInfo
#
g_union_info_get_n_fields = ctypes_get_func(
	libgirepository,
	'g_union_info_get_n_fields',
	gint,
	POINTER(GIUnionInfo),
)

g_union_info_get_field = ctypes_get_func(
	libgirepository,
	'g_union_info_get_field',
	POINTER(GIFieldInfo),
	POINTER(GIUnionInfo),
	gint,
)

g_union_info_get_n_methods = ctypes_get_func(
	libgirepository,
	'g_union_info_get_n_methods',
	gint,
	POINTER(GIUnionInfo),
)

g_union_info_get_method = ctypes_get_func(
	libgirepository,
	'g_union_info_get_method',
	POINTER(GIFunctionInfo),
	POINTER(GIUnionInfo),
	gint,
)

g_union_info_is_discriminated = ctypes_get_func(
	libgirepository,
	'g_union_info_is_discriminated',
	gboolean,
	POINTER(GIUnionInfo),
)

g_union_info_get_discriminator_offset = ctypes_get_func(
	libgirepository,
	'g_union_info_get_discriminator_offset',
	gint,
	POINTER(GIUnionInfo),
)

g_union_info_get_discriminator_type = ctypes_get_func(
	libgirepository,
	'g_union_info_get_discriminator_type',
	POINTER(GITypeInfo),
	POINTER(GIUnionInfo),
)

g_union_info_get_discriminator = ctypes_get_func(
	libgirepository,
	'g_union_info_get_discriminator',
	POINTER(GIConstantInfo),
	POINTER(GIUnionInfo),
	gint,
)

g_union_info_find_method = ctypes_get_func(
	libgirepository,
	'g_union_info_find_method',
	POINTER(GIFunctionInfo),
	POINTER(GIUnionInfo),
	gchar_p,
)

g_union_info_get_size = ctypes_get_func(
	libgirepository,
	'g_union_info_get_size',
	gsize,
	POINTER(GIUnionInfo),
)

g_union_info_get_alignment = ctypes_get_func(
	libgirepository,
	'g_union_info_get_alignment',
	gsize,
	POINTER(GIUnionInfo),
)

#
# GIFieldInfo
#
g_field_info_get_flags = ctypes_get_func(
	libgirepository,
	'g_field_info_get_flags',
	GIFieldInfoFlags,
	POINTER(GIFieldInfo),
)

g_field_info_get_size = ctypes_get_func(
	libgirepository,
	'g_field_info_get_size',
	gint,
	POINTER(GIFieldInfo),
)

g_field_info_get_offset = ctypes_get_func(
	libgirepository,
	'g_field_info_get_offset',
	gint,
	POINTER(GIFieldInfo),
)

g_field_info_get_type = ctypes_get_func(
	libgirepository,
	'g_field_info_get_type',
	POINTER(GITypeInfo),
	POINTER(GIFieldInfo),
)

g_field_info_get_field = ctypes_get_func(
	libgirepository,
	'g_field_info_get_field',
	gboolean,
	POINTER(GIFieldInfo),
	gpointer,
	POINTER(GIArgument),
)

g_field_info_set_field = ctypes_get_func(
	libgirepository,
	'g_field_info_set_field',
	gboolean,
	POINTER(GIFieldInfo),
	gpointer,
	POINTER(GIArgument),
)

#
# GIPropertyInfo
#
g_property_info_get_flags = ctypes_get_func(
	libgirepository,
	'g_property_info_get_flags',
	GParamFlags,
	POINTER(GIPropertyInfo),
)

g_property_info_get_type = ctypes_get_func(
	libgirepository,
	'g_property_info_get_type',
	POINTER(GITypeInfo),
	POINTER(GIPropertyInfo),
)

g_property_info_get_ownership_transfer = ctypes_get_func(
	libgirepository,
	'g_property_info_get_ownership_transfer',
	GITransfer,
	POINTER(GIPropertyInfo),
)

#
# GIVFuncInfo
#
g_vfunc_info_get_flags = ctypes_get_func(
	libgirepository,
	'g_vfunc_info_get_flags',
	GIVFuncInfoFlags,
	POINTER(GIVFuncInfo),
)

g_vfunc_info_get_offset = ctypes_get_func(
	libgirepository,
	'g_vfunc_info_get_offset',
	gint,
	POINTER(GIVFuncInfo),
)

g_vfunc_info_get_signal = ctypes_get_func(
	libgirepository,
	'g_vfunc_info_get_signal',
	POINTER(GISignalInfo),
	POINTER(GIVFuncInfo),
)

g_vfunc_info_get_invoker = ctypes_get_func(
	libgirepository,
	'g_vfunc_info_get_invoker',
	POINTER(GIFunctionInfo),
	POINTER(GIVFuncInfo),
)

#
# GISignalInfo
#
g_signal_info_get_flags = ctypes_get_func(
	libgirepository,
	'g_signal_info_get_flags',
	GSignalFlags,
	POINTER(GISignalInfo),
)

g_signal_info_get_class_closure = ctypes_get_func(
	libgirepository,
	'g_signal_info_get_class_closure',
	POINTER(GIVFuncInfo),
	POINTER(GISignalInfo),
)

g_signal_info_true_stops_emit = ctypes_get_func(
	libgirepository,
	'g_signal_info_true_stops_emit',
	gboolean,
	POINTER(GISignalInfo),
)

#
# GIEnumInfo
#
g_enum_info_get_n_values = ctypes_get_func(
	libgirepository,
	'g_enum_info_get_n_values',
	gint,
	POINTER(GIEnumInfo),
)

g_enum_info_get_value = ctypes_get_func(
	libgirepository,
	'g_enum_info_get_value',
	POINTER(GIValueInfo),
	POINTER(GIEnumInfo),
	gint,
)

g_enum_info_get_storage_type = ctypes_get_func(
	libgirepository,
	'g_enum_info_get_storage_type',
	GITypeTag,
	POINTER(GIEnumInfo),
)

g_value_info_get_value = ctypes_get_func(
	libgirepository,
	'g_value_info_get_value',
	glong,
	POINTER(GIValueInfo),
)

#
# GIRegisteredTypeInfo
#
g_registered_type_info_get_type_name = ctypes_get_func(
	libgirepository,
	'g_registered_type_info_get_type_name',
	gchar_p,
	POINTER(GIRegisteredTypeInfo),
)

g_registered_type_info_get_type_init = ctypes_get_func(
	libgirepository,
	'g_registered_type_info_get_type_init',
	gchar_p,
	POINTER(GIRegisteredTypeInfo),
)

g_registered_type_info_get_g_type = ctypes_get_func(
	libgirepository,
	'g_registered_type_info_get_g_type',
	GType,
	POINTER(GIRegisteredTypeInfo),
)

#
# GIObjectInfo
#
GIObjectInfoGetValueFunction = CFUNCTYPE(c_void_p, POINTER(GValue))
GIObjectInfoRefFunction = CFUNCTYPE(c_void_p, c_void_p)
GIObjectInfoSetValueFunction = CFUNCTYPE(None, POINTER(GValue), c_void_p)
GIObjectInfoUnrefFunction = CFUNCTYPE(None, c_void_p)

g_object_info_get_type_name = ctypes_get_func(
	libgirepository,
	'g_object_info_get_type_name',
	gchar_p,
	POINTER(GIObjectInfo),
)

g_object_info_get_type_init = ctypes_get_func(
	libgirepository,
	'g_object_info_get_type_init',
	gchar_p,
	POINTER(GIObjectInfo),
)

g_object_info_get_abstract = ctypes_get_func(
	libgirepository,
	'g_object_info_get_abstract',
	gboolean,
	POINTER(GIObjectInfo),
)

g_object_info_get_fundamental = ctypes_get_func(
	libgirepository,
	'g_object_info_get_fundamental',
	gboolean,
	POINTER(GIObjectInfo),
)

g_object_info_get_parent = ctypes_get_func(
	libgirepository,
	'g_object_info_get_parent',
	POINTER(GIObjectInfo),
	POINTER(GIObjectInfo),
)

g_object_info_get_n_interfaces = ctypes_get_func(
	libgirepository,
	'g_object_info_get_n_interfaces',
	gint,
	POINTER(GIObjectInfo),
)

g_object_info_get_interface = ctypes_get_func(
	libgirepository,
	'g_object_info_get_interface',
	POINTER(GIInterfaceInfo),
	POINTER(GIObjectInfo),
	gint,
)

g_object_info_get_n_fields = ctypes_get_func(
	libgirepository,
	'g_object_info_get_n_fields',
	gint,
	POINTER(GIObjectInfo),
)

g_object_info_get_field = ctypes_get_func(
	libgirepository,
	'g_object_info_get_field',
	POINTER(GIFieldInfo),
	POINTER(GIObjectInfo),
	gint,
)

g_object_info_get_n_properties = ctypes_get_func(
	libgirepository,
	'g_object_info_get_n_properties',
	gint,
	POINTER(GIObjectInfo),
)

g_object_info_get_property = ctypes_get_func(
	libgirepository,
	'g_object_info_get_property',
	POINTER(GIPropertyInfo),
	POINTER(GIObjectInfo),
	gint,
)

g_object_info_get_n_methods = ctypes_get_func(
	libgirepository,
	'g_object_info_get_n_methods',
	gint,
	POINTER(GIObjectInfo),
)

g_object_info_get_method = ctypes_get_func(
	libgirepository,
	'g_object_info_get_method',
	POINTER(GIFunctionInfo),
	POINTER(GIObjectInfo),
	gint,
)

g_object_info_find_method = ctypes_get_func(
	libgirepository,
	'g_object_info_find_method',
	POINTER(GIFunctionInfo),
	POINTER(GIObjectInfo),
	gchar_p,
)

g_object_info_get_n_signals = ctypes_get_func(
	libgirepository,
	'g_object_info_get_n_signals',
	gint,
	POINTER(GIObjectInfo),
)

g_object_info_get_signal = ctypes_get_func(
	libgirepository,
	'g_object_info_get_signal',
	POINTER(GISignalInfo),
	POINTER(GIObjectInfo),
	gint,
)

g_object_info_get_n_vfuncs = ctypes_get_func(
	libgirepository,
	'g_object_info_get_n_vfuncs',
	gint,
	POINTER(GIObjectInfo),
)

g_object_info_get_vfunc = ctypes_get_func(
	libgirepository,
	'g_object_info_get_vfunc',
	POINTER(GIVFuncInfo),
	POINTER(GIObjectInfo),
	gint,
)

g_object_info_get_n_constants = ctypes_get_func(
	libgirepository,
	'g_object_info_get_n_constants',
	gint,
	POINTER(GIObjectInfo),
)

g_object_info_get_constant = ctypes_get_func(
	libgirepository,
	'g_object_info_get_constant',
	POINTER(GIConstantInfo),
	POINTER(GIObjectInfo),
	gint,
)

g_object_info_get_class_struct = ctypes_get_func(
	libgirepository,
	'g_object_info_get_class_struct',
	POINTER(GIStructInfo),
	POINTER(GIObjectInfo),
)

g_object_info_find_vfunc = ctypes_get_func(
	libgirepository,
	'g_object_info_find_vfunc',
	POINTER(GIVFuncInfo),
	POINTER(GIObjectInfo),
	gchar_p,
)

g_object_info_get_unref_function = ctypes_get_func(
	libgirepository,
	'g_object_info_get_unref_function',
	gchar_p,
	POINTER(GIObjectInfo),
)

g_object_info_get_unref_function_pointer = ctypes_get_func(
	libgirepository,
	'g_object_info_get_unref_function_pointer',
	GIObjectInfoUnrefFunction,
	POINTER(GIObjectInfo),
)

g_object_info_get_ref_function = ctypes_get_func(
	libgirepository,
	'g_object_info_get_ref_function',
	gchar_p,
	POINTER(GIObjectInfo),
)

g_object_info_get_ref_function_pointer = ctypes_get_func(
	libgirepository,
	'g_object_info_get_ref_function_pointer',
	GIObjectInfoRefFunction,
	POINTER(GIObjectInfo),
)

g_object_info_get_set_value_function = ctypes_get_func(
	libgirepository,
	'g_object_info_get_set_value_function',
	gchar_p,
	POINTER(GIObjectInfo),
)

g_object_info_get_set_value_function_pointer = ctypes_get_func(
	libgirepository,
	'g_object_info_get_set_value_function_pointer',
	GIObjectInfoSetValueFunction,
	POINTER(GIObjectInfo),
)

g_object_info_get_get_value_function = ctypes_get_func(
	libgirepository,
	'g_object_info_get_get_value_function',
	gchar_p,
	POINTER(GIObjectInfo),
)

g_object_info_get_get_value_function_pointer = ctypes_get_func(
	libgirepository,
	'g_object_info_get_get_value_function_pointer',
	GIObjectInfoGetValueFunction,
	POINTER(GIObjectInfo),
)

#
# GIInterfaceInfo
#
g_interface_info_get_n_prerequisites = ctypes_get_func(
	libgirepository,
	'g_interface_info_get_n_prerequisites',
	gint,
	POINTER(GIInterfaceInfo),
)

g_interface_info_get_prerequisite = ctypes_get_func(
	libgirepository,
	'g_interface_info_get_prerequisite',
	POINTER(GIBaseInfo),
	POINTER(GIInterfaceInfo),
	gint,
)

g_interface_info_get_n_properties = ctypes_get_func(
	libgirepository,
	'g_interface_info_get_n_properties',
	gint,
	POINTER(GIInterfaceInfo),
)

g_interface_info_get_property = ctypes_get_func(
	libgirepository,
	'g_interface_info_get_property',
	POINTER(GIPropertyInfo),
	POINTER(GIInterfaceInfo),
	gint,
)

g_interface_info_get_n_methods = ctypes_get_func(
	libgirepository,
	'g_interface_info_get_n_methods',
	gint,
	POINTER(GIInterfaceInfo),
)

g_interface_info_get_method = ctypes_get_func(
	libgirepository,
	'g_interface_info_get_method',
	POINTER(GIFunctionInfo),
	POINTER(GIInterfaceInfo),
	gint,
)

g_interface_info_find_method = ctypes_get_func(
	libgirepository,
	'g_interface_info_find_method',
	POINTER(GIFunctionInfo),
	POINTER(GIInterfaceInfo),
	gchar_p,
)

g_interface_info_get_n_signals = ctypes_get_func(
	libgirepository,
	'g_interface_info_get_n_signals',
	gint,
	POINTER(GIInterfaceInfo),
)

g_interface_info_get_signal = ctypes_get_func(
	libgirepository,
	'g_interface_info_get_signal',
	POINTER(GISignalInfo),
	POINTER(GIInterfaceInfo),
	gint,
)

g_interface_info_get_n_vfuncs = ctypes_get_func(
	libgirepository,
	'g_interface_info_get_n_vfuncs',
	gint,
	POINTER(GIInterfaceInfo),
)

g_interface_info_get_vfunc = ctypes_get_func(
	libgirepository,
	'g_interface_info_get_vfunc',
	POINTER(GIVFuncInfo),
	POINTER(GIInterfaceInfo),
	gint,
)

g_interface_info_get_n_constants = ctypes_get_func(
	libgirepository,
	'g_interface_info_get_n_constants',
	gint,
	POINTER(GIInterfaceInfo),
)

g_interface_info_get_constant = ctypes_get_func(
	libgirepository,
	'g_interface_info_get_constant',
	POINTER(GIConstantInfo),
	POINTER(GIInterfaceInfo),
	gint,
)

g_interface_info_get_iface_struct = ctypes_get_func(
	libgirepository,
	'g_interface_info_get_iface_struct',
	POINTER(GIStructInfo),
	POINTER(GIInterfaceInfo),
)

g_interface_info_find_vfunc = ctypes_get_func(
	libgirepository,
	'g_interface_info_find_vfunc',
	POINTER(GIVFuncInfo),
	POINTER(GIInterfaceInfo),
	gchar_p,
)

#
# GIConstantInfo
#
g_constant_info_get_type = ctypes_get_func(
	libgirepository,
	'g_constant_info_get_type',
	POINTER(GITypeInfo),
	POINTER(GIConstantInfo),
)

g_constant_info_get_value = ctypes_get_func(
	libgirepository,
	'g_constant_info_get_value',
	gint,
	POINTER(GIConstantInfo),
	POINTER(GIArgument),
)

#
# GIErrorDomainInfo
#
g_error_domain_info_get_quark = ctypes_get_func(
	libgirepository,
	'g_error_domain_info_get_quark',
	gchar_p,
	POINTER(GIErrorDomainInfo),
)

g_error_domain_info_get_codes = ctypes_get_func(
	libgirepository,
	'g_error_domain_info_get_codes',
	POINTER(GIInterfaceInfo),
	POINTER(GIErrorDomainInfo),
)
