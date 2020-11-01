from .mockplugin import MockPlugin

@MockPlugin.register
class Test1(object):
	pass
