from struct import unpack, pack

from .rdata import RData
from ..util import sub
from .rrplugin import RRPlugin

@RRPlugin.register(type=28)
class AAAA(RData):
	def decode(self):
		self.raw = sub(self.raw, self.offset, 16)
		self.address = [ int(v) for v in unpack('!BBBBBBBBBBBBBBBB', self.raw) ]
		return self

	def encode(self):
		self.raw = pack('!BBBBBBBBBBBBBBBB', *self.address)
		return self
