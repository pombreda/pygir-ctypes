import sys
sys.path.append('..')

from struct import *
from gir._girepository import *

a = GArray('ABABABABCDCDCDCDEFEFEFEFGHGHGHGH', 32)
print(unpack('LLLL', 'ABABABABCDCDCDCDEFEFEFEFGHGHGHGH'))

bp = GIArgument * (a.len.value // sizeof(GIArgument))
ba = bp()
memmove(ba, a.data, 32)
print(ba[0].v_uint64.value,)
print(ba[1].v_uint64.value,)
print(ba[2].v_uint64.value,)
print(ba[3].v_uint64.value,)
