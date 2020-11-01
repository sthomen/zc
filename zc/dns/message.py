from struct import pack,unpack

from .data import Data
from .flags import Flags
from .record import Record
from .query import Query
from .invalidpacket import InvalidPacket

class Message(Data):
	FORMAT = '!HHHHHH'

	QUESTION   = 0
	ANSWER     = 1
	NS         = 2
	ADDITIONAL = 3

	def __init__(self, raw = None):
		self.flags = Flags()

		self.records = {
			self.QUESTION:   [],
			self.ANSWER:     [],
			self.NS:         [],
			self.ADDITIONAL: []
		}

		Data.__init__(self, raw)

	def setId(self, number):
		if not 0 <= number <= 0xff:
			raise ValueError("The ID number must be between 0 and 255")

		self.id = number
		return self

	def addRecord(self, section, record):
		if not -1 < section < 3:
			raise ValueError(f"Invalid section: {section}")

		self.records[section].append(record)
		return self

	def removeRecord(self, section, index):
		if not -1 < section < 3 and index not in self.records[section]:
			raise ValueError(f"There's no record {index} in {section}")

		del self.records[section][index]

		return self

	def record(self, section, index = 0):
		if index < len(self.records[section]):
			return self.records[section][index]

		return None

	def question(self, index = 0):
		return self.record(self.QUESTION, index)

	def answer(self, index = 0):
		return self.record(self.ANSWER, index)

	def ns(self, index = 0):
		return self.record(self.NS, index)

	def additional(self, index = 0):
		return self.record(self.ADDITIONAL, index)

	def decode(self):
		"""
		Decode a DNS message
		"""

		if len(self.raw) < 12:
			raise InvalidPacket("Packet data was shorter than the header")

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


		# Record the "breakpoints" of the various records, this lets us slot
		# them in the right section.
		breakpoints = []
		total = 0
		for idx, cur in enumerate([ self.qcount, self.acount, self.ncount, self.xcount ]):
			breakpoints.append(cur + total)
			total += cur

		# Start with questions
		section = self.QUESTION

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

		if offset != self.length:
			raise InvalidPacket(f"Packet length ({self.length} bytes) does not match up with processed data length ({offset} bytes)")

		return self

	def encode(self):
		self.raw = bytes()

		if not self.id:
			self.id = 0

		self.qcount = len(self.records[self.QUESTION])
		self.acount = len(self.records[self.ANSWER])
		self.ncount = len(self.records[self.NS])
		self.xcount = len(self.records[self.ADDITIONAL])

		self.raw += pack(
			self.FORMAT,
			self.id,
			self.flags.encode().raw,
			self.qcount,
			self.acount,
			self.ncount,
			self.xcount
		)

		for section in [ self.QUESTION, self.ANSWER, self.NS, self.ADDITIONAL ]:
			for item in self.records[section]:
				self.raw += item.encode().raw

		return self
