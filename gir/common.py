
# instancemethod
class instancemethod(object):
	def __init__(self, func):
		self._func = func
		
	def __get__(self, obj, type_=None):
		return lambda *args, **kwargs: self._func(obj, *args, **kwargs)
