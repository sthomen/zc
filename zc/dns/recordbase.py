from struct import pack, unpack

from .data import Data
from .util import sub

class RecordBase(Data):
	def __init__(self, raw, offset = 0):
		self.offset = offset
		Data.__init__(self, raw)
