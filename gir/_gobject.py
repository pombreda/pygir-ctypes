try:
	exec('from ._glib import *', globals(), locals())
except SyntaxError:
	from _glib import *
except ImportError:
	from _glib import *
	
# gobject - C library
libgobject = CDLL(find_library('gobject-2.0'))

#
# GType
#
class GType(gsize): pass

class GTypeInterface(Structure):
	_fields_ = [
		('g_type', GType),
		('g_instance_type', GType),
	]

class GTypeClass(Structure):
	_fields_ = [
		('g_type', GType),
	]

class GTypeInstance(Structure):
	_fields_ = [
		('g_class', POINTER(GTypeClass)),
	]

class GTypeInfo(Structure): pass

class GTypeFundamentalInfo(Structure): pass

class GInterfaceInfo(Structure): pass

class GTypeValueTable(Structure): pass

GTypeDebugFlags = gint
G_TYPE_DEBUG_NONE = GTypeDebugFlags(0)
G_TYPE_DEBUG_OBJECTS = GTypeDebugFlags(1 << 0)
G_TYPE_DEBUG_SIGNALS = GTypeDebugFlags(1 << 1)
G_TYPE_DEBUG_MASK = GTypeDebugFlags(0x03)

class GTypeQuery(Structure):
	_fields_ = [
		('type', GType),
		('type_name', gchar_p),
		('class_size', guint),
		('instance_size', guint),
	]

GTypeFlags = gint
G_TYPE_FLAG_ABSTRACT = GTypeFlags(1 << 4)
G_TYPE_FLAG_VALUE_ABSTRACT = GTypeFlags(1 << 5)

GTypeFundamentalFlags = gint
G_TYPE_FLAG_CLASSED = GTypeFundamentalFlags(1 << 0)
G_TYPE_FLAG_INSTANTIATABLE = GTypeFundamentalFlags(1 << 1)
G_TYPE_FLAG_DERIVABLE = GTypeFundamentalFlags(1 << 2)
G_TYPE_FLAG_DEEP_DERIVABLE = GTypeFundamentalFlags(1 << 3)

#
# GTypePlugin
#
class GTypePlugin(Structure): pass
class GTypePluginClass(Structure): pass

#
# GTypeModule
#
class GTypeModule(Structure):
	_fields_ = [
		('name', gchar_p),
	]

class GTypeModuleClass(Structure): pass

#
# GObject
#
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

class GObjectConstructParam(Structure): pass

class GInitiallyUnowned(GObject): pass
class GInitiallyUnownedClass(GObjectClass): pass

class GParameter(Structure): pass

#
# GEnum/GFlags
#
class GEnumClass(Structure): pass
class GFlagsClass(Structure): pass
class GEnumValue(Structure): pass
class GFlagsValue(Structure): pass

#
# GBoxed
#
GStrv = POINTER(gchar_p)

#
# GValue
#
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

#
# GParamSpec/GValue
#
class GParamSpecBoolean(Structure): pass
class GParamSpecChar(Structure): pass
class GParamSpecUChar(Structure): pass
class GParamSpecInt(Structure): pass
class GParamSpecUInt(Structure): pass
class GParamSpecLong(Structure): pass
class GParamSpecULong(Structure): pass
class GParamSpecInt64(Structure): pass
class GParamSpecUInt64(Structure): pass
class GParamSpecFloat(Structure): pass
class GParamSpecDouble(Structure): pass
class GParamSpecEnum(Structure): pass
class GParamSpecFlags(Structure): pass
class GParamSpecString(Structure): pass
gchararray = POINTER(gchar_p)
class GParamSpecParam(Structure): pass
class GParamSpecBoxed(Structure): pass
class GParamSpecPointer(Structure): pass
class GParamSpecObject(Structure): pass
class GParamSpecUnichar(Structure): pass
class GParamSpecValueArray(Structure): pass
class GParamSpecOverride(Structure): pass
class GParamSpecGType(Structure): pass
class GParamSpecVariant(Structure): pass

#
# GParamSpec
#
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

class GParamSpecTypeInfo(Structure): pass

class GParamSpecPool(Structure): pass

#
# GTypeCValue
#
class GTypeCValue(Union):
	_fields_ = [
		('v_int', gint),
		('v_long', glong),
		('v_int64', gint64),
		('v_double', gdouble),
		('v_pointer', gpointer),
	]

#
# GSignal
#
class  GSignalInvocationHint(Structure): pass
class GSignalCMarshaller(Structure): pass

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

GConnectFlags = gint
G_CONNECT_AFTER = GConnectFlags(1 << 0)
G_CONNECT_SWAPPED = GConnectFlags(1 << 1)

#
# GClosure
#
class GClosure(Structure):
	_fields_ = [
		('refcount_metamarshal_nguards_nfnotifiers_ninotifiers_ininotify_floating_derivativeflag_inmarshal_isinvalid', guint),
		('marshal', gpointer),
		('data', gpointer),
		('notifiers', gpointer),
	]

class GCClosure(Structure):
	_fields_ = [
		('closure', GClosure),
		('callback', gpointer),
	]

#
# GValueArray
#
class GValueArray(Structure):
	_fields_ = [
		('n_values', guint),
		('values', POINTER(GValue)),
	]

#
# GBinding
#
class GBinding(Structure): pass

GBindingFlags = gint
G_BINDING_DEFAULT = GBindingFlags(0)
G_BINDING_BIDIRECTIONAL = GBindingFlags(1 << 0)
G_BINDING_SYNC_CREATE = GBindingFlags(1 << 1)
G_BINDING_INVERT_BOOLEAN = GBindingFlags(1 << 2)

#
# GType
#
g_type_init = ctypes_get_func(
	libgobject,
	'g_type_init',
	None,
)

# necessary for rest of function calls
g_type_init()

g_type_init_with_debug_flags = ctypes_get_func(
	libgobject,
	'g_type_init_with_debug_flags',
	None,
	GTypeDebugFlags,
)

g_type_name = ctypes_get_func(
	libgobject,
	'g_type_name',
	gchar_p,
	GType,
)

g_type_qname = ctypes_get_func(
	libgobject,
	'g_type_qname',
	GQuark,
	GType,
)

g_type_from_name = ctypes_get_func(
	libgobject,
	'g_type_from_name',
	GType,
	gchar_p,
)

g_type_parent = ctypes_get_func(
	libgobject,
	'g_type_parent',
	GType,
	GType,
)

g_type_depth = ctypes_get_func(
	libgobject,
	'g_type_depth',
	guint,
	GType,
)

g_type_next_base = ctypes_get_func(
	libgobject,
	'g_type_next_base',
	GType,
	GType,
	GType,
)

g_type_is_a = ctypes_get_func(
	libgobject,
	'g_type_is_a',
	gboolean,
	GType,
	GType,
)

g_type_class_ref = ctypes_get_func(
	libgobject,
	'g_type_class_ref',
	gpointer,
	GType,
)

g_type_class_peek = ctypes_get_func(
	libgobject,
	'g_type_class_peek',
	gpointer,
	GType,
)

g_type_class_peek_static = ctypes_get_func(
	libgobject,
	'g_type_class_peek_static',
	gpointer,
	GType,
)

g_type_class_unref = ctypes_get_func(
	libgobject,
	'g_type_class_unref',
	None,
	gpointer,
)

g_type_class_peek_parent = ctypes_get_func(
	libgobject,
	'g_type_class_peek_parent',
	gpointer,
	gpointer,
)

g_type_class_add_private = ctypes_get_func(
	libgobject,
	'g_type_class_add_private',
	None,
	gpointer,
	gsize,
)

g_type_add_class_private = ctypes_get_func(
	libgobject,
	'g_type_add_class_private',
	None,
	GType,
	gsize,
)

g_type_interface_peek = ctypes_get_func(
	libgobject,
	'g_type_interface_peek',
	gpointer,
	gpointer,
	GType,
)

g_type_interface_peek_parent = ctypes_get_func(
	libgobject,
	'g_type_interface_peek_parent',
	gpointer,
	gpointer,
)

g_type_default_interface_ref = ctypes_get_func(
	libgobject,
	'g_type_default_interface_ref',
	gpointer,
	GType,
)

g_type_default_interface_peek = ctypes_get_func(
	libgobject,
	'g_type_default_interface_peek',
	gpointer,
	GType,
)

g_type_default_interface_unref = ctypes_get_func(
	libgobject,
	'g_type_default_interface_unref',
	None,
	gpointer,
)

g_type_children = ctypes_get_func(
	libgobject,
	'g_type_children',
	POINTER(GType),
	GType,
	POINTER(guint),
)

g_type_interfaces = ctypes_get_func(
	libgobject,
	'g_type_interfaces',
	POINTER(GType),
	GType,
	POINTER(guint),
)

g_type_interface_prerequisites = ctypes_get_func(
	libgobject,
	'g_type_interface_prerequisites',
	POINTER(GType),
	GType,
	POINTER(guint),
)

g_type_set_qdata = ctypes_get_func(
	libgobject,
	'g_type_set_qdata',
	None,
	GType,
	GQuark,
	gpointer,
)

g_type_get_qdata = ctypes_get_func(
	libgobject,
	'g_type_get_qdata',
	gpointer,
	GType,
	GQuark,
)

g_type_query = ctypes_get_func(
	libgobject,
	'g_type_query',
	None,
	GType,
	POINTER(GTypeQuery),
)

GBaseInitFunc = CFUNCTYPE(None, gpointer)
GBaseFinalizeFunc = CFUNCTYPE(None, gpointer)
GClassInitFunc = CFUNCTYPE(None, gpointer, gpointer)
GClassFinalizeFunc = CFUNCTYPE(None, gpointer, gpointer)
GInstanceInitFunc = CFUNCTYPE(None, POINTER(GTypeInstance), gpointer)
GInterfaceInitFunc = CFUNCTYPE(None, gpointer, gpointer)
GInterfaceFinalizeFunc = CFUNCTYPE(None, gpointer, gpointer)
GTypeClassCacheFunc = CFUNCTYPE(gboolean, gpointer, POINTER(GTypeClass))

g_type_register_static = ctypes_get_func(
	libgobject,
	'g_type_register_static',
	GType,
	GType,
	gchar_p,
	POINTER(GTypeInfo),
	GTypeFlags,
)

g_type_register_static_simple = ctypes_get_func(
	libgobject,
	'g_type_register_static_simple',
	GType,
	GType,
	gchar_p,
	guint,
	GClassInitFunc,
	guint,
	GInstanceInitFunc,
	GTypeFlags,
)

g_type_register_dynamic = ctypes_get_func(
	libgobject,
	'g_type_register_dynamic',
	GType,
	GType,
	gchar_p,
	POINTER(GTypePlugin),
	GTypeFlags,
)

g_type_register_fundamental = ctypes_get_func(
	libgobject,
	'g_type_register_fundamental',
	GType,
	GType,
	gchar_p,
	POINTER(GTypeInfo),
	POINTER(GTypeFundamentalInfo),
	GTypeFlags,
)

g_type_add_interface_static = ctypes_get_func(
	libgobject,
	'g_type_add_interface_static',
	None,
	GType,
	GType,
	POINTER(GInterfaceInfo),
)

g_type_add_interface_dynamic = ctypes_get_func(
	libgobject,
	'g_type_add_interface_dynamic',
	None,
	GType,
	GType,
	POINTER(GTypePlugin),
)

g_type_interface_add_prerequisite = ctypes_get_func(
	libgobject,
	'g_type_interface_add_prerequisite',
	None,
	GType,
	GType,
)

g_type_get_plugin = ctypes_get_func(
	libgobject,
	'g_type_get_plugin',
	POINTER(GTypePlugin),
	GType,
)

g_type_interface_get_plugin = ctypes_get_func(
	libgobject,
	'g_type_interface_get_plugin',
	POINTER(GTypePlugin),
	GType,
	GType,
)

g_type_fundamental_next = ctypes_get_func(
	libgobject,
	'g_type_fundamental_next',
	GType,
)

g_type_fundamental = ctypes_get_func(
	libgobject,
	'g_type_fundamental',
	GType,
	GType,
)

g_type_create_instance = ctypes_get_func(
	libgobject,
	'g_type_create_instance',
	POINTER(GTypeInstance),
	GType,
)

g_type_free_instance = ctypes_get_func(
	libgobject,
	'g_type_free_instance',
	None,
	POINTER(GTypeInstance),
)

g_type_add_class_cache_func = ctypes_get_func(
	libgobject,
	'g_type_add_class_cache_func',
	None,
	gpointer,
	GTypeClassCacheFunc,
)

g_type_remove_class_cache_func = ctypes_get_func(
	libgobject,
	'g_type_remove_class_cache_func',
	None,
	gpointer,
	GTypeClassCacheFunc,
)

