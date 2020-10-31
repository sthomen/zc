from .data import Data
from .util import sub

class RecordBase(Data):
	def __init__(self, raw = None, offset = 0):
		self.offset = offset
		self['class'] = 1 # default to IN
		Data.__init__(self, raw)

	def setLabels(self, *labels):
		"""
		Set the record label, all records can have labels, but they
		do not have to.

		A label MUST be a list of bytes

		:param labels list: a list of bytes objects
		"""
		self.labels = list(labels)
		return self

	def setClass(self, cls):
		"""
		Set the record class

		:param cls int: RR class
		"""
		self['class'] = cls
		return self

	def setType(self, type):
		"""
		Set the record type

		:param type int: RR type
		"""
		self.type = type
		return self
