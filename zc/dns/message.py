from struct import pack,unpack

from .data import Data
from .flags import Flags
from .record import Record
from .query import Query

class Message(Data):
	FORMAT = '!HHHHHH'

	# Is anything but 1 used, ever?
	CLASS_IN = 1
	CLASS_CS = 2
	CLASS_CH = 3
	CLASS_HS = 4

	SEC_QUESTION   = 0
	SEC_ANSWER     = 1
	SEC_NS         = 2
	SEC_ADDITIONAL = 3

	def decode(self):
		"""
		Decode a DNS message
		"""

		# Read the header
		(
			self.id,
			flags,
			self.qcount,
			self.acount,
			self.ncount,
			self.xcount
		) = unpack(self.FORMAT, self.raw[:12])

		# Decode the flags
		self.flags = Flags(flags)

		# We're now at an offset of 12, store the packet length for later
		offset=12
		self.length = len(self.raw)

		# Prime records dict
		self.records = {
			self.SEC_QUESTION:   [],
			self.SEC_ANSWER:     [],
			self.SEC_NS:         [],
			self.SEC_ADDITIONAL: []
		}

		# Record the "breakpoints" of the various records, this lets us slot
		# them in the right section.
		breakpoints = []
		total = 0
		for idx, cur in enumerate([ self.qcount, self.acount, self.ncount, self.xcount ]):
			breakpoints.append(cur + total)
			total += cur

		# Start with questions
		section = self.SEC_QUESTION

		for index in range(0, total):
			# If this is not a response (qr = True) then the record format
			# lacks a bunch of fields and needs to be treated special. This
			# could just as well check the section we're currently recording.
			if self.flags.qr != True:
				record = Query(self.raw, offset)
			else:
				record = Record(self.raw, offset)

			offset+=len(record)

			# Find the appropriate section to put this entry in
			for section, bp in enumerate(breakpoints):
				if index < bp:
					break

			# Slot it in place
			self.records[section].append(record)

		return self

	def encode(self):
		if not self.id:
			self.id = 0

		self.raw = pack(
			self.FORMAT,
			self.id,
			flags.encode().raw,
			self.qcount,
			self.acount,
			self.ncount,
			self.xcount
		)

		for section in [ self.SEC_QUESTION, self.SEC_ANSWER, self.SEC_NS, self.SEC_ADDITIONAL ]:
			for item in self.records[section]:
				self.raw += item.encode().raw

		return self