g_type_class_unref_uncached = ctypes_get_func(
	libgobject,
	'g_type_class_unref_uncached',
	None,
	gpointer,
)

GTypeInterfaceCheckFunc = CFUNCTYPE(None, gpointer, gpointer)

g_type_add_interface_check = ctypes_get_func(
	libgobject,
	'g_type_add_interface_check',
	None,
	gpointer,
	GTypeInterfaceCheckFunc,
)

g_type_remove_interface_check = ctypes_get_func(
	libgobject,
	'g_type_remove_interface_check',
	None,
	gpointer,
	GTypeInterfaceCheckFunc,
)

g_type_value_table_peek = ctypes_get_func(
	libgobject,
	'g_type_value_table_peek',
	POINTER(GTypeValueTable),
	GType,
)

#
# GTypePlugin
#
GTypePluginUse = CFUNCTYPE(None, POINTER(GTypePlugin))
GTypePluginUnuse = CFUNCTYPE(None, POINTER(GTypePlugin))
GTypePluginCompleteTypeInfo = CFUNCTYPE(None, POINTER(GTypePlugin), GType, POINTER(GTypeInfo), POINTER(GTypeValueTable))
GTypePluginCompleteInterfaceInfo = CFUNCTYPE(None, POINTER(GTypePlugin), GType, GType, POINTER(GInterfaceInfo))

g_type_plugin_use = ctypes_get_func(
	libgobject,
	'g_type_plugin_use',
	None,
	POINTER(GTypePlugin),
)

g_type_plugin_unuse = ctypes_get_func(
	libgobject,
	'g_type_plugin_unuse',
	None,
	POINTER(GTypePlugin),
)

g_type_plugin_complete_type_info = ctypes_get_func(
	libgobject,
	'g_type_plugin_complete_type_info',
	None,
	POINTER(GTypePlugin),
	GType,
	POINTER(GTypeInfo),
	POINTER(GTypeValueTable),
)

g_type_plugin_complete_interface_info = ctypes_get_func(
	libgobject,
	'g_type_plugin_complete_interface_info',
	None,
	POINTER(GTypePlugin),
	GType,
	GType,
	POINTER(GInterfaceInfo),
)

#
# GTypeModule
#
g_type_module_use = ctypes_get_func(
	libgobject,
	'g_type_module_use',
	gboolean,
	POINTER(GTypeModule),
)

g_type_module_unuse = ctypes_get_func(
	libgobject,
	'g_type_module_unuse',
	None,
	POINTER(GTypeModule),
)

g_type_module_set_name = ctypes_get_func(
	libgobject,
	'g_type_module_set_name',
	None,
	POINTER(GTypeModule),
	gchar_p,
)

g_type_module_register_type = ctypes_get_func(
	libgobject,
	'g_type_module_register_type',
	GType,
	POINTER(GTypeModule),
	GType,
	gchar_p,
	POINTER(GTypeInfo),
	GTypeFlags,
)

g_type_module_add_interface = ctypes_get_func(
	libgobject,
	'g_type_module_add_interface',
	None,
	POINTER(GTypeModule),
	GType,
	GType,
	POINTER(GInterfaceInfo),
)

g_type_module_register_enum = ctypes_get_func(
	libgobject,
	'g_type_module_register_enum',
	GType,
	POINTER(GTypeModule),
	gchar_p,
	POINTER(GEnumValue),
)

g_type_module_register_flags = ctypes_get_func(
	libgobject,
	'g_type_module_register_flags',
	GType,
	POINTER(GTypeModule),
	gchar_p,
	POINTER(GFlagsValue),
)

#
# GObject
#
GObjectGetPropertyFunc = CFUNCTYPE(None, POINTER(GObject), guint, POINTER(GValue), POINTER(GParamSpec))
GObjectSetPropertyFunc = CFUNCTYPE(None, POINTER(GObject), guint, POINTER(GValue), POINTER(GParamSpec))
GObjectFinalizeFunc = CFUNCTYPE(None, POINTER(GObject))

g_object_class_install_property = ctypes_get_func(
	libgobject,
	'g_object_class_install_property',
	None,
	POINTER(GObjectClass),
	guint,
	POINTER(GParamSpec),
)

g_object_class_install_properties = ctypes_get_func(
	libgobject,
	'g_object_class_install_properties',
	None,
	POINTER(GObjectClass),
	guint,
	POINTER(GParamSpec),
)

g_object_class_find_property = ctypes_get_func(
	libgobject,
	'g_object_class_find_property',
	POINTER(GParamSpec),
	POINTER(GObjectClass),
	gchar_p,
)

g_object_class_list_properties = ctypes_get_func(
	libgobject,
	'g_object_class_list_properties',
	POINTER(POINTER(GParamSpec)),
	POINTER(GObjectClass),
	POINTER(guint),
)

g_object_class_override_property = ctypes_get_func(
	libgobject,
	'g_object_class_override_property',
	None,
	POINTER(GObjectClass),
	guint,
	gchar_p,
)

g_object_interface_install_property = ctypes_get_func(
	libgobject,
	'g_object_interface_install_property',
	None,
	gpointer,
	POINTER(GParamSpec),
)

g_object_interface_find_property = ctypes_get_func(
	libgobject,
	'g_object_interface_find_property',
	None,
	POINTER(GParamSpec),
	gpointer,
	gchar_p,
)

g_object_interface_list_properties = ctypes_get_func(
	libgobject,
	'g_object_interface_list_properties',
	POINTER(POINTER(GParamSpec)),
	gpointer,
	POINTER(guint),
)

g_object_new = ctypes_get_func(
	libgobject,
	'g_object_new',
	gpointer,
	#GType,
	#gchar_p,
	#...,
)

g_object_newv = ctypes_get_func(
	libgobject,
	'g_object_newv',
	gpointer,
	GType,
	guint,
	POINTER(GParameter),
)

g_object_ref = ctypes_get_func(
	libgobject,
	'g_object_ref',
	gpointer,
	gpointer,
)

g_object_unref = ctypes_get_func(
	libgobject,
	'g_object_unref',
	None,
	gpointer,
)

g_object_ref_sink = ctypes_get_func(
	libgobject,
	'g_object_ref_sink',
	gpointer,
	gpointer,
)

g_object_is_floating = ctypes_get_func(
	libgobject,
	'g_object_is_floating',
	gpointer,
	gpointer,
)

g_object_force_floating = ctypes_get_func(
	libgobject,
	'g_object_force_floating',
	None,
	POINTER(GObject),
)

GWeakNotify = CFUNCTYPE(None, gpointer, POINTER(GObject))

g_object_weak_ref = ctypes_get_func(
	libgobject,
	'g_object_weak_ref',
	None,
	POINTER(GObject),
	GWeakNotify,
	gpointer,
)

g_object_weak_unref = ctypes_get_func(
	libgobject,
	'g_object_weak_unref',
	None,
	POINTER(GObject),
	GWeakNotify,
	gpointer,
)

g_object_add_weak_pointer = ctypes_get_func(
	libgobject,
	'g_object_add_weak_pointer',
	None,
	POINTER(GObject),
	POINTER(gpointer),
)

g_object_remove_weak_pointer = ctypes_get_func(
	libgobject,
	'g_object_remove_weak_pointer',
	None,
	POINTER(GObject),
	POINTER(gpointer),
)

GToggleNotify = CFUNCTYPE(None, gpointer, POINTER(GObject), gboolean)

g_object_add_toggle_ref = ctypes_get_func(
	libgobject,
	'g_object_add_toggle_ref',
	None,
	POINTER(GObject),
	GToggleNotify,
	gpointer,
)

g_object_remove_toggle_ref = ctypes_get_func(
	libgobject,
	'g_object_remove_toggle_ref',
	None,
	POINTER(GObject),
	GToggleNotify,
	gpointer,
)

g_object_connect = ctypes_get_func(
	libgobject,
	'g_object_connect',
	gpointer,
	#gpointer,
	#gchar_p,
	#...,
)

g_object_disconnect = ctypes_get_func(
	libgobject,
	'g_object_disconnect',
	None,
	#gpointer,
	#gchar_p,
	#...,
)

g_object_set = ctypes_get_func(
	libgobject,
	'g_object_set',
	None,
	#gpointer,
	#gchar_p,
	#...,
)

g_object_get = ctypes_get_func(
	libgobject,
	'g_object_get',
	None,
	#gpointer,
	#gchar_p,
	#...,
)

g_object_notify = ctypes_get_func(
	libgobject,
	'g_object_notify',
	None,
	POINTER(GObject),
	gchar_p,
)

g_object_notify_by_pspec = ctypes_get_func(
	libgobject,
	'g_object_notify_by_pspec',
	None,
	POINTER(GObject),
	POINTER(GParamSpec),
)

g_object_freeze_notify = ctypes_get_func(
	libgobject,
	'g_object_freeze_notify',
	None,
	POINTER(GObject),
)

g_object_thaw_notify = ctypes_get_func(
	libgobject,
	'g_object_thaw_notify',
	None,
	POINTER(GObject),
)

g_object_get_data = ctypes_get_func(
	libgobject,
	'g_object_get_data',
	gpointer,
	POINTER(GObject),
	gchar_p,
)

g_object_set_data = ctypes_get_func(
	libgobject,
	'g_object_set_data',
	None,
	POINTER(GObject),
	gchar_p,
	gpointer,
)

g_object_set_data_full = ctypes_get_func(
	libgobject,
	'g_object_set_data_full',
	None,
	POINTER(GObject),
	gchar_p,
	gpointer,
	GDestroyNotify,
)

g_object_steal_data = ctypes_get_func(
	libgobject,
	'g_object_steal_data',
	gpointer,
	POINTER(GObject),
	gchar_p,
)

g_object_get_qdata = ctypes_get_func(
	libgobject,
	'g_object_get_qdata',
	gpointer,
	POINTER(GObject),
	GQuark,
)

g_object_set_qdata = ctypes_get_func(
	libgobject,
	'g_object_set_qdata',
	None,
	POINTER(GObject),
	GQuark,
	gpointer,
)

g_object_set_qdata_full = ctypes_get_func(
	libgobject,
	'g_object_set_qdata_full',
	None,
	POINTER(GObject),
	GQuark,
	gpointer,
	GDestroyNotify,
)

g_object_steal_qdata = ctypes_get_func(
	libgobject,
	'g_object_steal_qdata',
	gpointer,
	POINTER(GObject),
	GQuark,
)

g_object_set_property = ctypes_get_func(
	libgobject,
	'g_object_set_property',
	None,
	POINTER(GObject),
	gchar_p,
	POINTER(GValue),
)

g_object_get_property = ctypes_get_func(
	libgobject,
	'g_object_get_property',
	None,
	POINTER(GObject),
	gchar_p,
	POINTER(GValue),
)

g_object_new_valist = ctypes_get_func(
	libgobject,
	'g_object_new_valist',
	POINTER(GObject),
	GType,
	gchar_p,
	gpointer, # va_list
)

g_object_set_valist = ctypes_get_func(
	libgobject,
	'g_object_set_valist',
	None,
	POINTER(GObject),
	gchar_p,
	gpointer, # va_list
)

g_object_get_valist = ctypes_get_func(
	libgobject,
	'g_object_get_valist',
	None,
	POINTER(GObject),
	gchar_p,
	gpointer, # va_list
)

g_object_watch_closure = ctypes_get_func(
	libgobject,
	'g_object_watch_closure',
	None,
	POINTER(GObject),
	POINTER(GClosure),
)

g_object_run_dispose = ctypes_get_func(
	libgobject,
	'g_object_run_dispose',
	None,
	POINTER(GObject),
)

g_initially_unowned_get_type = ctypes_get_func(
	libgobject,
	'g_initially_unowned_get_type',
	GType,
)

#
# GEnum/GFlags
#
g_enum_get_value = ctypes_get_func(
	libgobject,
	'g_enum_get_value',
	POINTER(GEnumValue),
	POINTER(GEnumClass),
	gint,
)

g_enum_get_value_by_name = ctypes_get_func(
	libgobject,
	'g_enum_get_value_by_name',
	POINTER(GEnumValue),
	POINTER(GEnumClass),
	gchar_p,
)

g_enum_get_value_by_nick = ctypes_get_func(
	libgobject,
	'g_enum_get_value_by_nick',
	POINTER(GEnumValue),
	POINTER(GEnumClass),
	gchar_p,
)

g_flags_get_first_value = ctypes_get_func(
	libgobject,
	'g_flags_get_first_value',
	POINTER(GFlagsValue),
	POINTER(GFlagsClass),
	guint,
)

g_flags_get_value_by_name = ctypes_get_func(
	libgobject,
	'g_flags_get_value_by_name',
	POINTER(GFlagsValue),
	POINTER(GFlagsClass),
	gchar_p,
)

