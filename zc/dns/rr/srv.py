from struct import unpack

from .rdata import RData
from ..util import sub, read_labels

class SRV(RData):
	def decode(self):
		header = sub(self.raw, self.offset, 6)
		offset = self.offset

		if len(header) == 6:
			self.priority, self.weight, self.port = unpack('!HHH', header)
			offset += 6

			offset, self.target = read_labels(self.raw, offset)
			self.length = offset - self.offset
			self.raw = sub(self.raw, self.offset, self.length)

		return self
