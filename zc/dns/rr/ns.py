from struct import unpack, pack

from .rdata import RData
from ..util import sub, decode_labels, encode_labels
from .rrplugin import RRPlugin

@RRPlugin.register(name='ns', type=2)
class NS(RData):
	"""
	NOTE NOTE NOTE

	This class is constructed from the spec, and NOT TESTED! This
	code was built for completeness, but mDNS doesn't seem to use
	SOA:s. Tread with care.
	"""
	def decode(self):
		offset, self.mname = decode_labels(self.raw, self.offset)
		offset, self.rname = decode_labels(self.raw, offset)

		footer = sub(self.raw, offset, 40)
		if len(footer) == 40:
			self.serial, \
			self.refresh, \
			self.retry, \
			self.expire, \
			self.minimum = unpack('!IIIII', footer)

			offset += 40

		self.raw = sub(self.raw, self.offset, offset)

		return self

	def encode(self):
		self.raw = bytes()
		self.raw += encode_labels(self.mname)
		self.raw += encode_labels(self.rname)

		self.raw += pack('!IIIII', \
			self.serial, \
			self.refresh, \
			self.retry, \
			self.expire, \
			self.minimum)

		return self
