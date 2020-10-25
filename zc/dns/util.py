from struct import unpack

def sub(data: bytes, offset: int, length: int) -> bytes:
	return data[offset:offset+length]

def read_labels(raw: bytes, offset: int) -> tuple:
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
		llen, first = unpack('!BB', sub(raw, offset, 2))

		if llen & ~0x3f == 0xc0:
			# A pointer
			# Store how far we got before jumping plus two bytes (length and first),
			# this is where decoding will continue when the labels are done, but
			# only record this value if it's the first jump
			if breakpoint == None:
				breakpoint = offset + 2

			# Use the original raw data, and find an offset
			offset = ((llen & 0x3) << 14) | first

			# Then continue reading
			continue

		elif llen == 0:
			# We're done, skip past the null byte and stop
			offset += 1
			break
		else:
			# skip past length byte
			offset += 1

		# Store the label here
		labels.append(sub(raw, offset, llen))
		offset += llen

	if breakpoint:
		offset = breakpoint

	return (offset, labels)
