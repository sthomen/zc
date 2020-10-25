from struct import pack,unpack

from .data import Data
from .flags import Flags
from .record import Record
from .query import Query

class Message(Data):
	FORMAT = '!HHHHHH'

	SEC_QUESTION   = 0
	SEC_ANSWER     = 1
	SEC_NS         = 2
	SEC_ADDITIONAL = 3

	def decode(self):
		"""
		Decode a DNS message

		:param raw bytes: The raw message
		"""
		(
			self.id,
			flags,
			self.qcount,	# Question
			self.acount,	# Answer
			self.ncount,	# Nameservers
			self.xcount		# Additional records
		) = unpack(self.FORMAT, self.raw[:12])

		self.flags = Flags(flags)

		offset=12
		self.length = len(self.raw)

		self.records = {
			self.SEC_QUESTION:   [],
			self.SEC_ANSWER:     [],
			self.SEC_NS:         [],
			self.SEC_ADDITIONAL: []
		}

		breakpoints = []
		total = 0
		for idx, cur in enumerate([ self.qcount, self.acount, self.ncount, self.xcount ]):
			breakpoints.append(cur + total)
			total += cur

		section = self.SEC_QUESTION

		for index in range(0, total):
			if self.flags.qr != True:
				record = Query(self.raw, offset)
			else:
				record = Record(self.raw, offset)

			offset+=len(record)

			# Find the appropriate section to put this entry in
			for section, bp in enumerate(breakpoints):
				if index < bp:
					break

			self.records[section].append(record)

		return self

	def encode(self):
		if not self.id:
			self.id = 0

		self.raw = pack(
			self.FORMAT,
			self.id,
			flags.encode().raw,
			self.zcount,
			self.pcount,
			self.ucount,
			self.acount
		)

		return self
