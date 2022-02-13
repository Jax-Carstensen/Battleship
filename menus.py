from vector2 import *

class Menu:
	def __init__(self, name="", components=[], inputs=[]):
		self.name = name
		self.components = components
		self.inputs = inputs
		self.clicked_index = -1

	def draw(self, screen, multiplier, game):
		for component in self.components:
			component.draw(screen, multiplier, game)
			if component.manage_hover():
				game.play_sound(game.click_sound)

		for i in self.inputs:
			i.draw(screen, multiplier, game)

	def update(self, game):
		for component in self.components:
			if game.box_collides(game.mouse_pos, component.get_position(game.multiplier), Vector2(1, 1), component.get_size(game.multiplier)):
				component.hover(True, game.delta_time)
				if game.unmanaged_click:
					game.unmanaged_click = False
					a = component.click()
					if len(a) > 1:
						game.manage_event(a[0], a[1])
					else:
						game.manage_event(a[0])
			else:
				component.hover(False, game.delta_time)
		for i in self.inputs:
			if game.box_collides(game.mouse_pos, i.get_position(game.multiplier), Vector2(1, 1), i.get_size(game.multiplier)):
				if game.unmanaged_click:
					game.unmanaged_click = False
					i.click()
					print("Input")
			elif game.unmanaged_click and i.clicked:
				i.clicked = False
				if self.inputs.index(i) == self.clicked_index:
					self.clicked_index = -1

	def manage_character(self, character, game):
		for i in self.inputs:
			if i.clicked:
				i.add_character(character, game)