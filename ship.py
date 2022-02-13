from vector2 import *

class Ship:
	def __init__(self, size=3, name="", orientation="h", direction=1):
		self.size = size
		self.name = name
		self.placed = False
		self.position = Vector2()
		self.orientation = orientation
		self.direction = direction

	def set_pos(self, pos, orientation="h", direction=1):
		self.position = pos
		self.orientation = orientation
		self.direction = direction