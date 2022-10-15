from genki_wave.data import ButtonEvent, DataPackage
#from ringbuffer import RingBuffer
from genki_wave.callbacks import WaveCallback
from genki_wave.threading_runner import WaveListener
from typing import Union
import time

ble_address = "DE:C5:2E:CA:F5:F8"

#Hér byrjar ringbuffer.py shitfix.
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
#Shitfix ringbuffer.py endar hér.



class BufferData(WaveCallback):
	def __init__(self, buffer: RingBuffer):
		self.buffer = buffer

	def _data_handler(self, data: DataPackage) -> None:
		self.buffer.add(data)

	def _button_handler(self, data: ButtonEvent) -> None:
		pass

	def __call__(self, data: Union[ButtonEvent, DataPackage]) -> None:
		if isinstance(data, ButtonEvent):
			self._button_handler(data)
		elif isinstance(data, DataPackage):
			self._data_handler(data)
		else:
			raise ValueError(f"Got data of unexpected type {type(data)}")



buffer1 = RingBuffer(20)

cb = BufferData(buffer1)
with WaveListener(ble_address, [cb]):
	while True:
		for package in buffer1:
			print(package)
		print()
		time.sleep(0.1)