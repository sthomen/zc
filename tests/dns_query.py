from unittest import TestCase

from zc.dns import Query

class TestQuery(TestCase):
	def setUp(self):
		# NOTE This is not the entire packet, it just the query part(s) of it. A real packet would also include the
		# headers, and the offsets in the packet would include those
		# Offset 0 will NOT be found in the wild
		# The LENGTH of the Query will NOT include the header data
		self.packet = b'\x04test\x04_sub\x0b_googlecast\x04_tcp\x05local\x00\x00\x0c\x80\x01\xc0\x05\x00\x0c\x80\x01'

	def test_given_packet_data_that_decoding_produces_valid_labels_types_classes_and_lengths(self):
		query = Query(self.packet, 0)

		self.assertEqual([b'test', b'_sub', b'_googlecast', b'_tcp', b'local'], query.labels)
		self.assertEqual(12, query.type)
		self.assertEqual(32769, query['class'])
		self.assertEqual(38, len(query))

	def test_given_packet_data_that_decoding_produces_valid_labels_types_classes_and_lengths_in_an_offset_query_with_jumps(self):
		query = Query(self.packet, 38)

		self.assertEqual([b'_sub', b'_googlecast', b'_tcp', b'local'], query.labels)
		self.assertEqual(12, query.type)
		self.assertEqual(32769, query['class'])
		self.assertEqual(6, len(query))
