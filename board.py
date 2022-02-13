from vector2 import *
from space import *

class Board:
	def __init__(self):
		self.map = []

	def reset(self):
		self.map = []
		for x in range(10):
			for y in range(10):
				self.map.append(Space(Vector2(x, y)))

	def get_space(self, position):
		return self.map[position.y + position.x * 10]

	def board_cleared(self):
		for m in self.map:
			if m.has_ship and (not m.hit):
				return False
		return True

	def set_ship(self, ship, position=Vector2(), orientation="h", direction=1):
		"""Takes a position, and tries to set a given ship based on the orientation (h: horizontal, v: vertical)"""
		pos = Vector2(position.x, position.y)
		if pos.x < 0 or pos.x > 9 or pos.y < 0 or pos.y > 9:
			return False
		if orientation == "h":
			works = True
			for x in range(ship.size):
				pos.x = position.x + x * direction
				if pos.x < 0 or pos.x > 9:
					return False
				if self.get_space(pos).has_ship:
					works = False
					return False
					break
			if works:
				for x in range(ship.size):
					pos.x = position.x + x * direction
					self.get_space(pos).set_ship(ship)
		elif orientation == "v":
			works = True
			for y in range(ship.size):
				pos.y = position.y + y * direction
				if pos.y < 0 or pos.y > 9:
					return False
				if self.get_space(pos).has_ship:
					works = False
					return False
					break
			if works:
				for y in range(ship.size):
					pos.y = position.y + y * direction
					self.get_space(pos).set_ship(ship)
		return True