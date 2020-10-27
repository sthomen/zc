from unittest import TestCase

from zc.dns import Flags

class TestFlags(TestCase):
	def test_given_a_zero_that_the_no_flag_is_set(self):
		number = 0x0

		flags = Flags(number)

		self.assertFalse(flags.qr)
		self.assertFalse(flags.aa)
		self.assertFalse(flags.tc)
		self.assertFalse(flags.rd)
		self.assertFalse(flags.ra)
		self.assertFalse(flags.z)
		self.assertFalse(flags.ad)
		self.assertFalse(flags.cd)

	def test_given_all_ones_that_all_flags_are_set(self):
		number = 0xffff

		flags = Flags(number)

		self.assertTrue(flags.qr)
		self.assertTrue(flags.aa)
		self.assertTrue(flags.tc)
		self.assertTrue(flags.rd)
		self.assertTrue(flags.ra)
		self.assertTrue(flags.z)
		self.assertTrue(flags.ad)
		self.assertTrue(flags.cd)

	def test_given_only_opcode_and_rcode_that_no_flags_are_set_but_opcode_and_rcode_are(self):
		# This could have been 0b01111000000001111 but hex is so much cooler
		number = 0x780f

		flags = Flags(number)

		self.assertFalse(flags.qr)
		self.assertFalse(flags.aa)
		self.assertFalse(flags.tc)
		self.assertFalse(flags.rd)
		self.assertFalse(flags.ra)
		self.assertFalse(flags.z)
		self.assertFalse(flags.ad)
		self.assertFalse(flags.cd)

		self.assertEqual(0xf, flags.opcode)
		self.assertEqual(0xf, flags.rcode)

	def test_setting_flags_yeilds_the_expected_number_when_encoding(self):
		flags = Flags()

		flags.qr = True
		flags.tc = True
		flags.ra = True
		flags.cd = True

		# Should become 0b1000001010010000

		self.assertEqual(0x8290, flags.encode().raw)

