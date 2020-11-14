from setuptools import setup, find_packages

setup(
	name = 'zc',
	version = '1.0',

	packages = find_packages(),

	author = 'Staffan Thomen',
	author_email = 'staffan@thomen.fi',

	description = ('Simple mDNS interface library'),

	long_description = 'file:README.md',

	keywords = 'mDNS library',

	url = 'https://mercurial.shangtai.net/zc',

	license = 'BSD',

	classifiers = [
		'Development Status :: 4 - Beta',
		'Programming Languge :: Python :: 3'
	]
)
