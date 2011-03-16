
class F(object):
	def __init__(self, func):
		self._func = func
	
	def __call__(self, *args, **kwargs):
		return self._func(*args, **kwargs)

class G(object):
	def __init__(self, func):
		self._func = func
	
	def __call__(self, obj, *args, **kwargs):
		return self._func(obj, *args, **kwargs)

class A(object):
	m1 = lambda self, *args, **kwargs: (F(lambda *args_, **kwargs_: (args_, kwargs_))(self, *args, **kwargs))
	m2 = G(lambda self, *args, **kwargs: (self, args, kwargs))

a = A()
print(a.m1(10, 20, c=30, d=40))
print(a.m2(10, 20, c=30, d=40))
