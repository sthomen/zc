from struct import pack,unpack

from .data import Data
from .flags import Flags
from .record import Record
from .query import Query

class Message(Data):
	FORMAT = '!HHHHHH'

	def decode(self):
		"""
		Decode a DNS message

		:param raw bytes: The raw message
		"""
		# Unpack the header

		(
			self.id,
			flags,
			self.zcount,
			self.pcount,
			self.ucount,
			self.acount
		) = unpack(self.FORMAT, self.raw[:12])

		# Initialize flags
		self.flags = Flags(flags)

		# Load the records

		self.records = []

		offset=12
		self.length = len(self.raw)

		for r in range(0, (self.zcount + self.pcount + self.ucount + self.acount)):
			if self.flags.qr:
				record = Record(self.raw, offset)
			else:
				record = Query(self.raw, offset)

			offset+=len(record)
			self.records.append(record)

		return self

	def encode(self):
		# Encode the header

		self.raw = pack(
			self.FORMAT,
			self.id,
			flags.encode().raw,
			self.zcount,
			self.pcount,
			self.ucount,
			self.acount
		)

		# Encode the data parts
		# TODO

		return self
