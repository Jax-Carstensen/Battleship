from vector2 import *
import pygame


class Image:
	def __init__(self, src, draw_width=64, draw_height=64):
		self.src = src
		self.image = pygame.image.load(self.src).convert_alpha()
		self.rescale(Vector2(draw_width, draw_height))
		self.image_rect = self.image.get_rect()
		self.dimensions = Vector2(self.image.get_width(), self.image.get_height())

	def rescale(self, new_dimensions):
		if self.image.get_width() != self.image.get_height():
			x = new_dimensions.x
			y = x
			new_dimensions = Vector2(int(new_dimensions.x), int(round(new_dimensions.x / self.image.get_width() * self.image.get_height())))
		self.image = pygame.transform.scale(self.image, new_dimensions.tuple()).convert_alpha()
		self.dimensions = Vector2(self.image.get_width(), self.image.get_height())

	def draw(self, screen, position, flip=False):
		if flip:
			screen.blit(pygame.transform.flip(self.image, True, False), position.tuple())
		else:
			screen.blit(self.image, position.tuple())