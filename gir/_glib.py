from ._common import *

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
class gchar(c_char): pass		# represents "[const] gchar"
class gchar_p(c_char_p): pass	# represents "[const] gchar*"
class gpointer(c_void_p): pass

class GQuark(guint32): pass
class GError(Structure): 
	_fields_ = [
		('domain', GQuark),
		('code', gint),
		('message', gchar_p),
	]
class GList(Structure): pass
class GSList(Structure): pass
class GHashTable(Structure): pass
class GOptionGroup(Structure): pass
class GMappedFile(Structure): pass
class GData(GQuark): pass
