from struct import unpack

from .rdata import RData
from ..util import sub

class A(RData):
	def decode(self):
		self.raw = sub(self.raw, self.offset, 4)
		self.address = [ int(v) for v in unpack('!BBBB', self.raw) ]
		return self

	def encode(self):
		self.raw = pack('!BBBB', *self.address)
