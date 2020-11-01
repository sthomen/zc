from .rdata import RData
from ..util import sub, decode_labels, encode_labels
from .rrplugin import RRPlugin

@RRPlugin.register(type=12)
class PTR(RData):
	def decode(self):
		offset, self.target = decode_labels(self.raw, self.offset)
		self.raw = sub(self.raw, self.offset, offset - self.offset)
		return self

	def encode(self):
		self.raw = bytes()
		self.raw += encode_labels(self.target)
		return self