g_flags_get_value_by_nick = ctypes_get_func(
	libgobject,
	'g_flags_get_value_by_nick',
	POINTER(GFlagsValue),
	POINTER(GFlagsClass),
	gchar_p,
)

g_enum_register_static = ctypes_get_func(
	libgobject,
	'g_enum_register_static',
	GType,
	gchar_p,
	POINTER(GEnumValue),
)

g_flags_register_static = ctypes_get_func(
	libgobject,
	'g_flags_register_static',
	GType,
	gchar_p,
	POINTER(GFlagsValue),
)

g_enum_complete_type_info = ctypes_get_func(
	libgobject,
	'g_enum_complete_type_info',
	None,
	GType,
	POINTER(GTypeInfo),
	POINTER(GEnumValue),
)

g_flags_complete_type_info = ctypes_get_func(
	libgobject,
	'g_flags_complete_type_info',
	None,
	GType,
	POINTER(GTypeInfo),
	POINTER(GFlagsValue),
)

#
# GBoxed
#
GBoxedCopyFunc = CFUNCTYPE(gpointer, gpointer)
GBoxedFreeFunc = CFUNCTYPE(None, gpointer)

g_boxed_copy = ctypes_get_func(
	libgobject,
	'g_boxed_copy',
	gpointer,
	GType,
	gconstpointer,
)

g_boxed_free = ctypes_get_func(
	libgobject,
	'g_boxed_free',
	None,
	GType,
	gpointer,
)

g_boxed_type_register_static = ctypes_get_func(
	libgobject,
	'g_boxed_type_register_static',
	GType,
	gchar_p,
	GBoxedCopyFunc,
	GBoxedFreeFunc,
)

g_pointer_type_register_static = ctypes_get_func(
	libgobject,
	'g_pointer_type_register_static',
	GType,
	gchar_p,
)

g_closure_get_type = ctypes_get_func(
	libgobject,
	'g_closure_get_type',
	GType,
)

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

g_date_get_type = ctypes_get_func(
	libgobject,
	'g_date_get_type',
	GType,
)

g_strv_get_type = ctypes_get_func(
	libgobject,
	'g_strv_get_type',
	GType,
)

g_gstring_get_type = ctypes_get_func(
	libgobject,
	'g_gstring_get_type',
	GType,
)

g_hash_table_get_type = ctypes_get_func(
	libgobject,
	'g_hash_table_get_type',
	GType,
)

g_array_get_type = ctypes_get_func(
	libgobject,
	'g_array_get_type',
	GType,
)

g_byte_array_get_type = ctypes_get_func(
	libgobject,
	'g_byte_array_get_type',
	GType,
)

g_ptr_array_get_type = ctypes_get_func(
	libgobject,
	'g_ptr_array_get_type',
	GType,
)

g_variant_type_get_gtype = ctypes_get_func(
	libgobject,
	'g_variant_type_get_gtype',
	GType,
)

g_variant_get_gtype = ctypes_get_func(
	libgobject,
	'g_variant_get_gtype',
	GType,
)

g_regex_get_type = ctypes_get_func(
	libgobject,
	'g_regex_get_type',
	GType,
)

g_error_get_type = ctypes_get_func(
	libgobject,
	'g_error_get_type',
	GType,
)

#
# GValue
#
g_value_init = ctypes_get_func(
	libgobject,
	'g_value_init',
	POINTER(GValue),
	POINTER(GValue),
	GType,
)

g_value_copy = ctypes_get_func(
	libgobject,
	'g_value_copy',
	None,
	POINTER(GValue),
	POINTER(GValue),
)

g_value_reset = ctypes_get_func(
	libgobject,
	'g_value_reset',
	POINTER(GValue),
	POINTER(GValue),
)

g_value_unset = ctypes_get_func(
	libgobject,
	'g_value_unset',
	None,
	POINTER(GValue),
)

g_value_set_instance = ctypes_get_func(
	libgobject,
	'g_value_set_instance',
	None,
	POINTER(GValue),
	gpointer,
)

g_value_fits_pointer = ctypes_get_func(
	libgobject,
	'g_value_fits_pointer',
	gboolean,
	POINTER(GValue),
)

g_value_peek_pointer = ctypes_get_func(
	libgobject,
	'g_value_peek_pointer',
	gboolean,
	POINTER(GValue),
)

g_value_type_compatible = ctypes_get_func(
	libgobject,
	'g_value_type_compatible',
	gboolean,
	GType,
	GType,
)

g_value_type_transformable = ctypes_get_func(
	libgobject,
	'g_value_type_transformable',
	gboolean,
	GType,
	GType,
)

g_value_transform = ctypes_get_func(
	libgobject,
	'g_value_transform',
	gboolean,
	POINTER(GValue),
	POINTER(GValue),
)

GValueTransform = CFUNCTYPE(None, POINTER(GValue), POINTER(GValue))

g_value_register_transform_func = ctypes_get_func(
	libgobject,
	'g_value_register_transform_func',
	None,
	GType,
	GType,
	GValueTransform,
)

g_strdup_value_contents = ctypes_get_func(
	libgobject,
	'g_strdup_value_contents',
	gchar_p,
	POINTER(GValue),
)

#
# GParamSpec/GValue
#
g_param_spec_boolean = ctypes_get_func(
	libgobject,
	'g_param_spec_boolean',
	POINTER(GParamSpec),
	gchar_p,
	gchar_p,
	gchar_p,
	gboolean,
	GParamFlags,
)

g_value_set_boolean = ctypes_get_func(
	libgobject,
	'g_value_set_boolean',
	None,
	POINTER(GValue),
	gboolean,
)

g_value_get_boolean = ctypes_get_func(
	libgobject,
	'g_value_get_boolean',
	gboolean,
	POINTER(GValue),
)

g_param_spec_char = ctypes_get_func(
	libgobject,
	'g_param_spec_char',
	POINTER(GParamSpec),
	gchar_p,
	gchar_p,
	gchar_p,
	gint8,
	gint8,
	gint8,
	GParamFlags,
)

g_value_set_char = ctypes_get_func(
	libgobject,
	'g_value_set_char',
	None,
	POINTER(GValue),
	gchar,
)

g_value_get_char = ctypes_get_func(
	libgobject,
	'g_value_get_char',
	gchar,
	POINTER(GValue),
)

g_param_spec_uchar = ctypes_get_func(
	libgobject,
	'g_param_spec_uchar',
	POINTER(GParamSpec),
	gchar_p,
	gchar_p,
	gchar_p,
	guint8,
	guint8,
	guint8,
	GParamFlags,
)

g_value_set_uchar = ctypes_get_func(
	libgobject,
	'g_value_set_uchar',
	None,
	POINTER(GValue),
	guchar,
)

g_value_get_uchar = ctypes_get_func(
	libgobject,
	'g_value_get_uchar',
	guchar,
	POINTER(GValue),
)

g_param_spec_int = ctypes_get_func(
	libgobject,
	'g_param_spec_int',
	POINTER(GParamSpec),
	gchar_p,
	gchar_p,
	gchar_p,
	gint,
	gint,
	gint,
	GParamFlags,
)

g_value_set_int = ctypes_get_func(
	libgobject,
	'g_value_set_int',
	None,
	POINTER(GValue),
	gint,
)

g_value_get_int = ctypes_get_func(
	libgobject,
	'g_value_get_int',
	gint,
	POINTER(GValue),
)

g_param_spec_uint = ctypes_get_func(
	libgobject,
	'g_param_spec_uint',
	POINTER(GParamSpec),
	gchar_p,
	gchar_p,
	gchar_p,
	guint,
	guint,
	guint,
	GParamFlags,
)

g_value_set_uint = ctypes_get_func(
	libgobject,
	'g_value_set_uint',
	None,
	POINTER(GValue),
	guint,
)

g_value_get_uint = ctypes_get_func(
	libgobject,
	'g_value_get_uint',
	guint,
	POINTER(GValue),
)

g_param_spec_long = ctypes_get_func(
	libgobject,
	'g_param_spec_long',
	POINTER(GParamSpec),
	gchar_p,
	gchar_p,
	gchar_p,
	glong,
	glong,
	glong,
	GParamFlags,
)

g_value_set_long = ctypes_get_func(
	libgobject,
	'g_value_set_long',
	None,
	POINTER(GValue),
	glong,
)

g_value_get_long = ctypes_get_func(
	libgobject,
	'g_value_get_long',
	glong,
	POINTER(GValue),
)

g_param_spec_ulong = ctypes_get_func(
	libgobject,
	'g_param_spec_ulong',
	POINTER(GParamSpec),
	gchar_p,
	gchar_p,
	gchar_p,
	gulong,
	gulong,
	gulong,
	GParamFlags,
)

g_value_set_ulong = ctypes_get_func(
	libgobject,
	'g_value_set_ulong',
	None,
	POINTER(GValue),
	gulong,
)

g_value_get_ulong = ctypes_get_func(
	libgobject,
	'g_value_get_ulong',
	gulong,
	POINTER(GValue),
)

g_param_spec_int64 = ctypes_get_func(
	libgobject,
	'g_param_spec_int64',
	POINTER(GParamSpec),
	gchar_p,
	gchar_p,
	gchar_p,
	gint64,
	gint64,
	gint64,
	GParamFlags,
)

g_value_set_int64 = ctypes_get_func(
	libgobject,
	'g_value_set_int64',
	None,
	POINTER(GValue),
	gint64,
)

g_value_get_int64 = ctypes_get_func(
	libgobject,
	'g_value_get_int64',
	gint64,
	POINTER(GValue),
)

g_param_spec_uint64 = ctypes_get_func(
	libgobject,
	'g_param_spec_uint64',
	POINTER(GParamSpec),
	gchar_p,
	gchar_p,
	gchar_p,
	guint64,
	guint64,
	guint64,
	GParamFlags,
)

g_value_set_uint64 = ctypes_get_func(
	libgobject,
	'g_value_set_uint64',
	None,
	POINTER(GValue),
	guint64,
)

g_value_get_uint64 = ctypes_get_func(
	libgobject,
	'g_value_get_uint64',
	guint64,
	POINTER(GValue),
)

g_param_spec_float = ctypes_get_func(
	libgobject,
	'g_param_spec_float',
	POINTER(GParamSpec),
	gchar_p,
	gchar_p,
	gchar_p,
	gfloat,
	gfloat,
	gfloat,
	GParamFlags,
)

g_value_set_float = ctypes_get_func(
	libgobject,
	'g_value_set_float',
	None,
	POINTER(GValue),
	gfloat,
)

g_value_get_float = ctypes_get_func(
	libgobject,
	'g_value_get_float',
	gfloat,
	POINTER(GValue),
)

g_param_spec_double = ctypes_get_func(
	libgobject,
	'g_param_spec_double',
	POINTER(GParamSpec),
	gchar_p,
	gchar_p,
	gchar_p,
	gdouble,
	gdouble,
	gdouble,
	GParamFlags,
)

g_value_set_double = ctypes_get_func(
	libgobject,
	'g_value_set_double',
	None,
	POINTER(GValue),
	gdouble,
)

g_value_get_double = ctypes_get_func(
	libgobject,
	'g_value_get_double',
	gdouble,
	POINTER(GValue),
)

g_param_spec_enum = ctypes_get_func(
	libgobject,
	'g_param_spec_enum',
	POINTER(GParamSpec),
	gchar_p,
	gchar_p,
	gchar_p,
	GType,
	gint,
	GParamFlags,
)

g_value_set_enum = ctypes_get_func(
	libgobject,
	'g_value_set_enum',
	None,
	POINTER(GValue),
	gint,
)

g_value_get_enum = ctypes_get_func(
	libgobject,
	'g_value_get_enum',
	gint,
	POINTER(GValue),
)

g_param_spec_flags = ctypes_get_func(
	libgobject,
	'g_param_spec_flags',
	POINTER(GParamSpec),
	gchar_p,
	gchar_p,
	gchar_p,
	GType,
	guint,
	GParamFlags,
)

g_value_set_flags = ctypes_get_func(
	libgobject,
	'g_value_set_flags',
	None,
	POINTER(GValue),
	guint,
)

g_value_get_flags = ctypes_get_func(
	libgobject,
	'g_value_get_flags',
	guint,
	POINTER(GValue),
)

g_param_spec_string = ctypes_get_func(
	libgobject,
	'g_param_spec_string',
	POINTER(GParamSpec),
	gchar_p,
	gchar_p,
	gchar_p,
	gchar_p,
	GParamFlags,
)

g_value_set_string = ctypes_get_func(
	libgobject,
	'g_value_set_string',
	None,
	POINTER(GValue),
	gchar_p,
)

g_value_set_static_string = ctypes_get_func(
	libgobject,
	'g_value_set_static_string',
	None,
	POINTER(GValue),
	gchar_p,
)

