
class instancemethod(object):
	def __init__(self, func):
		self._func = func
		
	def __get__(self, obj, type_=None):
		return lambda *args, **kwargs: self._func(obj, *args, **kwargs)

class Func(object):
	def __init__(self):
		pass
	
	def __call__(self, *args, **kwargs):
		return self, args, kwargs

class A(object):
	def __init__(self):
		pass
	
	f1 = classmethod(Func())
	f2 = instancemethod(Func())

a = A()
print(a.f1(10, 20))
print(a.f2(10, 20))
print(A.f1(10, 20))
