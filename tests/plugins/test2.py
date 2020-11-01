from .mockplugin import MockPlugin

@MockPlugin.register(foo="bar")
class Test2(object):
	def __init__(self, foo = None):
		self.foo = foo