g_value_take_string = ctypes_get_func(
	libgobject,
	'g_value_take_string',
	None,
	POINTER(GValue),
	gchar_p,
)

g_value_set_string_take_ownership = ctypes_get_func(
	libgobject,
	'g_value_set_string_take_ownership',
	None,
	POINTER(GValue),
	gchar_p,
)

g_value_get_string = ctypes_get_func(
	libgobject,
	'g_value_get_string',
	gchar_p,
	POINTER(GValue),
)

g_value_dup_string = ctypes_get_func(
	libgobject,
	'g_value_dup_string',
	gchar_p,
	POINTER(GValue),
)

g_param_spec_param = ctypes_get_func(
	libgobject,
	'g_param_spec_param',
	POINTER(GParamSpec),
	gchar_p,
	gchar_p,
	gchar_p,
	GType,
	GParamFlags,
)

g_value_set_param = ctypes_get_func(
	libgobject,
	'g_value_set_param',
	None,
	POINTER(GValue),
	POINTER(GParamSpec),
)

g_value_take_param = ctypes_get_func(
	libgobject,
	'g_value_take_param',
	None,
	POINTER(GValue),
	POINTER(GParamSpec),
)

g_value_set_param_take_ownership = ctypes_get_func(
	libgobject,
	'g_value_set_param_take_ownership',
	None,
	POINTER(GValue),
	POINTER(GParamSpec),
)

g_value_get_param = ctypes_get_func(
	libgobject,
	'g_value_get_param',
	POINTER(GParamSpec),
	POINTER(GValue),
)

g_value_dup_param = ctypes_get_func(
	libgobject,
	'g_value_dup_param',
	POINTER(GParamSpec),
	POINTER(GValue),
)

g_param_spec_boxed = ctypes_get_func(
	libgobject,
	'g_param_spec_boxed',
	POINTER(GParamSpec),
	gchar_p,
	gchar_p,
	gchar_p,
	GType,
	GParamFlags,
)

g_value_set_boxed = ctypes_get_func(
	libgobject,
	'g_value_set_boxed',
	None,
	POINTER(GValue),
	gconstpointer,
)

g_value_set_static_boxed = ctypes_get_func(
	libgobject,
	'g_value_set_static_boxed',
	None,
	POINTER(GValue),
	gconstpointer,
)

g_value_take_boxed = ctypes_get_func(
	libgobject,
	'g_value_take_boxed',
	None,
	POINTER(GValue),
	gconstpointer,
)

g_value_set_boxed_take_ownership = ctypes_get_func(
	libgobject,
	'g_value_set_boxed_take_ownership',
	None,
	POINTER(GValue),
	gconstpointer,
)

g_value_get_boxed = ctypes_get_func(
	libgobject,
	'g_value_get_boxed',
	gpointer,
	POINTER(GValue),
)

g_value_dup_boxed = ctypes_get_func(
	libgobject,
	'g_value_dup_boxed',
	gpointer,
	POINTER(GValue),
)

g_param_spec_pointer = ctypes_get_func(
	libgobject,
	'g_param_spec_pointer',
	POINTER(GParamSpec),
	gchar_p,
	gchar_p,
	gchar_p,
	GParamFlags,
)

g_value_set_pointer = ctypes_get_func(
	libgobject,
	'g_value_set_pointer',
	None,
	POINTER(GValue),
	gpointer,
)

g_value_get_pointer = ctypes_get_func(
	libgobject,
	'g_value_get_pointer',
	gpointer,
	POINTER(GValue),
)

g_gtype_get_type = ctypes_get_func(
	libgobject,
	'g_gtype_get_type',
	GType,
)

g_param_spec_object = ctypes_get_func(
	libgobject,
	'g_param_spec_object',
	POINTER(GParamSpec),
	gchar_p,
	gchar_p,
	gchar_p,
	GType,
	GParamFlags,
)

g_value_set_object = ctypes_get_func(
	libgobject,
	'g_value_set_object',
	None,
	POINTER(GValue),
	gpointer,
)

g_value_take_object = ctypes_get_func(
	libgobject,
	'g_value_take_object',
	None,
	POINTER(GValue),
	gpointer,
)

g_value_set_object_take_ownership = ctypes_get_func(
	libgobject,
	'g_value_set_object_take_ownership',
	None,
	POINTER(GValue),
	gpointer,
)

g_value_get_object = ctypes_get_func(
	libgobject,
	'g_value_get_object',
	gpointer,
	POINTER(GValue),
)

g_value_dup_object = ctypes_get_func(
	libgobject,
	'g_value_dup_object',
	gpointer,
	POINTER(GValue),
)

g_param_spec_unichar = ctypes_get_func(
	libgobject,
	'g_param_spec_unichar',
	POINTER(GParamSpec),
	gchar_p,
	gchar_p,
	gchar_p,
	gunichar,
	GParamFlags,
)

g_param_spec_value_array = ctypes_get_func(
	libgobject,
	'g_param_spec_value_array',
	POINTER(GParamSpec),
	gchar_p,
	gchar_p,
	gchar_p,
	POINTER(GParamSpec),
	GParamFlags,
)

g_param_spec_override = ctypes_get_func(
	libgobject,
	'g_param_spec_override',
	POINTER(GParamSpec),
	gchar_p,
	POINTER(GParamSpec),
)

g_param_spec_gtype = ctypes_get_func(
	libgobject,
	'g_param_spec_gtype',
	POINTER(GParamSpec),
	gchar_p,
	gchar_p,
	gchar_p,
	GType,
	GParamFlags,
)

g_value_get_gtype = ctypes_get_func(
	libgobject,
	'g_value_get_gtype',
	GType,
	POINTER(GValue),
)

g_value_set_gtype = ctypes_get_func(
	libgobject,
	'g_value_set_gtype',
	None,
	POINTER(GValue),
	GType,
)

g_param_spec_variant = ctypes_get_func(
	libgobject,
	'g_param_spec_variant',
	POINTER(GParamSpec),
	gchar_p,
	gchar_p,
	gchar_p,
	POINTER(GVariantType),
	POINTER(GVariant),
	GParamFlags,
)

g_value_get_variant = ctypes_get_func(
	libgobject,
	'g_value_get_variant',
	POINTER(GVariant),
	POINTER(GValue),
)

g_value_dup_variant = ctypes_get_func(
	libgobject,
	'g_value_dup_variant',
	POINTER(GVariant),
	POINTER(GValue),
)

g_value_set_variant = ctypes_get_func(
	libgobject,
	'g_value_set_variant',
	None,
	POINTER(GValue),
	POINTER(GVariant),
)

g_value_take_variant = ctypes_get_func(
	libgobject,
	'g_value_take_variant',
	None,
	POINTER(GValue),
	POINTER(GVariant),
)

#
# GParamSpec
#
g_param_spec_ref = ctypes_get_func(
	libgobject,
	'g_param_spec_ref',
	POINTER(GParamSpec),
	POINTER(GParamSpec),
)

g_param_spec_unref = ctypes_get_func(
	libgobject,
	'g_param_spec_unref',
	None,
	POINTER(GParamSpec),
)

g_param_spec_sink = ctypes_get_func(
	libgobject,
	'g_param_spec_sink',
	None,
	POINTER(GParamSpec),
)

g_param_spec_ref_sink = ctypes_get_func(
	libgobject,
	'g_param_spec_ref_sink',
	POINTER(GParamSpec),
	POINTER(GParamSpec),
)

g_param_value_set_default = ctypes_get_func(
	libgobject,
	'g_param_value_set_default',
	None,
	POINTER(GParamSpec),
	POINTER(GValue),
)

g_param_value_defaults = ctypes_get_func(
	libgobject,
	'g_param_value_defaults',
	gboolean,
	POINTER(GParamSpec),
	POINTER(GValue),
)

g_param_value_validate = ctypes_get_func(
	libgobject,
	'g_param_value_validate',
	gboolean,
	POINTER(GParamSpec),
	POINTER(GValue),
)

g_param_value_convert = ctypes_get_func(
	libgobject,
	'g_param_value_convert',
	gboolean,
	POINTER(GParamSpec),
	POINTER(GValue),
	POINTER(GValue),
	gboolean,
)

g_param_values_cmp = ctypes_get_func(
	libgobject,
	'g_param_values_cmp',
	gint,
	POINTER(GParamSpec),
	POINTER(GValue),
	POINTER(GValue),
)

g_param_spec_get_name = ctypes_get_func(
	libgobject,
	'g_param_spec_get_name',
	gchar,
	POINTER(GParamSpec),
)

g_param_spec_get_nick = ctypes_get_func(
	libgobject,
	'g_param_spec_get_nick',
	gchar,
	POINTER(GParamSpec),
)

g_param_spec_get_blurb = ctypes_get_func(
	libgobject,
	'g_param_spec_get_blurb',
	gchar,
	POINTER(GParamSpec),
)

g_param_spec_get_qdata = ctypes_get_func(
	libgobject,
	'g_param_spec_get_qdata',
	gpointer,
	POINTER(GParamSpec),
	GQuark,
)

g_param_spec_set_qdata = ctypes_get_func(
	libgobject,
	'g_param_spec_set_qdata',
	None,
	POINTER(GParamSpec),
	GQuark,
	gpointer,
)

g_param_spec_set_qdata_full = ctypes_get_func(
	libgobject,
	'g_param_spec_set_qdata_full',
	None,
	POINTER(GParamSpec),
	GQuark,
	gpointer,
	GDestroyNotify,
)

g_param_spec_steal_qdata = ctypes_get_func(
	libgobject,
	'g_param_spec_steal_qdata',
	gpointer,
	POINTER(GParamSpec),
	GQuark,
)

g_param_spec_get_redirect_target = ctypes_get_func(
	libgobject,
	'g_param_spec_get_redirect_target',
	POINTER(GParamSpec),
	POINTER(GParamSpec),
)

g_param_spec_internal = ctypes_get_func(
	libgobject,
	'g_param_spec_internal',
	gpointer,
	gchar_p,
	gchar_p,
	gchar_p,
	GParamFlags,
)

g_param_type_register_static = ctypes_get_func(
	libgobject,
	'g_param_type_register_static',
	GType,
	gchar_p,
	POINTER(GParamSpecTypeInfo),
)

g_param_spec_pool_new = ctypes_get_func(
	libgobject,
	'g_param_spec_pool_new',
	POINTER(GParamSpecPool),
	gboolean,
)

g_param_spec_pool_insert = ctypes_get_func(
	libgobject,
	'g_param_spec_pool_insert',
	None,
	POINTER(GParamSpecPool),
	POINTER(GParamSpec),
	GType,
)

g_param_spec_pool_remove = ctypes_get_func(
	libgobject,
	'g_param_spec_pool_remove',
	None,
	POINTER(GParamSpecPool),
	POINTER(GParamSpec),
)

g_param_spec_pool_lookup = ctypes_get_func(
	libgobject,
	'g_param_spec_pool_lookup',
	POINTER(GParamSpec),
	POINTER(GParamSpecPool),
	gchar_p,
	GType,
	gboolean,
)

g_param_spec_pool_list = ctypes_get_func(
	libgobject,
	'g_param_spec_pool_list',
	POINTER(POINTER(GParamSpec)),
	POINTER(GParamSpecPool),
	GType,
	POINTER(guint),
)

g_param_spec_pool_list_owned = ctypes_get_func(
	libgobject,
	'g_param_spec_pool_list_owned',
	POINTER(GList),
	POINTER(GParamSpecPool),
	GType,
)

#
# GTypeCValue
#

#
# GClosure
#
GCallback = CFUNCTYPE(None)
GClosureMarshal = CFUNCTYPE(None, POINTER(GClosure), POINTER(GValue), guint, POINTER(GValue), gpointer, gpointer)
GClosureNotify = CFUNCTYPE(None, gpointer, POINTER(GClosure))

g_cclosure_new = ctypes_get_func(
	libgobject,
	'g_cclosure_new',
	POINTER(GClosure),
	GCallback,
	gpointer,
	GClosureNotify,
)

g_cclosure_new_swap = ctypes_get_func(
	libgobject,
	'g_cclosure_new_swap',
	POINTER(GClosure),
	GCallback,
	gpointer,
	GClosureNotify,
)

g_cclosure_new_object = ctypes_get_func(
	libgobject,
	'g_cclosure_new_object',
	POINTER(GClosure),
	GCallback,
	POINTER(GObject),
)

g_cclosure_new_object_swap = ctypes_get_func(
	libgobject,
	'g_cclosure_new_object_swap',
	POINTER(GClosure),
	GCallback,
	POINTER(GObject),
)

g_closure_new_object = ctypes_get_func(
	libgobject,
	'g_closure_new_object',
	POINTER(GClosure),
	guint,
	POINTER(GObject),
)

