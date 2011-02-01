import os
import sys

# other imports
from ctypes import *

# dynamic libs
libgo = CDLL('libgobject-2.0.so')
libgir = CDLL('libgirepository-1.0.so')

# util
def ctypes_get_funcptr(lib, name, restype=None, *argtypes):
	func = getattr(lib, name)
	func.restype = restype
	func.argtypes = argtypes
	return func

# Glib
class struct_GObject(Structure): pass
typedef_GType = c_int
class struct_GError(Structure): pass
class struct_GList(Structure): pass
class struct_GSList(Structure): pass
class struct_GOptionGroup(Structure): pass
class struct_GMappedFile(Structure): pass

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

# GISignalInfo
class struct_GISignalInfo(struct_GICallableInfo): pass

# GIVFuncInfo
class struct_GIVFuncInfo(struct_GICallableInfo): pass

enum_GIVFuncInfoFlags = c_int
enum_GI_VFUNC_MUST_CHAIN_UP = c_int(1 << 0)
enum_GI_VFUNC_MUST_OVERRIDE = c_int(1 << 1)
enum_GI_VFUNC_MUST_NOT_OVERRIDE = c_int(1 << 2)

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

enum_GIScopeType = c_int
(
	enum_GI_SCOPE_TYPE_INVALID,
	enum_GI_SCOPE_TYPE_CALL,
	enum_GI_SCOPE_TYPE_ASYNC,
	enum_GI_SCOPE_TYPE_NOTIFIED,
) = map(c_int, range(4))

enum_GITransfer = c_int
(
	enum_GI_TRANSFER_NOTHING,
	enum_GI_TRANSFER_CONTAINER,
	enum_GI_TRANSFER_EVERYTHING,
) = map(c_int, range(3))

# GIArgument
class union_GIArgument(Union):
	_fields_ = [
		('v_boolean', c_int),		# gboolean v_boolean;
		('v_int8', c_byte),			# gint8    v_int8;
		('v_uint8', c_ubyte),		# guint8   v_uint8;
		('v_int16', c_short),		# gint16   v_int16;
		('v_uint16', c_ushort),		# guint16  v_uint16;
		('v_int32', c_int),			# gint32   v_int32;
		('v_uint32', c_uint),		# guint32  v_uint32;
		('v_int64', c_longlong),	# gint64   v_int64;
		('v_uint64', c_ulonglong),	# guint64  v_uint64;
		('v_float', c_float),		# gfloat   v_float;
		('v_double', c_double),		# gdouble  v_double;
		('v_short', c_short),		# gshort   v_short;
		('v_ushort', c_ushort),		# gushort  v_ushort;
		('v_int', c_int),			# gint     v_int;
		('v_uint', c_uint),			# guint    v_uint;
		('v_long', c_long),			# glong    v_long;
		('v_ulong', c_ulong),		# gulong   v_ulong;
		('v_ssize', c_long),		# gssize   v_ssize;
		('v_size', c_ulong),		# gsize    v_size;
		('v_string', c_char_p),		# gchar *  v_string;
		('v_pointer', c_void_p),	# gpointer v_pointer;
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

enum_GITypeTag = c_int
GI_TYPE_TAG_VOID = c_int(0)
GI_TYPE_TAG_BOOLEAN = c_int(1)
GI_TYPE_TAG_INT8 =  c_int(2)
GI_TYPE_TAG_UINT8 =  c_int(3)
GI_TYPE_TAG_INT16 =  c_int(4)
GI_TYPE_TAG_UINT16 =  c_int(5)
GI_TYPE_TAG_INT32 =  c_int(6)
GI_TYPE_TAG_UINT32 =  c_int(7)
GI_TYPE_TAG_INT64 =  c_int(8)
GI_TYPE_TAG_UINT64 = c_int(9)
GI_TYPE_TAG_FLOAT = c_int(10)
GI_TYPE_TAG_DOUBLE = c_int(11)
GI_TYPE_TAG_GTYPE = c_int(12)
GI_TYPE_TAG_UTF8 = c_int(13)
GI_TYPE_TAG_FILENAME = c_int(14)
GI_TYPE_TAG_ARRAY = c_int(15)
GI_TYPE_TAG_INTERFACE = c_int(16)
GI_TYPE_TAG_GLIST = c_int(17)
GI_TYPE_TAG_GSLIST = c_int(18)
GI_TYPE_TAG_GHASH = c_int(19)
GI_TYPE_TAG_ERROR = c_int(20)

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

# GIRepositoryLoadFlags
enum_GIRepositoryLoadFlags = c_int
enum_G_IREPOSITORY_LOAD_FLAG_LAZY = c_int(1 << 0)

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
	enum_BLOB_TYPE_UNION
) = map(c_int, range(12))

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
# util
#
def giargument_from_pyobject(obj):
	pass

