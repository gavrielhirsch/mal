class Env:
	def __init__(self, outer):
		self.outer = outer
		self.data = {}
	def set(self, key, val):
		self.data[key] = val
	def find(self, key):
		if (key in self.data):
			return self
		elif (self.outer is None):
			return None
		else:
			return self.outer.find(key)
	def get(self, key):
		envm = self.find(key)
		if (envm is None):
			raise ValueError("'" + key + "' was not found")
		else:
			return envm.data[key]
