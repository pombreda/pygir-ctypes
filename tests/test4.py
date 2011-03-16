import sys
import types

class Test4(types.ModuleType):
	def func1(self, *args, **kwargs):
		return(self, args, kwargs)

sys.modules['Test4'] = Test4('Test4', 'This is Test4') 

import Test4
print(Test4)
print(Test4.func1())
