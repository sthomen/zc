from unittest import TestCase

from zc.dns.recordbase import RecordBase

class TestRecordBase(TestCase):
	def test_that_it_is_possible_to_set_labels_from_both_str_and_bytes(self):
		rb = RecordBase()
		rb.setLabels(b'foo', b'bar')
		rb.setLabels('foo', 'bar')
		rb.setLabels(b'foo', 'bar')