g_closure_ref = ctypes_get_func(
	libgobject,
	'g_closure_ref',
	POINTER(GClosure),
	POINTER(GClosure),
)

g_closure_sink = ctypes_get_func(
	libgobject,
	'g_closure_sink',
	None,
	POINTER(GClosure),
)

g_closure_unref = ctypes_get_func(
	libgobject,
	'g_closure_unref',
	None,
	POINTER(GClosure),
)

g_closure_invoke = ctypes_get_func(
	libgobject,
	'g_closure_invoke',
	None,
	POINTER(GClosure),
	POINTER(GValue),
	guint,
	POINTER(GValue),
	gpointer,
)

g_closure_invalidate = ctypes_get_func(
	libgobject,
	'g_closure_invalidate',
	None,
	POINTER(GClosure),
)

g_closure_add_finalize_notifier = ctypes_get_func(
	libgobject,
	'g_closure_add_finalize_notifier',
	None,
	POINTER(GClosure),
	gpointer,
	GClosureNotify,
)

g_closure_add_invalidate_notifier = ctypes_get_func(
	libgobject,
	'g_closure_add_invalidate_notifier',
	None,
	POINTER(GClosure),
	gpointer,
	GClosureNotify,
)

g_closure_remove_finalize_notifier = ctypes_get_func(
	libgobject,
	'g_closure_remove_finalize_notifier',
	None,
	POINTER(GClosure),
	gpointer,
	GClosureNotify,
)

g_closure_remove_invalidate_notifier = ctypes_get_func(
	libgobject,
	'g_closure_remove_invalidate_notifier',
	None,
	POINTER(GClosure),
	gpointer,
	GClosureNotify,
)

g_closure_new_simple = ctypes_get_func(
	libgobject,
	'g_closure_new_simple',
	POINTER(GClosure),
	guint,
	gpointer,
)

g_closure_set_marshal = ctypes_get_func(
	libgobject,
	'g_closure_set_marshal',
	None,
	POINTER(GClosure),
	GClosureMarshal,
)

g_closure_add_marshal_guards = ctypes_get_func(
	libgobject,
	'g_closure_add_marshal_guards',
	None,
	POINTER(GClosure),
	gpointer,
	GClosureNotify,
	gpointer,
	GClosureNotify,
)

g_closure_set_meta_marshal = ctypes_get_func(
	libgobject,
	'g_closure_set_meta_marshal',
	None,
	POINTER(GClosure),
	gpointer,
	GClosureMarshal,
)

g_source_set_closure = ctypes_get_func(
	libgobject,
	'g_source_set_closure',
	None,
	POINTER(GSource),
	POINTER(GClosure),
)

#
# GSignal
#
GSignalAccumulator = CFUNCTYPE(gpointer, POINTER(GSignalInvocationHint), POINTER(GValue), POINTER(GValue), gpointer)
GSignalEmissionHook = CFUNCTYPE(gpointer, POINTER(GSignalInvocationHint), guint, POINTER(GValue), gpointer)

g_signal_new = ctypes_get_func(
	libgobject,
	'g_signal_new',
	guint,
	#gchar_p,
	#GType,
	#GSignalFlags,
	#guint,
	#GSignalAccumulator,
	#gpointer,
	#GSignalCMarshaller,
	#GType,
	#guint,
	#...
)

g_signal_newv = ctypes_get_func(
	libgobject,
	'g_signal_newv',
	guint,
	gchar_p,
	GType,
	GSignalFlags,
	guint,
	GSignalAccumulator,
	gpointer,
	GSignalCMarshaller,
	GType,
	guint,
	GType,
)

g_signal_new_valist = ctypes_get_func(
	libgobject,
	'g_signal_new_valist',
	guint,
	gchar_p,
	GType,
	GSignalFlags,
	guint,
	GSignalAccumulator,
	gpointer,
	GSignalCMarshaller,
	GType,
	guint,
	gpointer,
)

g_signal_query = ctypes_get_func(
	libgobject,
	'g_signal_query',
	None,
	guint,
	POINTER(GSignalQuery),
)

g_signal_lookup = ctypes_get_func(
	libgobject,
	'g_signal_lookup',
	guint,
	gchar_p,
	GType,
)

g_signal_name = ctypes_get_func(
	libgobject,
	'g_signal_name',
	gchar_p,
	guint,
)

g_signal_list_ids = ctypes_get_func(
	libgobject,
	'g_signal_list_ids',
	POINTER(guint),
	GType,
	POINTER(guint),
)

g_signal_emit = ctypes_get_func(
	libgobject,
	'g_signal_emit',
	None,
	#gpointer,
	#guint,
	#GQuark,
	#...
)

g_signal_emit_by_name = ctypes_get_func(
	libgobject,
	'g_signal_emit_by_name',
	None,
	#gpointer,
	#gchar_p,
	#...
)

g_signal_emitv = ctypes_get_func(
	libgobject,
	'g_signal_emitv',
	None,
	POINTER(GValue),
	guint,
	GQuark,
	POINTER(GValue),
)

g_signal_emit_valist = ctypes_get_func(
	libgobject,
	'g_signal_emit_valist',
	None,
	gpointer,
	guint,
	GQuark,
	gpointer,
)

g_signal_connect_object = ctypes_get_func(
	libgobject,
	'g_signal_connect_object',
	gulong,
	gpointer,
	gchar_p,
	GCallback,
	gpointer,
	GConnectFlags,
)

g_signal_connect_data = ctypes_get_func(
	libgobject,
	'g_signal_connect_data',
	gulong,
	gpointer,
	gchar_p,
	GCallback,
	gpointer,
	GClosureNotify,
	GConnectFlags,
)

g_signal_connect_closure = ctypes_get_func(
	libgobject,
	'g_signal_connect_closure',
	gulong,
	gpointer,
	gchar_p,
	POINTER(GClosure),
	gboolean,
)

g_signal_connect_closure_by_id = ctypes_get_func(
	libgobject,
	'g_signal_connect_closure_by_id',
	gulong,
	gpointer,
	guint,
	GQuark,
	POINTER(GClosure),
	gboolean,
)

g_signal_handler_block = ctypes_get_func(
	libgobject,
	'g_signal_handler_block',
	None,
	gpointer,
	gulong,
)

g_signal_handler_unblock = ctypes_get_func(
	libgobject,
	'g_signal_handler_unblock',
	None,
	gpointer,
	gulong,
)

g_signal_handler_disconnect = ctypes_get_func(
	libgobject,
	'g_signal_handler_disconnect',
	None,
	gpointer,
	gulong,
)

g_signal_handler_find = ctypes_get_func(
	libgobject,
	'g_signal_handler_find',
	gulong,
	gpointer,
	GSignalMatchType,
	guint,
	GQuark,
	POINTER(GClosure),
	gpointer,
	gpointer,
)

g_signal_handlers_block_matched = ctypes_get_func(
	libgobject,
	'g_signal_handlers_block_matched',
	guint,
	gpointer,
	GSignalMatchType,
	guint,
	GQuark,
	POINTER(GClosure),
	gpointer,
	gpointer,
)

g_signal_handlers_unblock_matched = ctypes_get_func(
	libgobject,
	'g_signal_handlers_unblock_matched',
	guint,
	gpointer,
	GSignalMatchType,
	guint,
	GQuark,
	POINTER(GClosure),
	gpointer,
	gpointer,
)

g_signal_handlers_disconnect_matched = ctypes_get_func(
	libgobject,
	'g_signal_handlers_disconnect_matched',
	guint,
	gpointer,
	GSignalMatchType,
	guint,
	GQuark,
	POINTER(GClosure),
	gpointer,
	gpointer,
)

g_signal_handler_is_connected = ctypes_get_func(
	libgobject,
	'g_signal_handler_is_connected',
	gboolean,
	gpointer,
	gulong,
)

g_signal_has_handler_pending = ctypes_get_func(
	libgobject,
	'g_signal_has_handler_pending',
	gboolean,
	gpointer,
	guint,
	GQuark,
	gboolean,
)

g_signal_stop_emission = ctypes_get_func(
	libgobject,
	'g_signal_stop_emission',
	None,
	gpointer,
	guint,
	GQuark,
)

g_signal_stop_emission_by_name = ctypes_get_func(
	libgobject,
	'g_signal_stop_emission_by_name',
	None,
	gpointer,
	gchar_p,
)

g_signal_override_class_closure = ctypes_get_func(
	libgobject,
	'g_signal_override_class_closure',
	None,
	guint,
	GType,
	POINTER(GClosure),
)

g_signal_chain_from_overridden = ctypes_get_func(
	libgobject,
	'g_signal_chain_from_overridden',
	None,
	POINTER(GValue),
	POINTER(GValue),
)

g_signal_new_class_handler = ctypes_get_func(
	libgobject,
	'g_signal_new_class_handler',
	guint,
	#gchar_p,
	#GType,
	#GSignalFlags,
	#GCallback,
	#GSignalAccumulator,
	#gpointer,
	#GSignalCMarshaller,
	#GType,
	#guint,
	#...
)

g_signal_override_class_handler = ctypes_get_func(
	libgobject,
	'g_signal_override_class_handler',
	None,
	gchar_p,
	GType,
	GCallback,
)

g_signal_chain_from_overridden_handler = ctypes_get_func(
	libgobject,
	'g_signal_chain_from_overridden_handler',
	None,
	#gpointer,
	#...
)

g_signal_add_emission_hook = ctypes_get_func(
	libgobject,
	'g_signal_add_emission_hook',
	gulong,
	guint,
	GQuark,
	GSignalEmissionHook,
	gpointer,
	GDestroyNotify,
)

g_signal_remove_emission_hook = ctypes_get_func(
	libgobject,
	'g_signal_remove_emission_hook',
	None,
	guint,
	gulong,
)

g_signal_parse_name = ctypes_get_func(
	libgobject,
	'g_signal_parse_name',
	gboolean,
	gchar_p,
	GType,
	POINTER(guint),
	POINTER(GQuark),
	gboolean,
)

g_signal_get_invocation_hint = ctypes_get_func(
	libgobject,
	'g_signal_get_invocation_hint',
	POINTER(GSignalInvocationHint),
	gpointer,
)

g_signal_type_cclosure_new = ctypes_get_func(
	libgobject,
	'g_signal_type_cclosure_new',
	POINTER(GClosure),
	GType,
	guint,
)

g_signal_accumulator_true_handled = ctypes_get_func(
	libgobject,
	'g_signal_accumulator_true_handled',
	gboolean,
	POINTER(GSignalInvocationHint),
	POINTER(GValue),
	POINTER(GValue),
	gpointer,
)

#
# GValueArray
#
g_value_array_get_nth = ctypes_get_func(
	libgobject,
	'g_value_array_get_nth',
	POINTER(GValue),
	POINTER(GValueArray),
	guint,
)

g_value_array_new = ctypes_get_func(
	libgobject,
	'g_value_array_new',
	POINTER(GValueArray),
	guint,
)

g_value_array_copy = ctypes_get_func(
	libgobject,
	'g_value_array_copy',
	POINTER(GValueArray),
	POINTER(GValueArray),
)

g_value_array_free = ctypes_get_func(
	libgobject,
	'g_value_array_free',
	None,
	POINTER(GValueArray),
)

g_value_array_append = ctypes_get_func(
	libgobject,
	'g_value_array_append',
	POINTER(GValueArray),
	POINTER(GValueArray),
	POINTER(GValue),
)

g_value_array_prepend = ctypes_get_func(
	libgobject,
	'g_value_array_prepend',
	POINTER(GValueArray),
	POINTER(GValueArray),
	POINTER(GValue),
)

g_value_array_insert = ctypes_get_func(
	libgobject,
	'g_value_array_insert',
	POINTER(GValueArray),
	POINTER(GValueArray),
	guint,
	POINTER(GValue),
)

g_value_array_remove = ctypes_get_func(
	libgobject,
	'g_value_array_remove',
	POINTER(GValueArray),
	POINTER(GValueArray),
	guint,
)

g_value_array_sort = ctypes_get_func(
	libgobject,
	'g_value_array_sort',
	POINTER(GValueArray),
	POINTER(GValueArray),
	GCompareFunc,
)

g_value_array_sort_with_data = ctypes_get_func(
	libgobject,
	'g_value_array_sort_with_data',
	POINTER(GValueArray),
	POINTER(GValueArray),
	GCompareDataFunc,
	gpointer,
)

#
# GBinding
#
g_binding_get_source = ctypes_get_func(
	libgobject,
	'g_binding_get_source',
	POINTER(GObject),
	POINTER(GBinding),
)

g_binding_get_source_property = ctypes_get_func(
	libgobject,
	'g_binding_get_source_property',
	gchar_p,
	POINTER(GBinding),
)

