
class A(object):
	@classmethod
	def new(cls, *args, **kwargs):
		print('A.new', cls, args, kwargs)
		self = super(A, cls).__new__(cls, *args, **kwargs)
		return self
	
	def __new__(cls, *args, **kwargs):
		print('A.__new__', cls, args, kwargs)
		self = super(A, cls).__new__(cls, *args, **kwargs)
		return self
	
	def __init__(self, *args, **kwargs):
		print('A.__init__', self, args, kwargs)

class B(A):
	@classmethod
	def new(cls, *args, **kwargs):
		print('B.new', cls, args, kwargs)
		self = super(B, cls).new(cls, *args, **kwargs)
		B.__init__(self, *args, **kwargs)
		return self
	
	def __new__(cls, *args, **kwargs):
		print('B.__new__', cls, args, kwargs)
		self = super(B, cls).new(*args, **kwargs)
		return self
	
	def __init__(self, *args, **kwargs):
		print('B.__init__', self, args, kwargs)
		A.__init__(self, *args, **kwargs)

b = B.new()
print(b)
