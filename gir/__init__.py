try:
	exec('from .girepository import *', globals(), locals())
except SyntaxError:
	from girepository import *
except ImportError:
	from girepository import *
