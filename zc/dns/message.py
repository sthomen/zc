from struct import pack,unpack

from .data import Data
from .flags import Flags

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

		# Load data parts
		# TODO

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
