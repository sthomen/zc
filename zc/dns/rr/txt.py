from struct import unpack
from collections import OrderedDict()

from .rdata import RData
from ..util import sub, decode_labels

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
			llen, = unpack('!B', sub(self.raw, offset, 1))

			offset += 1

			key, value = sub(self.raw, offset, llen).split(b'=')
			self.data[key] = value

			offset += llen

		return self

	def encode(self):
		self.raw = bytes()

		for key, value in self.data.items():
			value = b'='.join([ key, value ])
			self.raw += pack('!B', len(value))
			self.raw += value

		return self
