from struct import pack,unpack

from .recordbase import RecordBase
from .util import sub, read_labels

class Query(RecordBase):
	"""
	A query record, this differs from the regular RR in that it has no
	ttl, rdlength or rdata.

	section  length
	--------------------
	NAME     (variable)
	TYPE     2 bytes
	CLASS    2 bytes

	Name:
	A domain name represented as a sequence of labels, where each label
	consists of a length octet followed by that number of octets. The domain
	name terminates with the zero length octet for the null label of the root.
	Note that this field may be an odd number of octets; no padding is used.

	"""
	def decode(self):
		offset, self.labels = read_labels(self.raw, self.offset)
		header = sub(self.raw, offset, 4)

		if len(header) == 4:
			self.type, self['class'] = unpack('!HH', header)
			offset += 4

		self.length = offset - self.offset
		self.raw = sub(self.raw, self.offset, self.length)

		return self
