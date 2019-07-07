from setuptools import setup

setup(
	name='pystore',
	version='0.2',
	py_modules=['pystore'],
	install_requires=[
		'Click',
	],
	entry_points='''
		[console_scripts]
		pystore=pystore:cli
	''',
)
