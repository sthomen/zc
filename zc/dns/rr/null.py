from .rdata import RData
from ..util import sub
from .rrplugin import RRPlugin

@RRPlugin.register(name='null', type=10)
class NULL(RData):
	def decode(self):
		self.raw = sub(self.raw, self.offset, self.length)
		return self
