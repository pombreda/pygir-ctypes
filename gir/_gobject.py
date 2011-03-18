from ._glib import *

libgobject = CDLL(find_library('gobject-2.0'))

# GType
class GType(gsize): pass
class GTypeCValue(Union): pass
class GTypePlugin(Structure): pass
class GTypeClass(Structure):
	_fields_ = [
		('g_type', GType),
	]
class GTypeInterface(Structure):
	_fields_ = [
		('g_type', GType),
		('g_instance_type', GType),
	]
class GTypeInstance(Structure):
	_fields_ = [
		('g_class', POINTER(GTypeClass)),
	]
class GTypeInfo(Union): pass
class GTypeFundamentalInfo(Union): pass
class GInterfaceInfo(Union): pass
class GTypeValueTable(Union): pass
class GTypeQuery(Structure):
	_fields_ = [
		('type', GType),
		('type_name', gchar_p),
		('class_size', guint),
		('instance_size', guint),
	]

# GType
G_TYPE_INVALID = GType(0)
G_TYPE_NONE = GType(1)
G_TYPE_INTERFACE = GType(2)
G_TYPE_CHAR = GType(3)
G_TYPE_UCHAR = GType(4)
G_TYPE_BOOLEAN = GType(5)
G_TYPE_INT = GType(6)
G_TYPE_UINT = GType(7)
G_TYPE_LONG = GType(8)
G_TYPE_ULONG = GType(9)
G_TYPE_INT64 = GType(10)
G_TYPE_UINT64 = GType(11)
G_TYPE_ENUM = GType(12)
G_TYPE_FLAGS = GType(13)
G_TYPE_FLOAT = GType(14)
G_TYPE_DOUBLE = GType(15)
G_TYPE_STRING = GType(16)
G_TYPE_POINTER = GType(17)
G_TYPE_BOXED = GType(18)
G_TYPE_PARAM = GType(19)
G_TYPE_OBJECT = GType(20)
G_TYPE_VARIANT = GType(21)
G_TYPE_RESERVED_GLIB_FIRST = GType(22)
G_TYPE_RESERVED_GLIB_LAST = GType(31)
G_TYPE_RESERVED_BSE_FIRST = GType(32)
G_TYPE_RESERVED_BSE_LAST = GType(48)
G_TYPE_RESERVED_USER_FIRST = GType(49)

# GValue
class _GValue_union0(Union):
	_fields_ = [
		('v_int', gint),
		('v_uint', guint),
		('v_long', glong),
		('v_ulong', gulong),
		('v_int64', gint64),
		('v_uint64', guint64),
		('v_float', gfloat),
		('v_double', gdouble),
		('v_pointer', gpointer),
	]

class GValue(Structure):
	_fields_ = [
		('g_type', GType),
		('data', _GValue_union0 * 2),
	]

# GObject
class GObject(Structure):
	_fields_ = [
		('g_type_instance', GTypeInstance),
		('ref_count', guint),
		('qdata', POINTER(GData)),
	]
class GObjectClass(Structure):
	_fields_ = [
		('g_type_class', GTypeClass),
	]
class GInitiallyUnowned(Structure): pass
class GInitiallyUnownedClass(Structure): pass
class GObjectConstructParam(Structure): pass

# GParam
class GParamSpec(Structure): pass
class GParamSpecClass(Structure): pass

GParamFlags = gint
G_PARAM_READABLE = GParamFlags(1 << 0)
G_PARAM_WRITABLE = GParamFlags(1 << 1)
G_PARAM_CONSTRUCT = GParamFlags(1 << 2)
G_PARAM_CONSTRUCT_ONLY = GParamFlags(1 << 3)
G_PARAM_LAX_VALIDATION = GParamFlags(1 << 4)
G_PARAM_STATIC_NAME = GParamFlags(1 << 5)
G_PARAM_PRIVATE = G_PARAM_STATIC_NAME
G_PARAM_STATIC_NICK = GParamFlags(1 << 6)
G_PARAM_STATIC_BLURB = GParamFlags(1 << 7)
G_PARAM_DEPRECATED = GParamFlags(1 << 31)

# GCClosure
class GClosure(Structure): pass
class GCClosure(Structure): pass

GClosureMarshal = CFUNCTYPE(
	POINTER(GClosure),
	POINTER(GValue),
	guint,
	POINTER(GValue),
	gpointer,
	gpointer,
)

# GSignal
class GSignalInvocationHint(Structure): pass
GSignalCMarshaller = GClosureMarshal

GSignalEmissionHook = CFUNCTYPE(
	POINTER(GSignalInvocationHint),
	guint,
	POINTER(GValue),
	gpointer,
)

GSignalFlags = gint
G_SIGNAL_RUN_FIRST = GSignalFlags(1 << 0)
G_SIGNAL_RUN_LAST = GSignalFlags(1 << 1)
G_SIGNAL_RUN_CLEANUP = GSignalFlags(1 << 2)
G_SIGNAL_NO_RECURSE = GSignalFlags(1 << 3)
G_SIGNAL_DETAILED = GSignalFlags(1 << 4)
G_SIGNAL_ACTION = GSignalFlags(1 << 5)
G_SIGNAL_NO_HOOKS = GSignalFlags(1 << 6)

GSignalMatchType = gint
G_SIGNAL_MATCH_ID = GSignalMatchType(1 << 0)
G_SIGNAL_MATCH_DETAIL = GSignalMatchType(1 << 1)
G_SIGNAL_MATCH_CLOSURE = GSignalMatchType(1 << 2)
G_SIGNAL_MATCH_FUNC = GSignalMatchType(1 << 3)
G_SIGNAL_MATCH_DATA = GSignalMatchType(1 << 4)
G_SIGNAL_MATCH_UNBLOCKED = GSignalMatchType(1 << 5)

class GSignalQuery(Structure): pass

#
# GType
#
g_type_init = ctypes_get_func(
	libgobject,
	'g_type_init',
)

g_gtype_get_type = ctypes_get_func(
	libgobject,
	'g_gtype_get_type',
	GType,
)

#
# GValue
#
g_value_get_type = ctypes_get_func(
	libgobject,
	'g_value_get_type',
	GType,
)

g_value_array_get_type = ctypes_get_func(
	libgobject,
	'g_value_array_get_type',
	GType,
)

#
# GType/GValue
#
g_type_init() # necessary for rest of function calls
G_TYPE_GTYPE = g_gtype_get_type()
G_TYPE_VALUE = g_value_get_type()
G_TYPE_VALUE_ARRAY = g_value_array_get_type()
