class Vector2:
	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y

	def tuple(self):
		return (self.x, self.y)

	def __add__(self, other):
		return Vector2(self.x + other.x, self.y + other.y)