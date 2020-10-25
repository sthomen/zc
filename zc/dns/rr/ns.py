from struct import unpack

from .rdata import RData
from ..util import sub,read_labels

class NS(RData):
	"""
	NOTE NOTE NOTE

	This class is constructed from the spec, and NOT TESTED! This
	code was built for completeness, but mDNS doesn't seem to use
	SOA:s. Tread with care.
	"""
	def decode(self):
		offset, self.mname = read_labels(self.raw, self.offset)
		offset, self.rname = read_labels(self.raw, offset)

		footer = sub(self.raw, offset, 40)
		if len(footer) == 40:
			self.serial, \
			self.refresh, \
			self.retry, \
			self.expire, \
			self.minimum = unpack('!IIIII', footer)

			offset += 40

		self.length = offset

		return self
