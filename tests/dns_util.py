from unittest import TestCase

from zc.dns.util import decode_labels, encode_labels

class TestUtils(TestCase):
	def test_decoding_single_label_without_jumps(self):
		label = b'\x01a\x00'

		offset, labels = decode_labels(label, 0)

		self.assertEqual([b'a'], labels)
		self.assertEqual(3, offset)
		
	def test_decoding_multiple_labels_without_jumps(self):
		label = b'\x05hello\x03dot\x03com\x00'

		offset, labels = decode_labels(label, 0)

		self.assertEqual([b'hello', b'dot', b'com'], labels)
		self.assertEqual(15, offset)

	def test_decoding_multiple_labels_with_a_jump(self):
		label = b'\x03dot\x03com\x00\x05hello\xc0\x00'

		offset, labels = decode_labels(label, 9)

		self.assertEqual([b'hello', b'dot', b'com'], labels)
		self.assertEqual(17, offset)

	def test_decoding_multiple_labels_with_multiple_jumps(self):
		label = b'\x03com\x00\x03dot\xc0\x00\x05hello\xc0\x05'

		offset, labels = decode_labels(label, 11)

		self.assertEqual([b'hello', b'dot', b'com'], labels)
		self.assertEqual(19, offset)

	def test_encoding_singe_label(self):
		labels = [ b'hello' ]

		label = encode_labels(labels)

		self.assertEqual(b'\x05hello\x00', label)

	def test_encoding_multiple_labels(self):
		labels = [ b'hello', b'dot', b'com' ]

		label = encode_labels(labels)

		self.assertEqual(b'\x05hello\x03dot\x03com\x00', label)