def pyobject_from_giargument(arg):
	pass

def giargument_release(arg):
	pass

#
# GObject
#
func_g_type_init = ctypes_get_funcptr(
	libgo,
	'g_type_init',
)

#
# GIRepository
#
func_g_irepository_get_default = ctypes_get_funcptr(
	libgir,
	'g_irepository_get_default',
	POINTER(struct_GIRepository),
)

func_g_irepository_prepend_search_path = ctypes_get_funcptr(
	libgir,
	'g_irepository_prepend_search_path',
	None,
	c_char_p,
)

func_g_irepository_get_search_path = ctypes_get_funcptr(
	libgir,
	'g_irepository_get_search_path',
	POINTER(struct_GSList),
)

func_g_irepository_load_typelib = ctypes_get_funcptr(
	libgir,
	'g_irepository_load_typelib',
	c_char_p,
	POINTER(struct_GIRepository),
	POINTER(struct_GITypelib),
	enum_GIRepositoryLoadFlags,
	POINTER(POINTER(struct_GError)),
)

func_g_irepository_is_registered =  ctypes_get_funcptr(
	libgir,
	'g_irepository_is_registered',
	c_int,
	POINTER(struct_GIRepository),
	c_char_p,
	c_char_p,
)

func_g_irepository_find_by_name =  ctypes_get_funcptr(
	libgir,
	'g_irepository_find_by_name',
	POINTER(struct_GIBaseInfo),
	POINTER(struct_GIRepository),
	c_char_p,
	c_char_p,
)

func_g_irepository_require = ctypes_get_funcptr(
	libgir,
	'g_irepository_require',
	POINTER(struct_GITypelib),
	POINTER(struct_GIRepository),
	c_char_p,
	c_char_p,
	enum_GIRepositoryLoadFlags,
	POINTER(POINTER(struct_GError)),
)