g_binding_get_target = ctypes_get_func(
	libgobject,
	'g_binding_get_target',
	POINTER(GObject),
	POINTER(GBinding),
)

g_binding_get_target_property = ctypes_get_func(
	libgobject,
	'g_binding_get_target_property',
	gchar_p,
	POINTER(GBinding),
)

g_binding_get_flags = ctypes_get_func(
	libgobject,
	'g_binding_get_flags',
	GBindingFlags,
	POINTER(GBinding),
)

g_object_bind_property = ctypes_get_func(
	libgobject,
	'g_object_bind_property',
	POINTER(GBinding),
	gpointer,
	gchar_p,
	gpointer,
	gchar_p,
	GBindingFlags,
)

GBindingTransformFunc = CFUNCTYPE(gboolean, POINTER(GBinding), POINTER(GValue), POINTER(GValue), gpointer)

g_object_bind_property_full = ctypes_get_func(
	libgobject,
	'g_object_bind_property_full',
	POINTER(GBinding),
	gpointer,
	gchar_p,
	gpointer,
	gchar_p,
	GBindingFlags,
	GBindingTransformFunc,
	GBindingTransformFunc,
	gpointer,
	GDestroyNotify,
)

g_object_bind_property_with_closures = ctypes_get_func(
	libgobject,
	'g_object_bind_property_with_closures',
	POINTER(GBinding),
	gpointer,
	gchar_p,
	gpointer,
	gchar_p,
	GBindingFlags,
	POINTER(GClosure),
	POINTER(GClosure),
)

#
# GType
#
G_TYPE_FUNDAMENTAL = lambda type_: g_type_fundamental(type_)
G_TYPE_FUNDAMENTAL_SHIFT = gint(2)
G_TYPE_FUNDAMENTAL_MAX = GType(255 << G_TYPE_FUNDAMENTAL_SHIFT.value)
G_TYPE_MAKE_FUNDAMENTAL = lambda x: GType(x.value << G_TYPE_FUNDAMENTAL_SHIFT.value)
G_TYPE_IS_ABSTRACT = lambda type_: g_type_test_flags(type_, G_TYPE_FLAG_ABSTRACT)
G_TYPE_IS_DERIVED = lambda type_: gboolean(type_.value > G_TYPE_FUNDAMENTAL_MAX.value)
G_TYPE_IS_FUNDAMENTAL = lambda type_: gboolean(type_.value <= G_TYPE_FUNDAMENTAL_MAX.value)
G_TYPE_IS_VALUE_TYPE = lambda type_: g_type_check_is_value_type(type_)
G_TYPE_HAS_VALUE_TABLE = lambda type_: bool(g_type_value_table_peek(type_))
G_TYPE_IS_CLASSED = lambda type_: g_type_test_flags(type_, G_TYPE_FLAG_CLASSED)
G_TYPE_IS_INSTANTIATABLE = lambda type_: g_type_test_flags(type_, G_TYPE_FLAG_INSTANTIATABLE)
G_TYPE_IS_DERIVABLE = lambda type_: g_type_test_flags(type_, G_TYPE_FLAG_DERIVABLE)
G_TYPE_IS_DEEP_DERIVABLE = lambda type_: g_type_test_flags(type_, G_TYPE_FLAG_DEEP_DERIVABLE)
G_TYPE_IS_INTERFACE = lambda type_: gboolean(G_TYPE_FUNDAMENTAL(type_).value == G_TYPE_INTERFACE.value)
G_TYPE_FROM_INSTANCE = lambda instance: G_TYPE_FROM_CLASS(cast(instance, POINTER(GTypeInstance)).g_class)
G_TYPE_FROM_CLASS = lambda g_class: cast(g_class, POINTER(GTypeClass)).g_type
G_TYPE_FROM_INTERFACE = lambda g_iface: cast(g_iface, POINTER(GTypeInterface)).g_type
G_TYPE_INSTANCE_GET_CLASS = lambda instance, g_type, c_type: _G_TYPE_IGC(instance, g_type, c_type)
G_TYPE_INSTANCE_GET_INTERFACE = lambda instance, g_type, c_type: _G_TYPE_IGI(instance, g_type, c_type)
G_TYPE_INSTANCE_GET_PRIVATE = lambda instance, g_type, c_type: cast(g_type_instance_get_private(cast(instance, POINTER(GTypeInstance)), g_type), POINTER(c_type))
G_TYPE_CLASS_GET_PRIVATE = lambda klass, g_type, c_type: cast(g_type_class_get_private (cast(klass, POINTER(GTypeClass)), g_type), POINTER(c_type))
G_TYPE_CHECK_INSTANCE = lambda instance: _G_TYPE_CHI(cast(instance, POINTER(GTypeInstance)))
G_TYPE_CHECK_INSTANCE_CAST = lambda instance, g_type, c_type: _G_TYPE_CIC(instance, g_type, c_type)
G_TYPE_CHECK_INSTANCE_TYPE = lambda instance, g_type: _G_TYPE_CIT(instance, g_type)
G_TYPE_CHECK_CLASS_CAST = lambda g_class, g_type, c_type: _G_TYPE_CCC(g_class, g_type, c_type)
G_TYPE_CHECK_CLASS_TYPE = lambda g_class, g_type: _G_TYPE_CCT(g_class, g_type)
G_TYPE_CHECK_VALUE = lambda value: _G_TYPE_CHV(value)
G_TYPE_CHECK_VALUE_TYPE = lambda value, g_type: _G_TYPE_CVH(value, g_type)
G_TYPE_FLAG_RESERVED_ID_BIT = GType(1 << 0)

G_DEFINE_TYPE = lambda TN, t_n, T_P: G_DEFINE_TYPE_EXTENDED(TN, t_n, T_P, gint(0), None)

def G_DEFINE_TYPE_WITH_CODE(TN, t_n, T_P, _C_):
	_G_DEFINE_TYPE_EXTENDED_BEGIN(TN, t_n, T_P, gint(0))
	if _C_: _C_()
	_G_DEFINE_TYPE_EXTENDED_END()

G_DEFINE_ABSTRACT_TYPE = lambda TN, t_n, T_P: G_DEFINE_TYPE_EXTENDED(TN, t_n, T_P, G_TYPE_FLAG_ABSTRACT, None)

def G_DEFINE_ABSTRACT_TYPE_WITH_CODE(TN, t_n, T_P, _C_):
	_G_DEFINE_TYPE_EXTENDED_BEGIN(TN, t_n, T_P, G_TYPE_FLAG_ABSTRACT)
	if _C_: _C_()
	_G_DEFINE_TYPE_EXTENDED_END()

G_DEFINE_INTERFACE = lambda TN, t_n, T_P: G_DEFINE_INTERFACE_WITH_CODE(TN, t_n, T_P, None)

def G_DEFINE_INTERFACE_WITH_CODE(TN, t_n, T_P, _C_):
	_G_DEFINE_INTERFACE_EXTENDED_BEGIN(TN, t_n, T_P)
	if _C_: _C_()
	_G_DEFINE_INTERFACE_EXTENDED_END()

G_IMPLEMENT_INTERFACE = lambda TYPE_IFACE, iface_init: None

def G_DEFINE_TYPE_EXTENDED(TN, t_n, T_P, _f_, _C_):
	_G_DEFINE_TYPE_EXTENDED_BEGIN(TN, t_n, T_P, _f_)
	if _C_: _C_()
	_G_DEFINE_TYPE_EXTENDED_END()

G_DEFINE_BOXED_TYPE = lambda TypeName, type_name, copy_func, free_func: G_DEFINE_BOXED_TYPE_WITH_CODE(TypeName, type_name, copy_func, free_func, None)

def G_DEFINE_BOXED_TYPE_WITH_CODE(TypeName, type_name, copy_func, free_func, _C_):
	_G_DEFINE_BOXED_TYPE_BEGIN(TypeName, type_name, copy_func, free_func)
	if _C_: _C_()
	_G_DEFINE_TYPE_EXTENDED_END()

G_DEFINE_POINTER_TYPE = lambda TypeName, type_name: G_DEFINE_POINTER_TYPE_WITH_CODE(TypeName, type_name, None)

def G_DEFINE_POINTER_TYPE_WITH_CODE(TypeName, type_name, _C_):
	_G_DEFINE_POINTER_TYPE_BEGIN(TypeName, type_name)
	if _C_: _C_()
	_G_DEFINE_TYPE_EXTENDED_END()

G_TYPE_GTYPE = g_gtype_get_type()
G_TYPE_INVALID = G_TYPE_MAKE_FUNDAMENTAL(gint(0))
G_TYPE_NONE = G_TYPE_MAKE_FUNDAMENTAL(gint(1))
G_TYPE_INTERFACE = G_TYPE_MAKE_FUNDAMENTAL(gint(2))
G_TYPE_CHAR = G_TYPE_MAKE_FUNDAMENTAL(gint(3))
G_TYPE_UCHAR = G_TYPE_MAKE_FUNDAMENTAL(gint(4))
G_TYPE_BOOLEAN = G_TYPE_MAKE_FUNDAMENTAL(gint(5))
G_TYPE_INT = G_TYPE_MAKE_FUNDAMENTAL(gint(6))
G_TYPE_UINT = G_TYPE_MAKE_FUNDAMENTAL(gint(7))
G_TYPE_LONG = G_TYPE_MAKE_FUNDAMENTAL(gint(8))
G_TYPE_ULONG = G_TYPE_MAKE_FUNDAMENTAL(gint(9))
G_TYPE_INT64 = G_TYPE_MAKE_FUNDAMENTAL(gint(10))
G_TYPE_UINT64 = G_TYPE_MAKE_FUNDAMENTAL(gint(11))
G_TYPE_ENUM = G_TYPE_MAKE_FUNDAMENTAL(gint(12))
G_TYPE_FLAGS = G_TYPE_MAKE_FUNDAMENTAL(gint(13))
G_TYPE_FLOAT = G_TYPE_MAKE_FUNDAMENTAL(gint(14))
G_TYPE_DOUBLE = G_TYPE_MAKE_FUNDAMENTAL(gint(15))
G_TYPE_STRING = G_TYPE_MAKE_FUNDAMENTAL(gint(16))
G_TYPE_POINTER = G_TYPE_MAKE_FUNDAMENTAL(gint(17))
G_TYPE_BOXED = G_TYPE_MAKE_FUNDAMENTAL(gint(18))
G_TYPE_PARAM = G_TYPE_MAKE_FUNDAMENTAL(gint(19))
G_TYPE_OBJECT = G_TYPE_MAKE_FUNDAMENTAL(gint(20))
G_TYPE_VARIANT = G_TYPE_MAKE_FUNDAMENTAL(gint(21))
G_TYPE_RESERVED_GLIB_FIRST = G_TYPE_MAKE_FUNDAMENTAL(gint(22))
G_TYPE_RESERVED_GLIB_LAST = G_TYPE_MAKE_FUNDAMENTAL(gint(31))
G_TYPE_RESERVED_BSE_FIRST = G_TYPE_MAKE_FUNDAMENTAL(gint(32))
G_TYPE_RESERVED_BSE_LAST = G_TYPE_MAKE_FUNDAMENTAL(gint(48))
G_TYPE_RESERVED_BSE_LAST = G_TYPE_MAKE_FUNDAMENTAL(gint(49))

#
# GTypeModule
#
G_DEFINE_DYNAMIC_TYPE = lambda TN, t_n, T_P: G_DEFINE_DYNAMIC_TYPE_EXTENDED(TN, t_n, T_P, gint(0), None)
def G_DEFINE_DYNAMIC_TYPE_EXTENDED(TypeName, type_name, TYPE_PARENT, flags, CODE): pass
def G_IMPLEMENT_INTERFACE_DYNAMIC(TYPE_IFACE, iface_init): pass

#
# GObject
#
G_TYPE_IS_OBJECT = lambda type_: gboolean(G_TYPE_FUNDAMENTAL(type_).value == G_TYPE_OBJECT.value)
G_OBJECT = lambda object_: G_TYPE_CHECK_INSTANCE_CAST(object_, G_TYPE_OBJECT, GObject)
G_IS_OBJECT = lambda object_: G_TYPE_CHECK_INSTANCE_TYPE(object_, G_TYPE_OBJECT)
G_OBJECT_CLASS = lambda class_: G_TYPE_CHECK_CLASS_CAST(class_, G_TYPE_OBJECT, GObjectClass)
G_IS_OBJECT_CLASS = lambda class_: G_TYPE_CHECK_CLASS_TYPE (class_, G_TYPE_OBJECT)
G_OBJECT_GET_CLASS = lambda object_: G_TYPE_INSTANCE_GET_CLASS(object_, G_TYPE_OBJECT, GObjectClass)
G_OBJECT_TYPE = lambda object_: G_TYPE_FROM_INSTANCE(object_)
G_OBJECT_TYPE_NAME = lambda object_: g_type_name(G_OBJECT_TYPE(object_))
G_OBJECT_CLASS_TYPE = lambda class_: G_TYPE_FROM_CLASS(class_)
G_OBJECT_CLASS_NAME = lambda class_: g_type_name(G_OBJECT_CLASS_TYPE(class_))

