from struct import unpack, pack

def sub(data: bytes, offset: int, length: int) -> bytes:
	return data[offset:offset+length]

def decode_labels(raw: bytes, offset: int) -> tuple:
	"""
	This method does the buffer gymnastics of unpacking a set of labels.

	From the RFC:
	A domain name represented as a sequence of labels, where each label
	consists of a length octet followed by that number of octets. The domain
	name terminates with the zero length octet for the null label of the root.
	Note that this field may be an odd number of octets; no padding is used.

	:param raw bytes: The entire RR (required for label compression)
	:param offset int: Where to start reading
	"""
	labels = []

	start = offset
	breakpoint = None

	while offset < len(raw):
		# Read a byte into llen and advance past it
		llen, = unpack('!B', sub(raw, offset, 1))
		offset += 1

		if llen & ~0x3f == 0xc0:
			# If the first two bits of a length value are 1 and 1 (0xc)
			# then this is a jump, and the following 14 bytes indicate where
			# in the raw data we should jump to.

			# Read a byte into target, then advanced past it
			target, = unpack('!B', sub(raw, offset, 1))
			offset += 1

			# Store the breakpoint so we know where to return to when we're
			# done jumping around, but only the first time since there may
			# be multiple jumps
			if breakpoint == None:
				breakpoint = offset

			# Mask the first two indicator bits and merge the rest together
			# into an offset to jump to
			offset = ((llen & 0x3) << 14) | target

			# Then continue reading there
			continue

		elif llen == 0:
			# A length of 0 means that this is the null (root) label,
			# stop decoding here
			break

		labels.append(sub(raw, offset, llen))
		offset += llen

	if breakpoint:
		offset = breakpoint

	return (offset, labels)

def encode_labels(labels: list) -> bytes:
	label = bytes()

	# append labels prefixed by their length
	for name in labels:
		length = len(name)
		label += pack('!H', length)
		label += name

	# The null (root, zero length) label
	label += b'\x00'

	return label
