from struct import unpack

from .rdata import RData
from ..util import sub, decode_labels

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
