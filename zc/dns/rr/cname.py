from .ptr import PTR
from .rrplugin import RRPlugin

@RRPlugin.register(name='cname', type=5)
class CNAME(PTR):
	pass
