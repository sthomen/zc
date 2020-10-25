from .rdata import RData
from ..util import sub

class NULL(RData):
	def decode(self):
		self.raw = sub(self.raw, self.offset, self.length)
		return self
