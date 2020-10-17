class Data(dict):
	"""
	Handy data class stub for binary data.
	Do not instantiate directly, use a subclass.
	"""
	def __init__(self, raw = None):
		"""
		Initialize data class with the raw, decoding it if set

		:param raw bytes: Raw data bytes
		"""
		self.raw = raw

		if raw:
			self.decode()

	def __bytes__(self):
		return self.encode().raw

	def __getattr__(self, key):
		if key in self:
			return self[key]

		return None

	def __setattr__(self, key, value):
		self[key] = value

	def decode(self):
		"""
		Stub decode method

		"""
		return self

	def encode(self):
		"""
		Stub encode method

		"""
		return self
