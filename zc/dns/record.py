from struct import pack, unpack

from .recordbase import RecordBase
from .util import sub, read_labels
from . import rr

class Record(RecordBase):
	"""
	A resource record (RR)

	section  length
	--------------------
	NAME     (variable)
	TYPE     2 bytes
	CLASS    2 bytes
	TTL      4 bytes
	RDLENGTH 2 bytes
	RDATA    (variable, see rdlength)
	"""

	def decode(self):
		offset, self.labels = read_labels(self.raw, self.offset)
		header = sub(self.raw, offset, 10)

		if len(header) == 10:
			self.type, self['class'], self.ttl, self.rdlength = unpack('!HHIH', header)

			offset += 10

			self.rdata = rr.getInstance(self.type, self.raw, offset, self.rdlength)

			if self.rdata:
				offset += self.rdata.length

		self.length = offset - self.offset
		self.raw = sub(self.raw, self.offset, self.length)

		return self
