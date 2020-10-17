from .data import Data

class Flags(Data):
	# QR values
	REQUEST  = False
	RESPONSE = True

	# OpCode values
	QUERY    = 0
	IQUERY   = 1
	STATUS   = 2

	# RCode values
	NOERROR  = 0
	FORMERR  = 1
	SERVFAIL = 2
	NXDOMAIN = 3
	NOTIMP   = 4
	REFUSED  = 5
	YXDOMAIN = 6
	YXRRSET  = 7
	NXRRSET  = 8
	NOTAUTH  = 9
	NOTZONE  = 10

	def decode(self):
		"""
		Decode message flags

		                               1  1  1  1  1  1
		 0  1  2  3  4  5  6  7  8  9  0  1  2  3  4  5
		+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
		|QR|   OpCode  |AA|TC|RD|RA| Z|AD|CD|   RCODE   |
		+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

		QR: 0 = request, 1 = response

		OpCode:
			QUERY     0 A standard query
			IQUERY    1 An inverse query
			STATUS    2 A server status request

			3-15 unused(?)

		AA: Authoritative answer, true if autoritative
		TC: Truncation - this message was truncated due to length
		RD: Recursion Desired
		RA: Recursion Available
		Z:  Reserved
		AD: ?
		CD: ?

		RCODE:
			NOERROR   0 No error
			FORMERR   1 Query format error
			SERVFAIL  2 Internal failure processing the response
			NXDOMAIN  3 No such domain
			NOTIMP    4 Unsupported OpCode
			REFUSED   5 Query refused
			YXDOMAIN  6 Some name that ougt not to exist, does exist
			YXRRSET   7 Some RRset that ougt not to exist, does exist
			NXRRSET   8 Some RRset that ougt to exist, does not exist
			NOTAUTH   9 The server is not authorative for the zone named
			NOTZONE  10 A name used in the Prerequisite or Update section is not
						within the zone denoted by the Zone Section

		:param flags int: Flags bitfield
		"""
		self.qr     = bool((self.raw >> 15))
		self.opcode = (self.raw      >> 11) & 0xf
		self.aa     = bool((self.raw >> 10) & 0x1)
		self.tc     = bool((self.raw >> 9) & 0x1)
		self.rd     = bool((self.raw >> 8) & 0x1)
		self.ra     = bool((self.raw >> 7) & 0x1)
		self.z      = bool((self.raw >> 6) & 0x1)
		self.ad     = bool((self.raw >> 5) & 0x1)
		self.cd     = bool((self.raw >> 4) & 0x1)
		self.rcode  = self.raw & 0xf

		return self

	def encode(self):
		"""
		Encode the values in the flags back to a binary set of 16 bits

		See decode for the format

		"""
		value = 0

		if self.qr:     value |= 1 << 15
		if self.opcode: value |= self.opcode << 11
		if self.aa:     value |= 1 << 10
		if self.tc:     value |= 1 << 9
		if self.rd:     value |= 1 << 8
		if self.ra:     value |= 1 << 7
		if self.z:      value |= 1 << 6
		if self.ad:     value |= 1 << 5
		if self.cd:     value |= 1 << 4
		if self.rcode:  value |= self.rcode

		self.raw = value

		return self
