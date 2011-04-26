from ._common import *

# glib - C library
libglib = CDLL(find_library('glib-2.0'))

class gboolean(c_int): pass
class gint8(c_byte): pass
class guint8(c_ubyte): pass
class gint16(c_short): pass
class guint16(c_ushort): pass
class gint32(c_int): pass
class guint32(c_uint): pass
class gint64(c_longlong): pass
class guint64(c_ulonglong): pass
class gfloat(c_float): pass
class gdouble(c_double): pass
class gshort(c_short): pass
class gushort(c_ushort): pass
class gint(c_int): pass
class guint(c_uint): pass
class glong(c_long): pass
class gulong(c_ulong): pass
class gssize(c_long): pass
class gsize(c_ulong): pass
class gchar(c_char): pass
class gchar_p(c_char_p): pass
class guchar(c_char): pass
class guchar_p(c_char_p): pass
class gunichar(c_char): pass
class gunichar_p(c_char_p): pass
class gpointer(c_void_p): pass
class gconstpointer(c_void_p): pass

class GQuark(guint32): pass
class GError(Structure): 
	_fields_ = [
		('domain', GQuark),
		('code', gint),
		('message', gchar_p),
	]

class GList(Structure): pass
GList._fields_ = [
	('data', gpointer),
	('next', POINTER(GList)),
	('prev', POINTER(GList)),
]

class GSList(Structure): pass
GSList._fields_ = [
	('data', gpointer),
	('next', POINTER(GSList)),
]

class GHashTable(Structure): pass
class GOptionGroup(Structure): pass
class GMappedFile(Structure): pass
class GData(GQuark): pass
class GVariant(Structure): pass
class GVariantType(Structure): pass
class GSource(Structure): pass

class GArray(Structure):
	_fields_ = [
		('data', gchar_p),
		('len', guint),
	]

GDestroyNotify = CFUNCTYPE(None, gpointer)
GCompareFunc = CFUNCTYPE(gint, gconstpointer, gconstpointer)
GCompareDataFunc = CFUNCTYPE(gint, gconstpointer, gconstpointer, gpointer)

g_array_new = ctypes_get_func(
	libglib,
	'g_array_new',
	POINTER(GArray),
	gboolean,
	gboolean,
	guint,
)

g_array_sized_new = ctypes_get_func(
	libglib,
	'g_array_sized_new',
	POINTER(GArray),
	gboolean,
	gboolean,
	guint,
	guint,
)

g_array_ref = ctypes_get_func(
	libglib,
	'g_array_ref',
	POINTER(GArray),
	POINTER(GArray),
)

g_array_unref = ctypes_get_func(
	libglib,
	'g_array_unref',
	None,
	POINTER(GArray),
)

g_array_get_element_size = ctypes_get_func(
	libglib,
	'g_array_get_element_size',
	guint,
	POINTER(GArray),
)

g_array_insert_vals = ctypes_get_func(
	libglib,
	'g_array_insert_vals',
	POINTER(GArray),
	POINTER(GArray),
	guint,
	gconstpointer,
	guint,
)

def g_array_elt_len(a, i):
	# ((a)->elt_size * (i))
	return guint(g_array_get_element_size(a).value * i.value)

def g_array_index(a, t, i):
	# return ((t*)(void *)(a)->data)[i]
	al = g_array_elt_len(a, a.contents.len).value
	bl = al // sizeof(t)
	bt = (t * bl)
	ba = bt()
	memmove(ba, a.contents.data, al)
	return ba[i.value]

def g_array_insert_val(a, i, v):
	v_ = cast(pointer(v), gconstpointer)
	return g_array_insert_vals(a, i, v_, guint(1))

g_malloc0 = ctypes_get_func(
	libglib,
	'g_malloc0',
	gpointer,
	gsize,
)

def g_new0(struct_type, n_structs):
	return _G_NEW(struct_type, n_structs, g_malloc0)

def _G_NEW(struct_type, n_structs, func):
	# ((struct_type *) func ((n_structs), sizeof (struct_type)))
	res = func(n_structs * sizeof(struct_type))
	bt = (struct_type * n_structs)
	ba = bt()
	memmove(ba, res, n_structs * sizeof(struct_type))
	return ba
