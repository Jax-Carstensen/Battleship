from vector2 import *

class Space:
	def __init__(self, position=Vector2()):
		self.hit = False
		self.position = position
		self.has_ship = False
		self.ship_name = ""

	def set_ship(self, ship):
		self.has_ship = True
		self.ship_name = ship.name

	def try_hit(self):
		if self.hit:
			return False
		self.hit = True
		return True