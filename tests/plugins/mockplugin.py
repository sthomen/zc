from zc.plugin import Plugin

class MockPlugin(Plugin):
	paths = [ 'tests.plugins' ]

	def byFoo(self, foo):
		instance = None

		for name, plugin in self.plugins.items():
			if 'foo' in plugin['args'] and plugin['args']['foo'] == foo:
				instance = self.instance(name)
				break

		return instance