G_TYPE_INITIALLY_UNOWNED = g_initially_unowned_get_type()

def G_OBJECT_WARN_INVALID_PROPERTY_ID(object_, property_id, pspec): pass

#
# GEnum/GFlags
#
G_ENUM_CLASS_TYPE = lambda class_: G_TYPE_FROM_CLASS(class_)
G_ENUM_CLASS_TYPE_NAME = lambda class_: g_type_name(G_ENUM_CLASS_TYPE(class_))
G_TYPE_IS_ENUM = lambda type_: gboolean(G_TYPE_FUNDAMENTAL(type_).value == G_TYPE_ENUM.value)
G_ENUM_CLASS = lambda class_: G_TYPE_CHECK_CLASS_CAST(class_, G_TYPE_ENUM, GEnumClass)
G_IS_ENUM_CLASS = lambda class_: G_TYPE_CHECK_CLASS_TYPE(class_, G_TYPE_ENUM)
G_TYPE_IS_FLAGS = lambda type_: gboolean(G_TYPE_FUNDAMENTAL(type_).value == G_TYPE_FLAGS.value)
G_IS_FLAGS_CLASS = lambda class_: G_TYPE_CHECK_CLASS_TYPE(class_, G_TYPE_FLAGS)
G_IS_FLAGS_CLASS = lambda class_: G_TYPE_CHECK_CLASS_TYPE(class_, G_TYPE_FLAGS)
G_FLAGS_CLASS_TYPE = lambda class_: G_TYPE_FROM_CLASS(class_)
G_FLAGS_CLASS_TYPE_NAME = lambda class_: g_type_name(G_FLAGS_CLASS_TYPE(class_))

#
# GBoxed
#
G_TYPE_HASH_TABLE = g_hash_table_get_type()
G_TYPE_DATE = g_date_get_type()
G_TYPE_GSTRING = g_gstring_get_type()
G_TYPE_STRV = g_strv_get_type()
G_TYPE_REGEX = g_regex_get_type()
G_TYPE_ARRAY = g_array_get_type()
G_TYPE_BYTE_ARRAY = g_byte_array_get_type()
G_TYPE_PTR_ARRAY = g_ptr_array_get_type()
G_TYPE_VARIANT_TYPE = g_variant_type_get_gtype()
G_TYPE_ERROR = g_error_get_type()
# G_TYPE_DATE_TIME = g_date_time_get_type()

#
# GValue
#
G_VALUE_HOLDS = lambda value, type_: G_TYPE_CHECK_VALUE_TYPE(value, type_)
G_VALUE_TYPE = lambda value: cast(value, POINTER(GValue)).g_type
G_VALUE_TYPE_NAME = lambda value: g_type_name(G_VALUE_TYPE(value))
G_TYPE_IS_VALUE = lambda type_: g_type_check_is_value_type(type_)
G_TYPE_IS_VALUE_ABSTRACT = lambda type_: g_type_test_flags(type_, G_TYPE_FLAG_VALUE_ABSTRACT)
G_IS_VALUE = lambda value: G_TYPE_CHECK_VALUE(value)
G_TYPE_VALUE = g_value_get_type()
G_TYPE_VALUE_ARRAY = g_value_array_get_type()

#
# GParamSpec/GValue
#
# hack: "GType * 100", 100 is a hack
g_param_spec_types = cast(pointer(libgobject.g_param_spec_types), POINTER(GType * 100)).contents

G_IS_PARAM_SPEC_BOOLEAN = lambda pspec: G_TYPE_CHECK_INSTANCE_TYPE(pspec, G_TYPE_PARAM_BOOLEAN)
G_PARAM_SPEC_BOOLEAN = lambda pspec: G_TYPE_CHECK_INSTANCE_CAST(pspec, G_TYPE_PARAM_BOOLEAN, GParamSpecBoolean)
G_VALUE_HOLDS_BOOLEAN = lambda value: G_TYPE_CHECK_VALUE_TYPE(value, G_TYPE_BOOLEAN)
G_TYPE_PARAM_BOOLEAN = g_param_spec_types[2]

G_IS_PARAM_SPEC_CHAR = lambda pspec: G_TYPE_CHECK_INSTANCE_TYPE(pspec, G_TYPE_PARAM_CHAR)
G_PARAM_SPEC_CHAR = lambda pspec: G_TYPE_CHECK_INSTANCE_CAST(pspec, G_TYPE_PARAM_CHAR, GParamSpecChar)
G_VALUE_HOLDS_CHAR = lambda value: G_TYPE_CHECK_VALUE_TYPE(value, G_TYPE_CHAR)
G_TYPE_PARAM_CHAR = g_param_spec_types[0]

G_IS_PARAM_SPEC_UCHAR = lambda pspec: G_TYPE_CHECK_INSTANCE_TYPE(pspec, G_TYPE_PARAM_UCHAR)
G_PARAM_SPEC_UCHAR = lambda pspec: G_TYPE_CHECK_INSTANCE_CAST(pspec, G_TYPE_PARAM_UCHAR, GParamSpecUChar)
G_VALUE_HOLDS_UCHAR = lambda value: G_TYPE_CHECK_VALUE_TYPE(value, G_TYPE_UCHAR)
G_TYPE_PARAM_UCHAR = g_param_spec_types[1]

G_IS_PARAM_SPEC_INT = lambda pspec: G_TYPE_CHECK_INSTANCE_TYPE(pspec, G_TYPE_PARAM_INT)
G_PARAM_SPEC_INT = lambda pspec: G_TYPE_CHECK_INSTANCE_CAST(pspec, G_TYPE_PARAM_INT, GParamSpecInt)
G_VALUE_HOLDS_INT = lambda value: G_TYPE_CHECK_VALUE_TYPE(value, G_TYPE_INT)
G_TYPE_PARAM_INT = g_param_spec_types[3]

G_IS_PARAM_SPEC_UINT = lambda pspec: G_TYPE_CHECK_INSTANCE_TYPE(pspec, G_TYPE_PARAM_UINT)
G_PARAM_SPEC_UINT = lambda pspec: G_TYPE_CHECK_INSTANCE_CAST(pspec, G_TYPE_PARAM_UINT, GParamSpecUInt)
G_VALUE_HOLDS_UINT = lambda value: G_TYPE_CHECK_VALUE_TYPE(value, G_TYPE_UINT)
G_TYPE_PARAM_UINT = g_param_spec_types[4]

G_IS_PARAM_SPEC_LONG = lambda pspec: G_TYPE_CHECK_INSTANCE_TYPE(pspec, G_TYPE_PARAM_LONG)
G_PARAM_SPEC_LONG = lambda pspec: G_TYPE_CHECK_INSTANCE_CAST(pspec, G_TYPE_PARAM_LONG, GParamSpecLong)
G_VALUE_HOLDS_LONG = lambda value: G_TYPE_CHECK_VALUE_TYPE(value, G_TYPE_LONG)
G_TYPE_PARAM_LONG = g_param_spec_types[5]

G_IS_PARAM_SPEC_ULONG = lambda pspec: G_TYPE_CHECK_INSTANCE_TYPE(pspec, G_TYPE_PARAM_ULONG)
G_PARAM_SPEC_ULONG = lambda pspec: G_TYPE_CHECK_INSTANCE_CAST(pspec, G_TYPE_PARAM_ULONG, GParamSpecULong)
G_VALUE_HOLDS_ULONG = lambda value: G_TYPE_CHECK_VALUE_TYPE(value, G_TYPE_ULONG)
G_TYPE_PARAM_ULONG = g_param_spec_types[6]

G_IS_PARAM_SPEC_INT64 = lambda pspec: G_TYPE_CHECK_INSTANCE_TYPE(pspec, G_TYPE_PARAM_INT64)
G_PARAM_SPEC_INT64 = lambda pspec: G_TYPE_CHECK_INSTANCE_CAST(pspec, G_TYPE_PARAM_INT64, GParamSpecInt64)
G_VALUE_HOLDS_INT64 = lambda value: G_TYPE_CHECK_VALUE_TYPE(value, G_TYPE_INT64)
G_TYPE_PARAM_INT64 = g_param_spec_types[7]

G_IS_PARAM_SPEC_UINT64 = lambda pspec: G_TYPE_CHECK_INSTANCE_TYPE(pspec, G_TYPE_PARAM_UINT64)
G_PARAM_SPEC_UINT64 = lambda pspec: G_TYPE_CHECK_INSTANCE_CAST(pspec, G_TYPE_PARAM_UINT64, GParamSpecUInt64)
G_VALUE_HOLDS_UINT64 = lambda value: G_TYPE_CHECK_VALUE_TYPE(value, G_TYPE_UINT64)
G_TYPE_PARAM_UINT64 = g_param_spec_types[8]

G_IS_PARAM_SPEC_FLOAT = lambda pspec: G_TYPE_CHECK_INSTANCE_TYPE(pspec, G_TYPE_PARAM_FLOAT)
G_PARAM_SPEC_FLOAT = lambda pspec: G_TYPE_CHECK_INSTANCE_CAST(pspec, G_TYPE_PARAM_FLOAT, GParamSpecFloat)
G_VALUE_HOLDS_FLOAT = lambda value: G_TYPE_CHECK_VALUE_TYPE(value, G_TYPE_FLOAT)
G_TYPE_PARAM_FLOAT = g_param_spec_types[12]

G_IS_PARAM_SPEC_DOUBLE = lambda pspec: G_TYPE_CHECK_INSTANCE_TYPE(pspec, G_TYPE_PARAM_DOUBLE)
G_PARAM_SPEC_DOUBLE = lambda pspec: G_TYPE_CHECK_INSTANCE_CAST(pspec, G_TYPE_PARAM_DOUBLE, GParamSpecDouble)
G_VALUE_HOLDS_DOUBLE = lambda value: G_TYPE_CHECK_VALUE_TYPE(value, G_TYPE_DOUBLE)
G_TYPE_PARAM_DOUBLE = g_param_spec_types[13]

G_IS_PARAM_SPEC_ENUM = lambda pspec: G_TYPE_CHECK_INSTANCE_TYPE(pspec, G_TYPE_PARAM_ENUM)
G_PARAM_SPEC_ENUM = lambda pspec: G_TYPE_CHECK_INSTANCE_CAST(pspec, G_TYPE_PARAM_ENUM, GParamSpecEnum)
G_VALUE_HOLDS_ENUM = lambda value: G_TYPE_CHECK_VALUE_TYPE(value, G_TYPE_ENUM)
G_TYPE_PARAM_ENUM = g_param_spec_types[10]

G_IS_PARAM_SPEC_FLAGS = lambda pspec: G_TYPE_CHECK_INSTANCE_TYPE(pspec, G_TYPE_PARAM_FLAGS)
G_PARAM_SPEC_FLAGS = lambda pspec: G_TYPE_CHECK_INSTANCE_CAST(pspec, G_TYPE_PARAM_FLAGS, GParamSpecFlags)
G_VALUE_HOLDS_FLAGS = lambda value: G_TYPE_CHECK_VALUE_TYPE(value, G_TYPE_FLAGS)
G_TYPE_PARAM_FLAGS = g_param_spec_types[11]

G_IS_PARAM_SPEC_STRING = lambda pspec: G_TYPE_CHECK_INSTANCE_TYPE(pspec, G_TYPE_PARAM_STRING)
G_PARAM_SPEC_STRING = lambda pspec: G_TYPE_CHECK_INSTANCE_CAST(pspec, G_TYPE_PARAM_STRING, GParamSpecString)
G_VALUE_HOLDS_STRING = lambda value: G_TYPE_CHECK_VALUE_TYPE(value, G_TYPE_STRING)
G_TYPE_PARAM_STRING = g_param_spec_types[14]

G_IS_PARAM_SPEC_PARAM = lambda pspec: G_TYPE_CHECK_INSTANCE_TYPE(pspec, G_TYPE_PARAM_PARAM)
G_PARAM_SPEC_PARAM= lambda pspec: G_TYPE_CHECK_INSTANCE_CAST(pspec, G_TYPE_PARAM_PARAM, GParamSpecParam)
G_VALUE_HOLDS_PARAM= lambda value: G_TYPE_CHECK_VALUE_TYPE(value, G_TYPE_PARAM)
G_TYPE_PARAM_PARAM = g_param_spec_types[15]