func_g_irepository_require_private = ctypes_get_funcptr(
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

func_g_irepository_get_dependencies =  ctypes_get_funcptr(
	libgir,
	'g_irepository_get_dependencies',
	POINTER(c_char_p),
	POINTER(struct_GIRepository),
	c_char_p,
)

func_g_irepository_get_loaded_namespaces =  ctypes_get_funcptr(
	libgir,
	'g_irepository_get_loaded_namespaces',
	POINTER(c_char_p),
	POINTER(struct_GIRepository),
)

func_g_irepository_find_by_gtype =  ctypes_get_funcptr(
	libgir,
	'g_irepository_find_by_gtype',
	POINTER(struct_GIBaseInfo),
	POINTER(struct_GIRepository),
	typedef_GType
)

func_g_irepository_get_n_infos =  ctypes_get_funcptr(
	libgir,
	'g_irepository_get_n_infos',
	c_int,
	POINTER(struct_GIRepository),
	c_char_p,
)

func_g_irepository_get_info =  ctypes_get_funcptr(
	libgir,
	'g_irepository_get_info',
	POINTER(struct_GIBaseInfo),
	POINTER(struct_GIRepository),
	c_char_p,
	c_int,
)

func_g_irepository_get_typelib_path =  ctypes_get_funcptr(
	libgir,
	'g_irepository_get_typelib_path',
	c_char_p,
	POINTER(struct_GIRepository),
	c_char_p,
)

func_g_irepository_get_shared_library =  ctypes_get_funcptr(
	libgir,
	'g_irepository_get_shared_library',
	c_char_p,
	POINTER(struct_GIRepository),
	c_char_p,
)

func_g_irepository_get_version =  ctypes_get_funcptr(
	libgir,
	'g_irepository_get_version',
	c_char_p,
	POINTER(struct_GIRepository),
	c_char_p,
)

func_g_irepository_get_option_group =  ctypes_get_funcptr(
	libgir,
	'g_irepository_get_option_group',
	POINTER(struct_GOptionGroup),
)

func_g_irepository_get_c_prefix =  ctypes_get_funcptr(
	libgir,
	'g_irepository_get_c_prefix',
	c_char_p,
	POINTER(struct_GIRepository),
	c_char_p,
)

func_g_irepository_dump =  ctypes_get_funcptr(
	libgir,
	'g_irepository_dump',
	c_int,
	c_char_p,
	POINTER(POINTER(struct_GError)),
)

func_g_irepository_enumerate_versions =  ctypes_get_funcptr(
	libgir,
	'g_irepository_enumerate_versions',
	POINTER(struct_GList),
	POINTER(struct_GIRepository),
	c_char_p,
)

func_g_typelib_new_from_memory =  ctypes_get_funcptr(
	libgir,
	'g_typelib_new_from_memory',
	POINTER(struct_GITypelib),
	POINTER(c_ubyte),
	c_ulong,
	POINTER(POINTER(struct_GError)),
)

func_g_typelib_new_from_const_memory =  ctypes_get_funcptr(
	libgir,
	'g_typelib_new_from_const_memory',
	POINTER(struct_GITypelib),
	POINTER(c_ubyte),
	c_ulong,
	POINTER(POINTER(struct_GError)),
)

func_g_typelib_new_from_mapped_file =  ctypes_get_funcptr(
	libgir,
	'g_typelib_new_from_mapped_file',
	POINTER(struct_GITypelib),
	POINTER(struct_GMappedFile),
	POINTER(POINTER(struct_GError)),
)

func_g_typelib_free =  ctypes_get_funcptr(
	libgir,
	'g_typelib_free',
	None,
	POINTER(struct_GITypelib),
)

func_g_typelib_symbol =  ctypes_get_funcptr(
	libgir,
	'g_typelib_symbol',
	c_int,
	POINTER(struct_GITypelib),
	c_char_p,
	c_void_p,
)

func_g_typelib_get_namespace =  ctypes_get_funcptr(
	libgir,
	'g_typelib_get_namespace',
	c_char_p,
	POINTER(struct_GITypelib),
)

#
# GIBaseInfo
#
func_g_info_type_to_string =  ctypes_get_funcptr(
	libgir,
	'g_info_type_to_string',
	c_char_p,
	enum_GIInfoType,
)

func_g_base_info_ref =  ctypes_get_funcptr(
	libgir,
	'g_base_info_ref',
	POINTER(struct_GIBaseInfo),
	POINTER(struct_GIBaseInfo),
)

func_g_base_info_unref =  ctypes_get_funcptr(
	libgir,
	'g_base_info_unref',
	None,
	POINTER(struct_GIBaseInfo),
)

func_g_base_info_get_type =  ctypes_get_funcptr(
	libgir,
	'g_base_info_get_type',
	enum_GIInfoType,
	POINTER(struct_GIBaseInfo),
)

func_g_base_info_get_name =  ctypes_get_funcptr(
	libgir,
	'g_base_info_get_name',
	c_char_p,
	POINTER(struct_GIBaseInfo),
)

func_g_base_info_get_namespace =  ctypes_get_funcptr(
	libgir,
	'g_base_info_get_namespace',
	c_char_p,
	POINTER(struct_GIBaseInfo),
)

func_g_base_info_is_deprecated =  ctypes_get_funcptr(
	libgir,
	'g_base_info_is_deprecated',
	c_int,
	POINTER(struct_GIBaseInfo),
)

func_g_base_info_get_attribute =  ctypes_get_funcptr(
	libgir,
	'g_base_info_get_attribute',
	c_char_p,
	POINTER(struct_GIBaseInfo),
	c_char_p,
)

func_g_base_info_iterate_attributes =  ctypes_get_funcptr(
	libgir,
	'g_base_info_iterate_attributes',
	c_int,
	POINTER(struct_GIBaseInfo),
	POINTER(struct_GIAttributeIter),
	c_char_p,
	c_char_p,
)

func_g_base_info_get_container =  ctypes_get_funcptr(
	libgir,
	'g_base_info_get_container',
	POINTER(struct_GIBaseInfo),
	POINTER(struct_GIBaseInfo),
)

func_g_base_info_get_typelib =  ctypes_get_funcptr(
	libgir,
	'g_base_info_get_typelib',
	POINTER(struct_GITypelib),
	POINTER(struct_GIBaseInfo),
)

func_g_base_info_equal =  ctypes_get_funcptr(
	libgir,
	'g_base_info_equal',
	c_int,
	POINTER(struct_GIBaseInfo),
	POINTER(struct_GIBaseInfo),
)

#
# GIFunctionInfo
#
func_g_function_info_get_symbol =  ctypes_get_funcptr(
	libgir,
	'g_function_info_get_symbol',
	c_char_p,
	POINTER(struct_GIFunctionInfo),
)

func_g_function_info_get_flags =  ctypes_get_funcptr(
	libgir,
	'g_function_info_get_flags',
	enum_GIFunctionInfoFlags,
	POINTER(struct_GIFunctionInfo),
)

func_g_function_info_get_property =  ctypes_get_funcptr(
	libgir,
	'g_function_info_get_property',
	POINTER(struct_GIPropertyInfo),
	POINTER(struct_GIFunctionInfo),
)

func_g_function_info_get_vfunc =  ctypes_get_funcptr(
	libgir,
	'g_function_info_get_vfunc',
	POINTER(struct_GIVFuncInfo),
	POINTER(struct_GIFunctionInfo),
)

func_g_function_info_invoke =  ctypes_get_funcptr(
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
#~ GITypeInfo *        g_callable_info_get_return_type     (GICallableInfo *info);
#~ GITransfer          g_callable_info_get_caller_owns     (GICallableInfo *info);
#~ gboolean            g_callable_info_may_return_null     (GICallableInfo *info);
#~ const gchar *       g_callable_info_get_return_attribute
                                                        #~ (GICallableInfo *info,
                                                         #~ const gchar *name);
#~ gboolean            g_callable_info_iterate_return_attributes
                                                        #~ (GICallableInfo *info,
                                                         #~ GIAttributeIter *iterator,
                                                         #~ char **name,
                                                         #~ char **value);
#~ gint                g_callable_info_get_n_args          (GICallableInfo *info);
#~ GIArgInfo *         g_callable_info_get_arg             (GICallableInfo *info,
                                                         #~ gint n);
#~ void                g_callable_info_load_arg            (GICallableInfo *info,
                                                         #~ gint n,
                                                         #~ GIArgInfo *arg);
#~ void                g_callable_info_load_return_type    (GICallableInfo *info,
                                                         #~ GITypeInfo *type);

#
# GIArgInfo
#
#~ GIDirection         g_arg_info_get_direction            (GIArgInfo *info);
#~ gboolean            g_arg_info_is_caller_allocates      (GIArgInfo *info);
#~ gboolean            g_arg_info_is_return_value          (GIArgInfo *info);
#~ gboolean            g_arg_info_is_optional              (GIArgInfo *info);
#~ gboolean            g_arg_info_may_be_null              (GIArgInfo *info);
#~ GITransfer          g_arg_info_get_ownership_transfer   (GIArgInfo *info);
#~ GIScopeType         g_arg_info_get_scope                (GIArgInfo *info);
#~ gint                g_arg_info_get_closure              (GIArgInfo *info);
#~ gint                g_arg_info_get_destroy              (GIArgInfo *info);
#~ GITypeInfo *        g_arg_info_get_type                 (GIArgInfo *info);
#~ void                g_arg_info_load_type                (GIArgInfo *info,
                                                         #~ GITypeInfo *type);

#
# GIArgInfo
#
#~ GIDirection         g_arg_info_get_direction            (GIArgInfo *info);
#~ gboolean            g_arg_info_is_caller_allocates      (GIArgInfo *info);
#~ gboolean            g_arg_info_is_return_value          (GIArgInfo *info);
#~ gboolean            g_arg_info_is_optional              (GIArgInfo *info);
#~ gboolean            g_arg_info_may_be_null              (GIArgInfo *info);
#~ GITransfer          g_arg_info_get_ownership_transfer   (GIArgInfo *info);
#~ GIScopeType         g_arg_info_get_scope                (GIArgInfo *info);
#~ gint                g_arg_info_get_closure              (GIArgInfo *info);
#~ gint                g_arg_info_get_destroy              (GIArgInfo *info);
#~ GITypeInfo *        g_arg_info_get_type                 (GIArgInfo *info);
#~ void                g_arg_info_load_type                (GIArgInfo *info,
                                                         #~ GITypeInfo *type);

#
# GIStructInfo
#
#~ gint                g_struct_info_get_n_fields          (GIStructInfo *info);
#~ GIFieldInfo *       g_struct_info_get_field             (GIStructInfo *info,
                                                         #~ gint n);
#~ gint                g_struct_info_get_n_methods         (GIStructInfo *info);
#~ GIFunctionInfo *    g_struct_info_get_method            (GIStructInfo *info,
                                                         #~ gint n);
#~ GIFunctionInfo *    g_struct_info_find_method           (GIStructInfo *info,
                                                         #~ const gchar *name);
#~ gsize               g_struct_info_get_size              (GIStructInfo *info);
#~ gsize               g_struct_info_get_alignment         (GIStructInfo *info);
#~ gboolean            g_struct_info_is_gtype_struct       (GIStructInfo *info);
#~ gboolean            g_struct_info_is_foreign            (GIStructInfo *info);

#
# GIUnionInfo
#
#~ gint                g_union_info_get_n_fields           (GIUnionInfo *info);
#~ GIFieldInfo *       g_union_info_get_field              (GIUnionInfo *info,
                                                         #~ gint n);
#~ gint                g_union_info_get_n_methods          (GIUnionInfo *info);
#~ GIFunctionInfo *    g_union_info_get_method             (GIUnionInfo *info,
                                                         #~ gint n);
#~ gboolean            g_union_info_is_discriminated       (GIUnionInfo *info);
#~ gint                g_union_info_get_discriminator_offset
                                                        #~ (GIUnionInfo *info);
#~ GITypeInfo *        g_union_info_get_discriminator_type (GIUnionInfo *info);
#~ GIConstantInfo *    g_union_info_get_discriminator      (GIUnionInfo *info,
                                                         #~ gint n);
#~ GIFunctionInfo *    g_union_info_find_method            (GIUnionInfo *info,
                                                         #~ const gchar *name);
#~ gsize               g_union_info_get_size               (GIUnionInfo *info);
#~ gsize               g_union_info_get_alignment          (GIUnionInfo *info);

#
# GIFieldInfo
#
#~ GIFieldInfoFlags    g_field_info_get_flags              (GIFieldInfo *info);
#~ gint                g_field_info_get_size               (GIFieldInfo *info);
#~ gint                g_field_info_get_offset             (GIFieldInfo *info);
#~ GITypeInfo *        g_field_info_get_type               (GIFieldInfo *info);
#~ gboolean            g_field_info_get_field              (GIFieldInfo *field_info,
                                                         #~ gpointer mem,
                                                         #~ GIArgument *value);
#~ gboolean            g_field_info_set_field              (GIFieldInfo *field_info,
                                                         #~ gpointer mem,
                                                         #~ const GIArgument *value);

#
# GIPropertyInfo
#
#~ GParamFlags         g_property_info_get_flags           (GIPropertyInfo *info);
#~ GITypeInfo *        g_property_info_get_type            (GIPropertyInfo *info);
#~ GITransfer          g_property_info_get_ownership_transfer
                                                        #~ (GIPropertyInfo *info);

#
# GIVFuncInfo
#
#~ GIVFuncInfoFlags    g_vfunc_info_get_flags              (GIVFuncInfo *info);
#~ gint                g_vfunc_info_get_offset             (GIVFuncInfo *info);
#~ GISignalInfo *      g_vfunc_info_get_signal             (GIVFuncInfo *info);
#~ GIFunctionInfo *    g_vfunc_info_get_invoker            (GIVFuncInfo *info);

#
# GISignalInfo
#
#~ GSignalFlags        g_signal_info_get_flags             (GISignalInfo *info);
#~ GIVFuncInfo *       g_signal_info_get_class_closure     (GISignalInfo *info);
#~ gboolean            g_signal_info_true_stops_emit       (GISignalInfo *info);

#
# GIEnumInfo
#
#~ gint                g_enum_info_get_n_values            (GIEnumInfo *info);
#~ GIValueInfo *       g_enum_info_get_value               (GIEnumInfo *info,
                                                         #~ gint n);
#~ GITypeTag           g_enum_info_get_storage_type        (GIEnumInfo *info);
#~ glong               g_value_info_get_value              (GIValueInfo *info);

#
# GIRegisteredTypeInfo
#
#~ const gchar *       g_registered_type_info_get_type_name
                                                        #~ (GIRegisteredTypeInfo *info);
#~ const gchar *       g_registered_type_info_get_type_init
                                                        #~ (GIRegisteredTypeInfo *info);
#~ GType               g_registered_type_info_get_g_type   (GIRegisteredTypeInfo *info);

#
# GIObjectInfo
#
#~ void *              (*GIObjectInfoGetValueFunction)     (const GValue *value);
#~ void *              (*GIObjectInfoRefFunction)          (void *object);
#~ void                (*GIObjectInfoSetValueFunction)     (GValue *value,
                                                         #~ void *object);
#~ void                (*GIObjectInfoUnrefFunction)        (void *object);
#~ const gchar *       g_object_info_get_type_name         (GIObjectInfo *info);
#~ const gchar *       g_object_info_get_type_init         (GIObjectInfo *info);
#~ gboolean            g_object_info_get_abstract          (GIObjectInfo *info);
#~ gboolean            g_object_info_get_fundamental       (GIObjectInfo *info);
#~ GIObjectInfo *      g_object_info_get_parent            (GIObjectInfo *info);
#~ gint                g_object_info_get_n_interfaces      (GIObjectInfo *info);
#~ GIInterfaceInfo *   g_object_info_get_interface         (GIObjectInfo *info,
                                                         #~ gint n);
#~ gint                g_object_info_get_n_fields          (GIObjectInfo *info);
#~ GIFieldInfo *       g_object_info_get_field             (GIObjectInfo *info,
                                                         #~ gint n);
#~ gint                g_object_info_get_n_properties      (GIObjectInfo *info);
#~ GIPropertyInfo *    g_object_info_get_property          (GIObjectInfo *info,
                                                         #~ gint n);
#~ gint                g_object_info_get_n_methods         (GIObjectInfo *info);
#~ GIFunctionInfo *    g_object_info_get_method            (GIObjectInfo *info,
                                                         #~ gint n);
#~ GIFunctionInfo *    g_object_info_find_method           (GIObjectInfo *info,
                                                         #~ const gchar *name);
#~ gint                g_object_info_get_n_signals         (GIObjectInfo *info);
#~ GISignalInfo *      g_object_info_get_signal            (GIObjectInfo *info,
                                                         #~ gint n);
#~ gint                g_object_info_get_n_vfuncs          (GIObjectInfo *info);
#~ GIVFuncInfo *       g_object_info_get_vfunc             (GIObjectInfo *info,
                                                         #~ gint n);
#~ gint                g_object_info_get_n_constants       (GIObjectInfo *info);
#~ GIConstantInfo *    g_object_info_get_constant          (GIObjectInfo *info,
                                                         #~ gint n);
#~ GIStructInfo *      g_object_info_get_class_struct      (GIObjectInfo *info);
#~ GIVFuncInfo *       g_object_info_find_vfunc            (GIObjectInfo *info,
                                                         #~ const gchar *name);
#~ const char *        g_object_info_get_unref_function    (GIObjectInfo *info);
#~ GIObjectInfoUnrefFunction  g_object_info_get_unref_function_pointer
                                                        #~ (GIObjectInfo *info);
#~ const char *        g_object_info_get_ref_function      (GIObjectInfo *info);
#~ GIObjectInfoRefFunction  g_object_info_get_ref_function_pointer
                                                        #~ (GIObjectInfo *info);
#~ const char *        g_object_info_get_set_value_function
                                                        #~ (GIObjectInfo *info);
#~ GIObjectInfoSetValueFunction  g_object_info_get_set_value_function_pointer
                                                        #~ (GIObjectInfo *info);
#~ const char *        g_object_info_get_get_value_function
                                                        #~ (GIObjectInfo *info);
#~ GIObjectInfoGetValueFunction  g_object_info_get_get_value_function_pointer
                                                        #~ (GIObjectInfo *info);

#
# GIInterfaceInfo
#
#~ gint                g_interface_info_get_n_prerequisites
                                                        #~ (GIInterfaceInfo *info);
#~ GIBaseInfo *        g_interface_info_get_prerequisite   (GIInterfaceInfo *info,
                                                         #~ gint n);
#~ gint                g_interface_info_get_n_properties   (GIInterfaceInfo *info);
#~ GIPropertyInfo *    g_interface_info_get_property       (GIInterfaceInfo *info,
                                                         #~ gint n);
#~ gint                g_interface_info_get_n_methods      (GIInterfaceInfo *info);
#~ GIFunctionInfo *    g_interface_info_get_method         (GIInterfaceInfo *info,
                                                         #~ gint n);
#~ GIFunctionInfo *    g_interface_info_find_method        (GIInterfaceInfo *info,
                                                         #~ const gchar *name);
#~ gint                g_interface_info_get_n_signals      (GIInterfaceInfo *info);
#~ GISignalInfo *      g_interface_info_get_signal         (GIInterfaceInfo *info,
                                                         #~ gint n);
#~ gint                g_interface_info_get_n_vfuncs       (GIInterfaceInfo *info);
#~ GIVFuncInfo *       g_interface_info_get_vfunc          (GIInterfaceInfo *info,
                                                         #~ gint n);
#~ gint                g_interface_info_get_n_constants    (GIInterfaceInfo *info);
#~ GIConstantInfo *    g_interface_info_get_constant       (GIInterfaceInfo *info,
                                                         #~ gint n);
#~ GIStructInfo *      g_interface_info_get_iface_struct   (GIInterfaceInfo *info);
#~ GIVFuncInfo *       g_interface_info_find_vfunc         (GIInterfaceInfo *info,
                                                         #~ const gchar *name);

#
# GIConstantInfo
#
#~ GITypeInfo *        g_constant_info_get_type            (GIConstantInfo *info);
#~ gint                g_constant_info_get_value           (GIConstantInfo *info,
                                                         #~ GIArgument *value);

#
# GIErrorDomainInfo
#
#~ const gchar *       g_error_domain_info_get_quark       (GIErrorDomainInfo *info);
#~ GIInterfaceInfo *   g_error_domain_info_get_codes       (GIErrorDomainInfo *info);


#
# Low-level C classes
#


#
# High-level Python classes
#
