exec('from ._common import *', globals(), locals())

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

def g_array_index(a, t, i):
	# return ((t*)(void *)(a)->data)[i]
	ba = (t * (a.contents.len.value // sizeof(t)))()
	memmove(ba, a.contents.data, a.contents.len.value)
	return ba[i.value]
