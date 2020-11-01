from ...plugin import Plugin
from ..data import Data

class RRPlugin(Plugin):
	paths = [ 'zc.dns.rr' ]

	def getTypeMap(self):
		typemap = Data()
		
		for typename, plugin in self.plugins.items():
			if 'type' in plugin['args']:
				typemap[typename] = plugin['args']['type']

		return typemap

	def typeByName(self, name):
		number = None

		for typename, plugin in self.plugins.items():
			if typename == name and 'type' in plugin['args']:
				number = plugin['args']['type']
				break

		return number

	def byType(self, type, **config):
		instance = None

		for name, plugin in self.plugins.items():
			if 'type' in plugin['args'] and plugin['args']['type'] == type:
				instance = self.instance(name, config)
				break

		return instance
