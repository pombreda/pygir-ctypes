from ._glib import *

libgobject = CDLL(find_library('gobject-2.0'))

#~ # GType

#~ class GTypeCValue(Union): pass

#~ 

#~ 
#~ # GObject

#~ 
#~ # GParam
#~ class GParamSpec(Structure): pass
#~ class GParamSpecClass(Structure): pass
#~ 
#~ GParamFlags = gint
#~ G_PARAM_READABLE = GParamFlags(1 << 0)
#~ G_PARAM_WRITABLE = GParamFlags(1 << 1)
#~ G_PARAM_CONSTRUCT = GParamFlags(1 << 2)
#~ G_PARAM_CONSTRUCT_ONLY = GParamFlags(1 << 3)
#~ G_PARAM_LAX_VALIDATION = GParamFlags(1 << 4)
#~ G_PARAM_STATIC_NAME = GParamFlags(1 << 5)
#~ G_PARAM_PRIVATE = G_PARAM_STATIC_NAME
#~ G_PARAM_STATIC_NICK = GParamFlags(1 << 6)
#~ G_PARAM_STATIC_BLURB = GParamFlags(1 << 7)
#~ G_PARAM_DEPRECATED = GParamFlags(1 << 31)
#~ 
#~ # GCClosure
#~ class GClosure(Structure): pass
#~ class GCClosure(Structure): pass
#~ 
#~ GClosureMarshal = CFUNCTYPE(
	#~ POINTER(GClosure),
	#~ POINTER(GValue),
	#~ guint,
	#~ POINTER(GValue),
	#~ gpointer,
	#~ gpointer,
#~ )
#~ 
#~ # GSignal
#~ class GSignalInvocationHint(Structure): pass
#~ GSignalCMarshaller = GClosureMarshal
#~ 
#~ GSignalEmissionHook = CFUNCTYPE(
	#~ POINTER(GSignalInvocationHint),
	#~ guint,
	#~ POINTER(GValue),
	#~ gpointer,
#~ )
#~ 
#~ GSignalFlags = gint
#~ G_SIGNAL_RUN_FIRST = GSignalFlags(1 << 0)
#~ G_SIGNAL_RUN_LAST = GSignalFlags(1 << 1)
#~ G_SIGNAL_RUN_CLEANUP = GSignalFlags(1 << 2)
#~ G_SIGNAL_NO_RECURSE = GSignalFlags(1 << 3)
#~ G_SIGNAL_DETAILED = GSignalFlags(1 << 4)
#~ G_SIGNAL_ACTION = GSignalFlags(1 << 5)
#~ G_SIGNAL_NO_HOOKS = GSignalFlags(1 << 6)
#~ 
#~ GSignalMatchType = gint
#~ G_SIGNAL_MATCH_ID = GSignalMatchType(1 << 0)
#~ G_SIGNAL_MATCH_DETAIL = GSignalMatchType(1 << 1)
#~ G_SIGNAL_MATCH_CLOSURE = GSignalMatchType(1 << 2)
#~ G_SIGNAL_MATCH_FUNC = GSignalMatchType(1 << 3)
#~ G_SIGNAL_MATCH_DATA = GSignalMatchType(1 << 4)
#~ G_SIGNAL_MATCH_UNBLOCKED = GSignalMatchType(1 << 5)
#~ 
#~ class GSignalQuery(Structure): pass

#~ 
#~ #
#~ # GType/GValue
#~ #

#~ G_TYPE_GTYPE = g_gtype_get_type()
#~ G_TYPE_VALUE = g_value_get_type()
#~ G_TYPE_VALUE_ARRAY = g_value_array_get_type()












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

#
# GValue
#
#~ GValue *            g_value_init                        (GValue *value,
                                                         #~ GType g_type);
#~ void                g_value_copy                        (const GValue *src_value,
                                                         #~ GValue *dest_value);
#~ GValue *            g_value_reset                       (GValue *value);
#~ void                g_value_unset                       (GValue *value);
#~ void                g_value_set_instance                (GValue *value,
                                                         #~ gpointer instance);
#~ gboolean            g_value_fits_pointer                (const GValue *value);
#~ gpointer            g_value_peek_pointer                (const GValue *value);
#~ gboolean            g_value_type_compatible             (GType src_type,
                                                         #~ GType dest_type);
#~ gboolean            g_value_type_transformable          (GType src_type,
                                                         #~ GType dest_type);
#~ gboolean            g_value_transform                   (const GValue *src_value,
                                                         #~ GValue *dest_value);
#~ void                (*GValueTransform)                  (const GValue *src_value,
                                                         #~ GValue *dest_value);
#~ void                g_value_register_transform_func     (GType src_type,
                                                         #~ GType dest_type,
                                                         #~ GValueTransform transform_func);
#~ gchar *                 g_strdup_value_contents         (const GValue *value);

#
# GType
#
G_TYPE_FUNDAMENTAL = lambda type_: g_type_fundamental(type_)
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
G_TYPE_DATE_TIME = g_date_time_get_type()

#
# GValue
#
#~ #define             G_VALUE_HOLDS                       (value,
                                                         #~ type)
#~ #define             G_VALUE_TYPE                        (value)
#~ #define             G_VALUE_TYPE_NAME                   (value)
#~ #define             G_TYPE_IS_VALUE                     (type)
#~ #define             G_TYPE_IS_VALUE_ABSTRACT            (type)
#~ #define             G_IS_VALUE                          (value)

#~ #define             G_TYPE_VALUE
#~ #define             G_TYPE_VALUE_ARRAY
