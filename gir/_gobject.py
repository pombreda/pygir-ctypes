from ._glib import *

libgobject = CDLL(find_library('gobject-2.0'))

# GType
class GType(gsize): pass
class GValue(Structure): pass
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
