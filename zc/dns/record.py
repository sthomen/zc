from struct import pack, unpack

from .recordbase import RecordBase
from .util import sub, decode_labels
from .rr import RR
from .invalidrecord import InvalidRecord

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

	CLASS_IN = 1
	CLASS_CS = 2
	CLASS_CH = 3
	CLASS_HS = 4

	def setTTL(self, ttl):
		self.ttl = ttl
		return self

	def setData(self, rdata):
		self.rdata = rdata
		self.rdlength = len(rdata)
		return self

	def decode(self):
		offset, self.labels = decode_labels(self.raw, self.offset)
		header = sub(self.raw, offset, 10)

		if len(header) != 10:
			raise InvalidRecord("There wasn't enough bytes left in the packet to read in the record header")

		self.type, \
		self['class'], \
		self.ttl, \
		self.rdlength = unpack('!HHIH', header)

		offset += 10

		self.rdata = RR().byType(self.type, raw=self.raw, offset=offset, length=self.rdlength)

		if self.rdata:
			offset += len(self.rdata)

		self.raw = sub(self.raw, self.offset, offset - self.offset)

		return self

	def encode(self):
		rdata = self.rdata.encode().raw
		# update rdlength
		self.rdlength = len(rdata)

		self.raw = bytes()
		self.raw += pack('!HHIH', self.type, self['class'], self.ttl, self.rdlength)
		self.raw += rdata

		return self
