from struct import pack,unpack

from .recordbase import RecordBase
from .util import sub, decode_labels, encode_labels
from .invalidrecord import InvalidRecord

class Query(RecordBase):
	"""
	A query record, this differs from the regular RR in that it has no
	ttl, rdlength or rdata.

	section  length
	--------------------
	NAME     (variable)
	TYPE     2 bytes
	CLASS    2 bytes

	"""
	def decode(self):
		offset, self.labels = decode_labels(self.raw, self.offset)
		header = sub(self.raw, offset, 4)

		if len(header) != 4:
			raise InvalidRecord("There wasn't enough bytes left in the packet to read in the record header")

		self.type, self['class'] = unpack('!HH', header)
		offset += 4

		self.raw = sub(self.raw, self.offset, offset - self.offset)

		return self

	def encode(self):
		self.raw = bytes()
		self.raw += encode_labels(self.labels)
		self.raw += pack('!HH', self.type, self['class'])

		return self
