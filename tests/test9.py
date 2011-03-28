#
# A
#
clsname = 'A'
clsbases = (object,)
clsdict = {}

A = type(clsname, clsbases, clsdict)

@classmethod
def new(cls, *args, **kwargs):
	print('A.new', cls, args, kwargs)
	self = super(A, cls).__new__(cls, *args, **kwargs)
	return self

setattr(A, 'new', new)

def __new__(cls, *args, **kwargs):
	print('A.__new__', cls, args, kwargs)
	self = super(A, cls).__new__(cls, *args, **kwargs)
	return self

setattr(A, '__new__', __new__)

def __init__(self, *args, **kwargs):
	print('A.__init__', self, args, kwargs)

setattr(A, '__init__', __init__)

#
# B
#
clsname = 'B'
clsbases = (A,)
clsdict = {}

B = type(clsname, clsbases, clsdict)

@classmethod
def new(cls, *args, **kwargs):
	print('B.new', cls, args, kwargs)
	self = super(B, cls).__new__(cls, *args, **kwargs)
	return self

setattr(B, 'new', new)

def __new__(cls, *args, **kwargs):
	print('B.__new__', cls, args, kwargs)
	self = super(B, cls).__new__(cls, *args, **kwargs)
	return self

setattr(B, '__new__', __new__)

def __init__(self, *args, **kwargs):
	print('B.__init__', self, args, kwargs)
	A.__init__(self, *args, **kwargs)

setattr(B, '__init__', __init__)

if __name__ == '__main__':
	b = B()
	print(b)
	print(dir(b))
