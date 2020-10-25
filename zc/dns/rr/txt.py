from struct import unpack

from .rdata import RData
from ..util import sub, read_labels

class TXT(RData):
	"""
	TXT records are a string of name/value pairs prefixed by their combined length
	and separated by = signs.
	"""
	def decode(self):
		self.raw = sub(self.raw, self.offset, self.length)

		self.data = {}
		offset = 0

		while offset < self.length:
			llen = int(unpack('!B', sub(self.raw, offset, 1))[0])

			offset += 1

			key, value = sub(self.raw, offset, llen).split(b'=')
			self.data[key] = value

			offset += llen

		return self
