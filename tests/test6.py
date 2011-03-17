import types

class F(object):
	def __init__(self, func):
		self._func = func
	
	def __call__(self, *args, **kwargs):
		return self._func(*args, **kwargs)

class G(object):
	def __init__(self, func):
		self._func = func
	
	def __get__(self, obj, type_=None):
		# print('*', self, obj, type_)
		if isinstance(obj, type_):
			return lambda *args, **kwargs: self(obj, *args, **kwargs)
		else:
			return self
	
	def __call__(self, *args, **kwargs):
		return self._func(*args, **kwargs)

class A(object):
	m1 = F(lambda *args, **kwargs: (args, kwargs))
	m2 = G(lambda *args, **kwargs: (args, kwargs))

if __name__ == '__main__':
	a = A()

	print(A.m1)
	print(a.m1)
	print(a.m1(10, 20, c=30, d=40))

	print(A.m2)
	print(a.m2)
	print(a.m2(10, 20, c=30, d=40))
