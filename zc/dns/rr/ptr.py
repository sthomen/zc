from .rdata import RData
from ..util import sub, read_labels

class PTR(RData):
	def decode(self):
		offset, self.target = read_labels(self.raw, self.offset)
		self.raw = sub(self.raw, self.offset, offset - self.offset)
		return self