G_IS_PARAM_SPEC_BOXED = lambda pspec: G_TYPE_CHECK_INSTANCE_TYPE(pspec, G_TYPE_PARAM_BOXED)
G_PARAM_SPEC_BOXED= lambda pspec: G_TYPE_CHECK_INSTANCE_CAST(pspec, G_TYPE_PARAM_BOXED, GParamSpecBoxed)
G_VALUE_HOLDS_BOXED= lambda value: G_TYPE_CHECK_VALUE_TYPE(value, G_TYPE_BOXED)
G_TYPE_PARAM_BOXED = g_param_spec_types[16]

G_IS_PARAM_SPEC_POINTER = lambda pspec: G_TYPE_CHECK_INSTANCE_TYPE(pspec, G_TYPE_PARAM_POINTER)
G_PARAM_SPEC_POINTER= lambda pspec: G_TYPE_CHECK_INSTANCE_CAST(pspec, G_TYPE_PARAM_POINTER, GParamSpecPointer)
G_VALUE_HOLDS_POINTER= lambda value: G_TYPE_CHECK_VALUE_TYPE(value, G_TYPE_POINTER)
G_TYPE_PARAM_POINTER = g_param_spec_types[17]

G_IS_PARAM_SPEC_OBJECT = lambda pspec: G_TYPE_CHECK_INSTANCE_TYPE(pspec, G_TYPE_PARAM_OBJECT)
G_PARAM_SPEC_OBJECT= lambda pspec: G_TYPE_CHECK_INSTANCE_CAST(pspec, G_TYPE_PARAM_OBJECT, GParamSpecObject)
G_VALUE_HOLDS_OBJECT= lambda value: G_TYPE_CHECK_VALUE_TYPE(value, G_TYPE_OBJECT)
G_TYPE_PARAM_OBJECT = g_param_spec_types[19]

G_IS_PARAM_SPEC_UNICHAR = lambda pspec: G_TYPE_CHECK_INSTANCE_TYPE(pspec, G_TYPE_PARAM_UNICHAR)
G_PARAM_SPEC_UNICHAR= lambda pspec: G_TYPE_CHECK_INSTANCE_CAST(pspec, G_TYPE_PARAM_UNICHAR, GParamSpecUnichar)
G_TYPE_PARAM_UNICHAR = g_param_spec_types[9]

G_IS_PARAM_SPEC_VALUE_ARRAY = lambda pspec: G_TYPE_CHECK_INSTANCE_TYPE(pspec, G_TYPE_PARAM_VALUE_ARRAY)
G_PARAM_SPEC_VALUE_ARRAY= lambda pspec: G_TYPE_CHECK_INSTANCE_CAST(pspec, G_TYPE_PARAM_VALUE_ARRAY, GParamSpecValueArray)
G_TYPE_PARAM_VALUE_ARRAY = g_param_spec_types[18]

G_IS_PARAM_SPEC_OVERRIDE = lambda pspec: G_TYPE_CHECK_INSTANCE_TYPE(pspec, G_TYPE_PARAM_OVERRIDE)
G_PARAM_SPEC_OVERRIDE= lambda pspec: G_TYPE_CHECK_INSTANCE_CAST(pspec, G_TYPE_PARAM_OVERRIDE, GParamSpecOverride)
G_TYPE_PARAM_OVERRIDE = g_param_spec_types[20]

G_IS_PARAM_SPEC_GTYPE = lambda pspec: G_TYPE_CHECK_INSTANCE_TYPE(pspec, G_TYPE_PARAM_GTYPE)
G_PARAM_SPEC_GTYPE= lambda pspec: G_TYPE_CHECK_INSTANCE_CAST(pspec, G_TYPE_PARAM_GTYPE, GParamSpecGType)
G_VALUE_HOLDS_GTYPE= lambda value: G_TYPE_CHECK_VALUE_TYPE(value, G_TYPE_GTYPE)
G_TYPE_PARAM_GTYPE = g_param_spec_types[21]

G_IS_PARAM_SPEC_VARIANT = lambda pspec: G_TYPE_CHECK_INSTANCE_TYPE(pspec, G_TYPE_PARAM_VARIANT)
G_PARAM_SPEC_VARIANT= lambda pspec: G_TYPE_CHECK_INSTANCE_CAST(pspec, G_TYPE_PARAM_VARIANT, GParamSpecVariant)
G_VALUE_HOLDS_VARIANT= lambda value: G_TYPE_CHECK_VALUE_TYPE(value, G_TYPE_VARIANT)
G_TYPE_PARAM_VARIANT = g_param_spec_types[22]

#
# GParamSpec
#
G_TYPE_IS_PARAM = lambda type_: gboolean(G_TYPE_FUNDAMENTAL(type_).value == G_TYPE_PARAM.value)
G_PARAM_SPEC = lambda pspec: G_TYPE_CHECK_INSTANCE_CAST(pspec, G_TYPE_PARAM, GParamSpec)
G_IS_PARAM_SPEC = lambda pspec: G_TYPE_CHECK_INSTANCE_TYPE(pspec, G_TYPE_PARAM)
G_PARAM_SPEC_CLASS = lambda pclass: G_TYPE_CHECK_CLASS_CAST(pclass, G_TYPE_PARAM, GParamSpecClass)
G_IS_PARAM_SPEC_CLASS = lambda pclass: G_TYPE_CHECK_CLASS_TYPE(pclass, G_TYPE_PARAM)
G_PARAM_SPEC_GET_CLASS = lambda pspec: G_TYPE_INSTANCE_GET_CLASS(pspec, G_TYPE_PARAM, GParamSpecClass)
G_PARAM_SPEC_TYPE = lambda pspec: G_TYPE_FROM_INSTANCE(pspec)
G_PARAM_SPEC_TYPE_NAME = lambda pspec: g_type_name(G_PARAM_SPEC_TYPE(pspec))
G_PARAM_SPEC_VALUE_TYPE = lambda pspec: G_PARAM_SPEC(pspec).value_type

G_PARAM_READWRITE = gint(G_PARAM_READABLE.value | G_PARAM_WRITABLE.value)
G_PARAM_STATIC_STRINGS = gint(G_PARAM_STATIC_NAME.value | G_PARAM_STATIC_NICK.value | G_PARAM_STATIC_BLURB.value)
G_PARAM_MASK = gint(0x000000ff)
G_PARAM_USER_SHIFT = gint(8)

#
# GTypeCValue
#
def G_VALUE_COLLECT_INIT(value, _value_type, var_args, flags, __error): pass
def G_VALUE_COLLECT(value, var_args, flags, __error): pass
def G_VALUE_LCOPY(value, var_args, flags, __error): pass
G_VALUE_COLLECT_FORMAT_MAX_LENGTH = gint(8)

#
# GSignal
#
G_SIGNAL_TYPE_STATIC_SCOPE = G_TYPE_FLAG_RESERVED_ID_BIT
G_SIGNAL_MATCH_MASK = gint(0x3f)
G_SIGNAL_FLAGS_MASK = gint(0x7f)

def g_signal_connect(instance, detailed_signal, c_handler, data):
	return g_signal_connect_data(
		instance,
		detailed_signal,
		c_handler,
		data,
		None,
		GConnectFlags(0)
	)
	
def g_signal_connect_after(instance, detailed_signal, c_handler, data):
	return g_signal_connect_data(
		instance,
		detailed_signal,
		c_handler,
		data,
		None,
		G_CONNECT_AFTER
	)
	
def g_signal_connect_swapped(instance, detailed_signal, c_handler, data):
	return g_signal_connect_data(
		instance,
		detailed_signal,
		c_handler,
		data,
		None,
		G_CONNECT_SWAPPED
	)

def g_signal_handlers_block_by_func(instance, func, data):
	return g_signal_handlers_block_matched(
		instance,
		GSignalMatchType(G_SIGNAL_MATCH_FUNC.value | G_SIGNAL_MATCH_DATA.value),
		gint(0),
		gint(0),
		None,
		func,
		data
	)

def g_signal_handlers_unblock_by_func(instance, func, data):
	return g_signal_handlers_unblock_matched(
		instance,
		GSignalMatchType(G_SIGNAL_MATCH_FUNC.value | G_SIGNAL_MATCH_DATA.value),
		gint(0),
		gint(0),
		None,
		func,
		data
	)

def g_signal_handlers_disconnect_by_func(instance, func, data):
	return g_signal_handlers_disconnect_matched(
		instance,
		GSignalMatchType(G_SIGNAL_MATCH_FUNC.value | G_SIGNAL_MATCH_DATA.value),
		gint(0),
		gint(0),
		None,
		func,
		data
	)

#
# GClosure
#
G_CLOSURE_NEEDS_MARSHAL = lambda closure: gboolean(not bool((cast(closure, POINTER(GClosure))).marshal))
def G_CLOSURE_N_NOTIFIERS(cl): pass
G_CCLOSURE_SWAP_DATA = lambda cclosure: (cast(cclosure, POINTER(GClosure))).derivative_flag
G_CALLBACK = lambda f: cast(f, GCallback)
G_TYPE_CLOSURE = g_closure_get_type()
# G_TYPE_IO_CHANNEL = g_io_channel_get_type()
# G_TYPE_IO_CONDITION = g_io_condition_get_type()

########################################################################

#
# Closure
#
#~ class Closure(Structure):
	#~ _fields_ = [
		#~ ('closure', GClosure),
		#~ ('data', gpointer),
	#~ ]

#~ _closure_ids = {}
#~ 
#~ class Closure(Structure):
	#~ _fields_ = [
		#~ ('closure', GClosure),
		#~ ('id', guint),
	#~ ]
#~ 
#~ def closure_new(pyobj):
	#~ global _closure_ids
	#~ closure_id = len(_closure_ids)
	#~ _closure_id = guint(closure_id)
	#~ _closure_ids[closure_id] = pyobj
	#~ 
	#~ gclosure_p = g_closure_new_simple(guint(sizeof(Closure)), gpointer(0))
	#~ print(bool(gclosure_p))
	#~ #gclosure_p = pointer(GClosure())
	#~ gclosure_p.contents.inmarshal_isinvalid = guint(0)
	#~ g_closure_ref(gclosure_p)
	#~ closure_p = cast(gclosure_p, POINTER(Closure))
	#~ closure_p.contents.id = _closure_id
	#~ return closure_p
#~ 
#~ def closure_invoke(closure_p, *args):
	#~ global _closure_ids
	#~ _closure_id = closure_p.contents.id
	#~ pyobj = _closure_ids[_closure_id.value]
	#~ ret = pyobj(*args)
	#~ return ret
#~ 
#~ def closure_del(closure_p):
	#~ global _closure_ids
	#~ _closure_id = closure_p.contents.id
	#~ del _closure_ids[_closure_id.value]
	#~ g_closure_unref(gclosure_p)

#~ _pyclosure_ids = {}
#~ 
#~ class PyClosure(Structure):
	#~ _fields_ = [
		#~ ('closure', GClosure),
		#~ ('id', guint),
	#~ ]
#~ 
#~ def pyclosure_invalidate(_data, _gclosure):
	#~ global _pyclosure_ids
	#~ _pyclosure = cast(_gclosure, POINTER(PyClosure))
	#~ _pyclosure_id = _pyclosure.contents.id
	#~ pyclosure_id = _pyclosure_id.value
	#~ del _pyclosure_ids[pyclosure_id]
#~ 
#~ def pyclosure_finalize(_data, _gclosure):
	#~ g_closure_unref(_gclosure)
#~ 
#~ def pyclosure_new(_data, pyobj):
	#~ global _pyclosure_ids
	#~ pyclosure_id = len(_pyclosure_ids)
	#~ _pyclosure_id = guint(pyclosure_id)
	#~ _pyclosure_ids[pyclosure_id] = pyobj
	#~ 
	#~ _gclosure = g_closure_new_simple(sizeof(PyClosure), _data)
	#~ _pyclosure = cast(_gclosure, POINTER(PyClosure))
	#~ _pyclosure.contents.id = _pyclosure_id
	#~ 
	#~ g_closure_add_finalize_notifier(_gclosure, gpointer(None), (CFUNCTYPE(None, gpointer, POINTER(GClosure)))(pyclosure_finalize))
	#~ g_closure_add_invalidate_notifier(_gclosure, gpointer(None), (CFUNCTYPE(None, gpointer, POINTER(GClosure)))(pyclosure_invalidate))
	#~ 
	#~ return _gclosure
#~ 
#~ def pyclosure_invoke(_gclosure, args):
	#~ _pyclosure = cast(_gclosure, POINTER(PyClosure))
	#~ _pyclosure_id = _pyclosure.contents.id
	#~ pyclosure_id = _pyclosure_id.value
	#~ pyobj = _pyclosure_ids[pyclosure_id]
	#~ _return = pyobj(*args)
	#~ return _return
