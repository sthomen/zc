from struct import unpack

class Data(dict):
	"""
	Base data class used by the Flags and Message classes
	"""
	def __init__(self, raw = None):
		"""
		Initialize data class with the raw, decoding it if set

		:param raw bytes: Raw data bytes
		"""
		self.raw = raw

		if raw:
			self.decode()

	def __getattr__(self, key):
		if key in self:
			return self[key]

		return None

	def __setattr__(self, key, value):
		self[key] = value

class Flags(Data):
	REQUEST  = 0
	RESPONSE = 1

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
		self.qr     = bool(self.raw >> 15)
		self.opcode = (self.raw >> 11) & 0xf
		self.aa     = bool((self.raw >> 10) & 0x1)
		self.tc     = bool((self.raw >> 9) & 0x1)
		self.rd     = bool((self.raw >> 8) & 0x1)
		self.ra     = bool((self.raw >> 7) & 0x1)
		self.z      = bool((self.raw >> 6) & 0x1)
		self.ad     = bool((self.raw >> 5) & 0x1)
		self.cd     = bool((self.raw >> 4) & 0x1)
		self.rcode  = self.raw & 0xf

		return self

class Message(Data):
	def decode(self):
		"""
		Decode a DNS message

		:param raw bytes: The raw message
		"""
		(id, flags, zcount, pcount, ucount, acount) = unpack('!HHHHHH', self.raw[:12])

		self.update({
			'id':     id,
			'flags':  Flags(flags),
			'zcount': zcount,
			'pcount': pcount,
			'ucount': ucount,
			'acount': acount
		})

		return self
