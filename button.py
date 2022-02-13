from vector2 import *
import pygame

class Button:
	def __init__(self, text, position=Vector2(), width=1920, height=1080, onclick=None, center_x=False, arg=None, top_left="", bottom_left="", permanent=False):
		self.title = text
		self.position = position
		self.width = width
		self.height = height
		self.start_width = width
		self.unhandled_hover = False
		self.hovered = False
		self.onclick = onclick
		self.center_x = center_x
		self.arg = arg
		self.top_left = top_left
		self.bottom_left = bottom_left
		self.permanent = permanent

	def click(self):
		if self.arg != None:
			return [self.onclick, self.arg]
		return [self.onclick]

	def get_position(self, multiplier):
		if self.center_x:
			return Vector2(self.position.x * multiplier - self.width * multiplier * 0.5, self.position.y * multiplier)
		return Vector2(self.position.x * multiplier, self.position.y * multiplier)
	
	def get_size(self, multiplier):
		return Vector2(self.width * multiplier, self.height * multiplier)

	def draw(self, screen, multiplier, game):
		if self.center_x:
			self.draw_center_x(screen, multiplier, game)
			return
		# Left shadow triangle
		pygame.draw.polygon(screen, (0, 0, 0), points=[
			(self.position.x * multiplier + (self.start_width * multiplier * 0.0125) + 1, self.position.y * multiplier + self.height * multiplier + (self.height * multiplier * 0.125) - 1), 
			(self.position.x * multiplier + (self.start_width * multiplier * 0.0125) + 1, self.position.y * multiplier + (self.height * multiplier * 0.125)),
			(self.position.x * multiplier - self.start_width * multiplier * 0.05 + (self.start_width * multiplier * 0.0125) + 1, self.position.y * multiplier + self.height * multiplier + (self.height * multiplier * 0.125) - 1),
		])
		# Shadow rectangle
		pygame.draw.rect(screen, (0, 0, 0), (self.position.x * multiplier + (self.width * multiplier * 0.0125), self.position.y * multiplier + (self.height * multiplier * 0.125), self.width * multiplier, self.height * multiplier))
		# Right shadoe triangle
		pygame.draw.polygon(screen, (0, 0, 0), points=[
			(self.position.x * multiplier + self.width * multiplier + (self.width * multiplier * 0.0125) - 1, self.position.y * multiplier + self.height * multiplier + (self.height * multiplier * 0.125) - 1), 
			(self.position.x * multiplier + self.width * multiplier + (self.width * multiplier * 0.0125) - 1, self.position.y * multiplier + (self.height * multiplier * 0.125)),
			(self.position.x * multiplier + self.width * multiplier + self.width * multiplier * 0.05 + (self.width * multiplier * 0.0125) - 1, self.position.y * multiplier + (self.height * multiplier * 0.125)),
		])

		# Left main triangle
		pygame.draw.polygon(screen, (65, 65, 65), points=[
			(self.position.x * multiplier, self.position.y * multiplier + self.height * multiplier - 1), 
			(self.position.x * multiplier, self.position.y * multiplier),
			(self.position.x * multiplier - self.start_width * multiplier * 0.05, self.position.y * multiplier + self.height * multiplier - 1),
		])
		# Main rectangle
		pygame.draw.rect(screen, (65, 65, 65), (self.position.x * multiplier, self.position.y * multiplier, self.width * multiplier, self.height * multiplier))
		# Right main triangle
		pygame.draw.polygon(screen, (65, 65, 65), points=[
			(self.position.x * multiplier + self.width * multiplier - 1, self.position.y * multiplier + self.height * multiplier - 1), 
			(self.position.x * multiplier + self.width * multiplier - 1, self.position.y * multiplier),
			(self.position.x * multiplier + self.width * multiplier + self.width * multiplier * 0.05 - 1, self.position.y * multiplier),
		])
		# Draws button text
		game.draw_text(self.title, Vector2(self.position.x * multiplier, self.position.y * multiplier) + Vector2(multiplier * 16, 0), (255, 255, 255), vertical_center=Vector2(self.width * multiplier, self.height * multiplier))
		#game.draw_text(self.bottom_left, Vector2(self.position.x * multiplier * 1.1, self.position.y * multiplier), (255, 255, 255))

	def draw_center_x(self, screen, multiplier, game):
		# Left shadow triangle
		pygame.draw.polygon(screen, (0, 0, 0), points=[
			(self.position.x * multiplier + (self.start_width * multiplier * 0.0125) + 1 - self.width * multiplier * 0.5, self.position.y * multiplier + self.height * multiplier + (self.height * multiplier * 0.125) - 1), 
			(self.position.x * multiplier + (self.start_width * multiplier * 0.0125) + 1 - self.width * multiplier * 0.5, self.position.y * multiplier + (self.height * multiplier * 0.125)),
			(self.position.x * multiplier - self.start_width * multiplier * 0.05 + (self.start_width * multiplier * 0.0125) + 1 - self.width * multiplier * 0.5, self.position.y * multiplier + self.height * multiplier + (self.height * multiplier * 0.125) - 1),
		])
		# Shadow rectangle
		pygame.draw.rect(screen, (0, 0, 0), (self.position.x * multiplier + (self.width * multiplier * 0.0125) - self.width * multiplier * 0.5, self.position.y * multiplier + (self.height * multiplier * 0.125), self.width * multiplier, self.height * multiplier))
		# Right shadoe triangle
		pygame.draw.polygon(screen, (0, 0, 0), points=[
			(self.position.x * multiplier + self.width * multiplier + (self.width * multiplier * 0.0125) - 1 - self.width * multiplier * 0.5, self.position.y * multiplier + self.height * multiplier + (self.height * multiplier * 0.125) - 1), 
			(self.position.x * multiplier + self.width * multiplier + (self.width * multiplier * 0.0125) - 1 - self.width * multiplier * 0.5, self.position.y * multiplier + (self.height * multiplier * 0.125)),
			(self.position.x * multiplier + self.width * multiplier + self.width * multiplier * 0.05 + (self.width * multiplier * 0.0125) - 1 - self.width * multiplier * 0.5, self.position.y * multiplier + (self.height * multiplier * 0.125)),
		])

		# Left main triangle
		pygame.draw.polygon(screen, (65, 65, 65), points=[
			(self.position.x * multiplier - self.width * multiplier * 0.5, self.position.y * multiplier + self.height * multiplier - 1), 
			(self.position.x * multiplier - self.width * multiplier * 0.5, self.position.y * multiplier),
			(self.position.x * multiplier - self.start_width * multiplier * 0.05 - self.width * multiplier * 0.5, self.position.y * multiplier + self.height * multiplier - 1),
		])
		# Main rectangle
		pygame.draw.rect(screen, (65, 65, 65), (self.position.x * multiplier - self.width * multiplier * 0.5, self.position.y * multiplier, self.width * multiplier, self.height * multiplier))
		# Right main triangle
		pygame.draw.polygon(screen, (65, 65, 65), points=[
			(self.position.x * multiplier - self.width * multiplier * 0.5 + self.width * multiplier - 1, self.position.y * multiplier + self.height * multiplier - 1), 
			(self.position.x * multiplier - self.width * multiplier * 0.5 + self.width * multiplier - 1, self.position.y * multiplier),
			(self.position.x * multiplier - self.width * multiplier * 0.5 + self.width * multiplier + self.width * multiplier * 0.05 - 1, self.position.y * multiplier),
		])
		# Draws button text
		game.draw_text(self.title, Vector2(self.position.x * multiplier - self.width * multiplier * 0.5, self.position.y * multiplier) + Vector2(multiplier * 16, 0), (255, 255, 255), center=Vector2(self.width * multiplier, self.height * multiplier))
		game.draw_text(self.bottom_left, Vector2(self.position.x * multiplier * 1.1 - self.width * multiplier * 0.5, self.position.y * multiplier + self.height * 0.925), (255, 255, 255), font=game.small_font)
		game.draw_text(self.top_left, Vector2(self.position.x * multiplier * 1.1 - self.width * multiplier * 0.5, self.position.y * multiplier), (255, 255, 255), font=game.small_font)

	def hover(self, is_hovering, delta_time):
		speed = 0.9
		if is_hovering:
			self.width += delta_time * speed
			if not self.unhandled_hover and not self.hovered:
				self.unhandled_hover = True
			self.hovered = True
		else:
			self.width -= delta_time * speed
		self.width = max(self.width, self.start_width)
		self.width = min(self.width, self.start_width * 1.275)
		if self.width == self.start_width:
			self.hovered = False

	def manage_hover(self):
		if self.unhandled_hover:
			self.unhandled_hover = False
			return True
		return False


class RoundButton(Button):
	def __init__(self, text, position=Vector2(), radius=540, onclick=None, arg=None, permanent=True):
		super().__init__(text, position, width=radius*2, height=radius*2, onclick=onclick, arg=arg, permanent=permanent)
		self.radius = radius

	def draw(self, screen, multiplier, game):
		pygame.draw.circle(screen, (0, 0, 0), (self.position.x * multiplier + (multiplier * 8), self.position.y * multiplier + (multiplier * 8)), self.radius * multiplier)
		pygame.draw.circle(screen, (0, 255, 0), (self.position.x * multiplier, self.position.y * multiplier), self.radius * multiplier)
		game.draw_text(self.title, Vector2((self.position.x - self.radius) * multiplier, (self.position.y - self.radius) * multiplier), (255, 255, 255), center=Vector2(self.radius * 2 * multiplier, self.radius * 2 * multiplier), font=game.massive_font)