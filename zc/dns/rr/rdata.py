from ..data import Data

class RData(Data):
	def __init__(self, raw, offset, length):
		self.offset = offset
		self.length = length
		Data.__init__(self, raw)
