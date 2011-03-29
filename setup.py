from distutils.core import setup

setup(
	name='pygir-ctypes',
	version='0.1.0',
	description='Python GObject Introspection Repository',
	long_description='Pure Python GObject Introspection Repository (GIR) wrapper using ctypes',
	author='Marko Tasic',
	author_email='mtasic85@gmail.com',
	url='http://code.google.com/p/pygir-ctypes/',
	packages=['gir'],
	license='New BSD License',
	platforms=['Any'],
	data_files=[('', ['LICENSE'])],
)
