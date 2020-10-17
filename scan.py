#!/usr/bin/env python

from struct import unpack
from zc import MulticastListener

def decode_flags(flags):
	"""
	Flags
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
	qr     = flags >> 15
	opcode = (flags >> 11) & 0xf
	aa     = (flags >> 10) & 0x1
	tc     = (flags >> 9) & 0x1
	rd     = (flags >> 8) & 0x1
	ra     = (flags >> 7) & 0x1
	z      = (flags >> 6) & 0x1
	ad     = (flags >> 5) & 0x1
	cd     = (flags >> 4) & 0x1
	rcode  = flags & 0xf

	return (qr, opcode, aa, tc, rd, ra, z, ad, cd, rcode)

def decode_header(raw):
	(id, flags, zcount, pcount, ucount, acount) = unpack('!HHHHHH', raw)

	print(f"Query id: 0x{id:x}")
	print(f"Flags: 0x{flags:x}")
	(qr, opcode, aa, tc, rd, ra, z, ad, cd, rcode) = decode_flags(flags)

	print(f"      QR: {qr:b}")
	print(f"  OpCode: {opcode}")
	print(f"      AA: {aa:b}")
	print(f"      TC: {tc:b}")
	print(f"      RD: {rd:b}")
	print(f"      RA: {ra:b}")
	print(f"       Z: {z:b}")
	print(f"      AD: {ad:b}")
	print(f"      CD: {cd:b}")
	print(f"   RCODE: {rcode}")

	print(f"Numer of RRs in the zone section: {zcount}")
	print(f"Number of RRs in the prerequisite section: {pcount}")
	print(f"Number of RRs in the update section: {ucount}")
	print(f"Number of RRs in the additional data section: {acount}")


listener = MulticastListener().register('224.0.0.251', 5353)

while True:
	data, remote = listener.receive()
	print(f"Received packet from {remote}")
	print(decode_header(data[:12]))

listener.unregister()
