from struct import unpack, pack

from .rdata import RData
from ..util import sub, decode_labels, encode_labels
from .rrplugin import RRPlugin

@RRPlugin.register(type=33)
class SRV(RData):
	def decode(self):
		header = sub(self.raw, self.offset, 6)
		offset = self.offset

		if len(header) == 6:
			self.priority, self.weight, self.port = unpack('!HHH', header)
			offset += 6

			offset, self.target = decode_labels(self.raw, offset)

		self.raw = sub(self.raw, self.offset, offset - self.offset)

		return self

	def encode(self):
		self.raw = bytes()
		self.raw += pack('!HHH', self.priority, self.weight, self.port)
		self.raw += encode_labels(self.target)

		return self
