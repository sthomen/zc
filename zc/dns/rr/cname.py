from .ptr import PTR
from .rrplugin import RRPlugin

@RRPlugin.register(type=5)
class CNAME(PTR):
	pass
