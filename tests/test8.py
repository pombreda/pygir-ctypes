
class A(object):
	@classmethod
	def new(cls, *args, **kwargs):
		return cls(_self=None, *args, **kwargs)
	
	def __new__(cls, *args, **kwargs):
		self = super(A, cls).__new__(cls, *args, **kwargs)
		return self
	
	def __init__(self, *args, **kwargs):
		pass

class B(A):
	def __new__(cls, *args, **kwargs):
		self = super(B, cls).__new__(cls, *args, **kwargs)
		B.__init__(self, *args, **kwargs)
		return self
	
	def __init__(self, *args, **kwargs):
		A.__init__(self, *args, **kwargs)

b = B()
print(b)

b = B.new()
print(b)
