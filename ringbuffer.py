class RingIterator:
	def __init__(self, data: RingBuffer):
		self.data = data
		self.length = data.capacity
		self.stop = data.newest + 1
		self.idx = data.oldest
		self.done = False

	def __iter__(self):
		return self

	def __next__(self):
		if self.done:
			raise StopIteration
		self.idx = (self.idx + 1) % self.length
		if self.idx == self.stop:
			self.done = True
		return self.data.contents[self.idx - 1]

class RingBuffer:
	def __init__(self, capacity: int):
		self.capacity = capacity
		self.contents = [None] * capacity
		self.newest = -1
		self.oldest = -1

	def add(self,item):
		self.newest = (self.newest + 1) % self.capacity
		self.contents[self.newest] = item
		if self.oldest < 0:
			self.oldest = 0
		elif self.oldest == self.newest:
			self.oldest = self.oldest + 1 % self.capacity

	def __iter__(self):
		return RingIterator(self)
