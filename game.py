import pygame
from time import time
from random import randint, choice
from vector2 import *
from button import *
from image import *
from menus import *
from space import *
from ship import *
from board import *


class Game:
	def __init__(self):
		self.running = False
		self.fps_cap = 60
		self.delta_time = self.fps_cap
		self.fps = 0
		self.test_height = 1080
		self.multiplier = 1
		self.mouse_down = False
		self.unmanaged_click = False
		self.current_menu = "menu"
		self.menus = []
		self.menu_index = 0
		self.mouse_over_pos = Vector2()
		self.mouse_over_spot = False
		self.current_error = ""
		self.has_error = False
		self.error_time = 0

		self.located_ship = False
		self.located_ship_position = Vector2()
		self.tried_dirs = {"l": False, "r": False, "u": False, "d": False}
		self.dir_values = {"l": Vector2(-1, 0), "r": Vector2(1, 0), "u": Vector2(0, -1), "d": Vector2(0, 1)}

		self.player_board = Board()
		self.cpu_board = Board()
		self.setting_ships = True

		self.crosshair_size = 192
		self.ships_to_set = []
		self.selected_ship_index = -1
		self.direction = 1
		self.orientation = "h"

		#Debug options
		self.force_screen_size = False

	def play_sound(self, sound):
		pygame.mixer.Sound.play(sound)

	def tuple_to_vector(self, t):
		return Vector2(t[0], t[1])

	def change_menu(self, new_menu):
		for i in range(len(self.menus)):
			if self.menus[i].name == new_menu:
				self.menu_index = i
				break
		self.current_menu = new_menu

	def set_variables(self):
		self.clock = pygame.time.Clock()
		if self.force_screen_size:
			self.screen_height = 1080
			self.screen_width = 1920
		else:
			self.screen_height = int(pygame.display.Info().current_h)
			self.screen_width = int(pygame.display.Info().current_w)
		self.multiplier = self.screen_height / self.test_height
		self.small_font = pygame.font.Font("./fonts/arial.ttf", int(25 * self.multiplier))
		self.font = pygame.font.Font("./fonts/arial.ttf", int(45 * self.multiplier))
		self.massive_font = pygame.font.Font("./fonts/arial.ttf", int(95 * self.multiplier))
		self.slightly_massiver_font = pygame.font.Font("./fonts/arial.ttf", int(110 * self.multiplier))
		self.flags = pygame.DOUBLEBUF | pygame.RESIZABLE | pygame.FULLSCREEN
		self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), self.flags)

		self.game_won = False
		self.winner = "player"
		self.load_images()
		self.viewing = "player"

		self.setup_boards()

		self.menus = [
			Menu("main", [
				Button("Singleplayer", Vector2(960, 440 - 37.5), 675, 75, onclick="singleplayer", center_x=True),
				Button("Multiplayer", Vector2(960, 540 - 37.5), 675, 75, onclick="multiplayer", center_x=True),
				Button("Quit", Vector2(960, 640 - 37.5), 675, 75, onclick="quit", center_x=True)
			]), Menu("game", [])
		]
		self.running = True

	def load_images(self):
		self.logo = Image("./images/logo.png", 800 * self.multiplier, 310 * self.multiplier)
		self.hit_symbol = Image("./images/crosshair2.png", 80 * self.multiplier, 80 * self.multiplier)
		self.hit_symbol_small = Image("./images/crosshair2.png", 32 * self.multiplier, 32 * self.multiplier)
		self.selector = Image("./images/selector.png", 80 * self.multiplier, 80 * self.multiplier)
		self.click_sound = pygame.mixer.Sound("./sounds/click.wav")
		self.arrows = Image("./images/exchange-arrows.png", 80 * self.multiplier, 80 * self.multiplier)

	def start(self):
		pygame.init()
		pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
		self.set_variables()
		#self.manage_event("singleplayer")
		#self.DEBUG_PLACE_SHIP()
		while self.running:
			exit_loop = self.manage_events()
			if exit_loop:
				self.running = False
				break
			self.update()
			self.draw()
			self.delta_time = self.clock.tick(self.fps_cap)
			self.fps = int(round(self.clock.get_fps()))

	def update(self):
		self.mouse_pos = self.tuple_to_vector(pygame.mouse.get_pos())
		self.menus[self.menu_index].update(self)
		if self.has_error:
			if time() - self.error_time > 2:
				self.has_error = False

	def setup_boards(self):
		self.ships_to_set = [
			Ship(5, "Carrier"),
			Ship(4, "Battleship"),
			Ship(3, "Cruiser"),
			Ship(3, "Submarine"),
			Ship(2, "Destroyer"),
		]
		self.player_board.reset()
		self.cpu_board.reset()
		self.auto_place_ships(False)

	def draw(self):
		self.screen.fill((25, 25, 25))
		self.menus[self.menu_index].draw(self.screen, self.multiplier, self)


		# If we're playing the game rather than in the menu
		if self.current_menu == "game":
			self.screen.fill((0, 157, 196))
			grid_size = 80
			pos = Vector2()
			padding = self.multiplier * grid_size
			pt = 960 - (grid_size * 4.5)
			# Draws the numbers that relate to 
			for i in range(10):
				self.draw_text(str(i + 1), Vector2(pt * self.multiplier, (540 * self.multiplier - (grid_size * 6 * self.multiplier))), (255, 0, 0), horizontal_center=True)
				pt += grid_size
			pt = 540 - (grid_size * 4.5)
			for i in range(10):
				self.draw_text("ABCDEFGHIJ"[i], Vector2(960 * self.multiplier - (grid_size * 6 * self.multiplier), pt * self.multiplier), (255, 0, 0), horizontal_center=True)
				pt += grid_size
			if self.setting_ships:
				s = pygame.Surface((384 * self.multiplier, 1080 * self.multiplier))
				s.set_alpha(64)
				s.fill((0,0,0))
				self.screen.blit(s, (0,0))
				bg = pygame.Surface((384 * self.multiplier, 128 * self.multiplier))
				bg.set_alpha(64)
				bg.fill((0,0,0))
				draw_pos = Vector2(0, 32 * self.multiplier)
				ind = -1
				for ship in self.ships_to_set:
					ind += 1
					draw_pos.y += self.multiplier * 150
					if ship.placed:
						continue
					self.screen.blit(bg, (draw_pos.x, draw_pos.y))
					if self.unmanaged_click:
						if self.box_collides(draw_pos, self.mouse_pos, Vector2(384 * self.multiplier, 128 * self.multiplier), Vector2(1, 1)):
							self.selected_ship_index = ind
							self.unmanaged_click = False
					if self.selected_ship_index == ind:
						pygame.draw.rect(self.screen, (255, 0, 0), (draw_pos.x, draw_pos.y, 384 * self.multiplier, 128 * self.multiplier), width=8)
					pygame.draw.rect(self.screen, (128,128,128), (self.multiplier * 32, draw_pos.y + 16 * self.multiplier, (ship.size / 5) * self.multiplier * 256, self.multiplier * 96))
					pygame.draw.polygon(self.screen, (128, 128, 128), points=[
						(self.multiplier * 32 + (ship.size / 5) * self.multiplier * 256 - 1, draw_pos.y + 16 * self.multiplier), 
						(self.multiplier * 32 + (ship.size / 5) * self.multiplier * 256 + 44 * self.multiplier, draw_pos.y + 16 * self.multiplier), 
						(self.multiplier * 32 + (ship.size / 5) * self.multiplier * 256 - 1, draw_pos.y + 16 * self.multiplier + self.multiplier * 96 - 1), 
					])
					self.draw_text(ship.name + "  (" + str(ship.size) + ")", position=Vector2(draw_pos.x + 28 * self.multiplier, draw_pos.y + 96 * self.multiplier), color=(255,255,255), font=self.small_font)
			pos = Vector2(960 * self.multiplier - (grid_size * 5.2 * self.multiplier), 540 * self.multiplier - (grid_size * self.multiplier * 4.7))
			self.mouse_over_spot = False
			board = self.get_current_board()
			for x in range(10):
				for y in range(10):
					space = board.get_space(Vector2(x, y))
					pygame.draw.rect(self.screen, (0, 0, 255), (pos.x, pos.y, self.multiplier * grid_size, self.multiplier * grid_size), 3)
					p = Vector2(pos.x, pos.y)
					if not self.mouse_over_spot:
						if self.box_collides(p, self.mouse_pos, Vector2(self.multiplier * grid_size, self.multiplier * grid_size), Vector2(1, 1)):
							self.mouse_over_spot = True
							self.mouse_over_pos = Vector2(x, y)
							if self.unmanaged_click:
								self.hit_space(Vector2(x, y))
								self.unmanaged_click = False
							if self.setting_ships:
								if self.selected_ship_index != -1:
									s = self.ships_to_set[self.selected_ship_index].size * grid_size * self.multiplier
									if self.orientation == "h":
										if self.direction == 1:
											pygame.draw.rect(self.screen, (0, 255, 0), (p.x, p.y, s, grid_size * self.multiplier))
										else:
											pygame.draw.rect(self.screen, (0, 255, 0), (p.x - s + grid_size * self.multiplier, p.y, s, grid_size * self.multiplier))
									elif self.orientation == "v":
										if self.direction == 1:
											pygame.draw.rect(self.screen, (0, 255, 0), (p.x, p.y, grid_size * self.multiplier, s))
										else:
											pygame.draw.rect(self.screen, (0, 255, 0), (p.x, p.y - s + grid_size * self.multiplier, grid_size * self.multiplier, s))
					pos.y += grid_size * self.multiplier
				pos.x += grid_size * self.multiplier
				pos.y = 540 * self.multiplier - (grid_size * self.multiplier * 4.7)
			self.draw_other_board()
			self.draw_ships(grid_size)
			self.draw_hits(grid_size)
			if not self.setting_ships:
				if self.box_collides(Vector2(1456 * self.multiplier, 56 * self.multiplier), self.mouse_pos, Vector2(463 * self.multiplier, 72 * self.multiplier), Vector2(1, 1)):
					pygame.draw.rect(self.screen, (128, 128, 128), (1456 * self.multiplier, 56 * self.multiplier, 463 * self.multiplier, 72 * self.multiplier))
					if self.unmanaged_click:
						self.unmanaged_click = False
						self.viewing = self.get_opposite_view()
				n = self.get_opposite_view() + "'s"
				if n == "player's":
					n = "your "
				txt = "view " + n + " board"
				self.arrows.draw(self.screen, Vector2(1460 * self.multiplier, 56 * self.multiplier))
				self.draw_text(txt, Vector2(1540 * self.multiplier, 64 * self.multiplier), (0,0,0), text_shadow=False)
		elif self.current_menu == "menu":
			self.logo.draw(self.screen, Vector2(self.screen_width * 0.5 - (self.multiplier * 800) * 0.5, 0))

		if self.game_won:
			pygame.draw.rect(self.screen, (0, 0, 0), (0, self.multiplier * 854, self.multiplier * 1920, self.multiplier * 216))
			pygame.draw.rect(self.screen, (255, 255, 0), (0, self.multiplier * 864, self.multiplier * 1920, self.multiplier * 216))
			self.draw_text(self.winner.title() + " won the game!", color=(255, 255, 255), position=Vector2(0, self.multiplier * 864), center=Vector2(self.multiplier * 1920, self.multiplier * 216))

		pygame.draw.rect(self.screen, (0,0,0), (0, self.mouse_pos.y, 1920 * self.multiplier, 5))
		pygame.draw.rect(self.screen, (0,0,0), (self.mouse_pos.x - 2, 0, 5, 1080 * self.multiplier))
		self.draw_errors()

		self.draw_text(f"FPS " + str(self.fps), Vector2(), color=(0, 210, 0), text_shadow=True, font=self.small_font)
		#self.crosshair.draw(self.screen, Vector2(self.mouse_pos.x - self.multiplier * self.crosshair_size * 0.5, self.mouse_pos.y - self.multiplier * self.crosshair_size * 0.5))
		pygame.display.flip()

	def cpu_turn(self):
		"""Manages the computer's AI"""
		self.check_wins()
		if self.game_won:
			return
		while True:
			x = randint(0, 9)
			y = randint(0, 9)
			if not self.player_board.get_space(Vector2(x, y)).hit:
				self.player_board.get_space(Vector2(x, y)).try_hit()
				break
		self.check_wins()

	def get_opposite_view(self):
		"""Returns the opposite to the board you are currently viewing"""
		if self.viewing == "player":
			return "cpu"
		else:
			return "player"

	def check_wins(self):
		"""Checks to see if either board has been cleared of all ships"""
		if self.cpu_board.board_cleared():
			self.game_won = True
			self.winner = "player"
		elif self.player_board.board_cleared():
			self.game_won = True
			self.winner = "cpu"

	def get_current_board(self):
		"""Returns the board you are currently viewing"""
		if self.viewing == "player":
			return self.player_board
		return self.cpu_board

	def draw_other_board(self):
		"""Draws the smaller board that you are not viewing in the bottom right corner"""
		board = self.cpu_board
		if self.viewing == "cpu":
			board = self.player_board
		square_size = int(32 * self.multiplier)
		pos = Vector2(1920 * self.multiplier - square_size * 11, 1080 - square_size * 11)
		ogp = Vector2(1920 * self.multiplier - square_size * 11, 1080 - square_size * 11)
		for x in range(10):
			for y in range(10):
				pygame.draw.rect(self.screen, (0,0,255), (pos.x, pos.y, square_size, square_size), 1)
				pos.y += square_size
			pos.y = ogp.y
			pos.x += square_size
		pos.x = ogp.x
		pos.y = ogp.y
		if self.viewing == "cpu":
			padding = 3 * self.multiplier
			for s in self.ships_to_set:
				if not s.placed:
					continue
				p = Vector2(s.position.x * square_size + ogp.x, s.position.y * square_size + ogp.y)
				sz = s.size * square_size
				if s.orientation == "h":
					if s.direction == 1:
						pygame.draw.rect(self.screen, (128, 128, 128), (p.x + padding, p.y + padding, sz - padding * 2, square_size - padding * 2))
					else:
						pygame.draw.rect(self.screen, (128, 128, 128), (p.x - sz + square_size + padding, p.y + padding, sz - padding * 2, square_size - padding * 2))
				elif s.orientation == "v":
					if s.direction == 1:
						pygame.draw.rect(self.screen, (128, 128, 128), (p.x + padding, p.y + padding, square_size - padding * 2, sz - padding * 2))
					else:
						pygame.draw.rect(self.screen, (128, 128, 128), (p.x + padding, p.y - sz + square_size + padding, square_size - padding * 2, sz - padding * 2))

		for x in range(10):
			for y in range(10):
				space = board.get_space(Vector2(x,y))
				if space.hit:
					if space.has_ship:
						self.hit_symbol_small.draw(self.screen, pos)
					else:
						pygame.draw.circle(self.screen, (255,255,255), (pos.x + square_size * 0.5, pos.y + square_size * 0.5), self.multiplier * 4)
				pos.y += square_size
			pos.y = ogp.y
			pos.x += square_size

	def draw_ships(self, grid_size):
		"""Iterates through all of the ships and draws them to the screen"""
		if self.viewing != "player":
			return
		pt = Vector2(960 * self.multiplier - (grid_size * 5.2 * self.multiplier), 540 * self.multiplier - (grid_size * self.multiplier * 4.7))
		for s in self.ships_to_set:
			if not s.placed:
				continue
			p = Vector2(s.position.x * self.multiplier * grid_size + pt.x, s.position.y * grid_size * self.multiplier + pt.y)
			sz = s.size * grid_size * self.multiplier
			padding = 8 * self.multiplier
			if s.orientation == "h":
				if s.direction == 1:
					pygame.draw.rect(self.screen, (128, 128, 128), (p.x + padding, p.y + padding, sz - padding * 2, grid_size * self.multiplier - padding * 2))
				else:
					pygame.draw.rect(self.screen, (128, 128, 128), (p.x - sz + grid_size * self.multiplier + padding, p.y + padding, sz - padding * 2, grid_size * self.multiplier - padding * 2))
			elif s.orientation == "v":
				if s.direction == 1:
					pygame.draw.rect(self.screen, (128, 128, 128), (p.x + padding, p.y + padding, grid_size * self.multiplier - padding * 2, sz - padding * 2))
				else:
					pygame.draw.rect(self.screen, (128, 128, 128), (p.x + padding, p.y - sz + grid_size * self.multiplier + padding, grid_size * self.multiplier - padding * 2, sz - padding * 2))

	def draw_hits(self, grid_size):
		"""Draws all of the hits and misses on the player's board"""
		pt = Vector2(960 * self.multiplier - (grid_size * 5.2 * self.multiplier), 540 * self.multiplier - (grid_size * self.multiplier * 4.7))
		pos = Vector2(960 * self.multiplier - (grid_size * 5.2 * self.multiplier), 540 * self.multiplier - (grid_size * self.multiplier * 4.7))
		for x in range(10):
			for y in range(10):
				space = self.get_current_board().get_space(Vector2(x, y))
				if space.hit:
					if not space.has_ship:
						pygame.draw.circle(self.screen, (255,255,255), (pos.x + grid_size * 0.5 * self.multiplier, pos.y + grid_size * 0.5 * self.multiplier), self.multiplier * 8)
					else:
						self.hit_symbol.draw(self.screen, pos)
				self.selector.draw(self.screen, Vector2(self.mouse_over_pos.x * grid_size * self.multiplier + pt.x, self.mouse_over_pos.y * grid_size * self.multiplier + pt.y))
				pos.y += grid_size * self.multiplier
			pos.x += grid_size * self.multiplier
			pos.y = 540 * self.multiplier - (grid_size * self.multiplier * 4.7)

	def draw_errors(self):
		"""Displays any errors or messages to the screen"""
		if self.has_error:
			alf = 255
			if time() - self.error_time > 0.75:
				lft = 2 - (time() - self.error_time)
				alf = lft * 255
			self.draw_text(self.current_error, Vector2(0, 476 * self.multiplier), color=(255,255,255), center=Vector2(1920 * self.multiplier, 128 * self.multiplier), alpha=alf)

	def DEBUG_PLACE_SHIP(self):
		"""FOR DEBUG ONLY. Automatically places the player's ships to save time"""
		self.auto_place_ships(True)

	def auto_place_ships(self, is_player):
		"""Picks random valid positions to place the ships at"""
		ind = 0
		while ind < 5:
			d = 1
			if randint(0, 1) == 0:
				d = -1
			o = "h"
			if randint(0, 1) == 0:
				o = "v"
			pos = Vector2(randint(0, 9), randint(0, 9))
			if is_player:
				works = self.player_board.set_ship(self.ships_to_set[ind], pos, o, d)
				if works:
					self.ships_to_set[ind].placed = True
					self.ships_to_set[ind].set_pos(pos, o, d)
					ind += 1
			else:
				works = self.cpu_board.set_ship(self.ships_to_set[ind], pos, o, d)
				if works:
					ind += 1
		if is_player:
			self.setting_ships = False
			self.viewing = "cpu"

	def hit_space(self, position=Vector2()):
		"""Attempts to hit the space at the given position"""
		if self.game_won:
			return
		if self.setting_ships:
			space = self.player_board.get_space(position)
			if self.selected_ship_index != -1:
				works = self.player_board.set_ship(self.ships_to_set[self.selected_ship_index], position, self.orientation, self.direction)
				if not works:
					self.display_error("You cannot place your ship here!")
				else:
					self.ships_to_set[self.selected_ship_index].placed = True
					self.ships_to_set[self.selected_ship_index].set_pos(position, self.orientation, self.direction)
					self.selected_ship_index = -1
					self.orientation = "h"
					self.direction = 1
					placed_all = True
					for ship in self.ships_to_set:
						if not ship.placed:
							placed_all = False
					self.setting_ships = not placed_all
					if not self.setting_ships:
						self.viewing = "cpu"
			else:
				self.display_error("Please select a ship first!")
		else:
			if self.viewing == "player":
				self.display_error("You cannot attack on your own board!")
				return
			space = self.cpu_board.get_space(position)
			if space.hit:
				self.display_error("You have already hit this spot!")
			else:
				response = space.try_hit()
				self.cpu_turn()

	def display_error(self, error):
		"""Called whenever you want to display an error"""
		self.current_error = error
		self.error_time = time()
		self.has_error = True

	def manage_events(self):
		"""Loops through all of PyGame's events and manages them"""
		exit_loop = False
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit_loop = True
				break
			elif event.type == pygame.KEYDOWN:
				if pygame.key.name(event.key) == "q":
					exit_loop = True
					break
				elif pygame.key.name(event.key) == "r":
					if self.orientation == "h":
						self.orientation = "v"
						self.direction *= -1
					else:
						self.orientation = "h"
			elif event.type == pygame.MOUSEBUTTONDOWN:
				self.mouse_down = True
				self.unmanaged_click = True
			elif event.type == pygame.MOUSEBUTTONUP:
				self.mouse_down = False
				self.unmanaged_click = False
		return exit_loop

	def draw_text(self, text="", position=Vector2(), color=(0,0,0), text_shadow=True, font=None, vertical_center=None, center=None, horizontal_center=None, alpha=256):
		"""Draws text to the screen based on the provided parameters"""
		if font == None:
			font = self.font

		draw_position = Vector2(position.x, position.y)
		if vertical_center != None:
			h = self.measure_text(text, font).y
			draw_position.y = (position.y + vertical_center.y * 0.5) - h * 0.5
		if horizontal_center != None:
			w = self.measure_text(text, font).y
			draw_position.x -= (w * 0.5)
		if center != None:
			w = self.measure_text(text, font).x
			h = self.measure_text(text, font).y
			draw_position = Vector2((position.x + center.x * 0.5) - w * 0.5, (position.y + center.y * 0.5) - h * 0.5)
		if alpha == 256:
			if text_shadow:
				text_surface = font.render(text, True, (0,0,0))
				self.screen.blit(text_surface, (draw_position.x + self.multiplier * 4, draw_position.y + self.multiplier * 4))
			text_surface = font.render(text, True, color)
			self.screen.blit(text_surface, draw_position.tuple())
		else:
			if text_shadow:
				text_surface = font.render(text, True, (0,0,0))
				text_surface.set_alpha(alpha)
				self.screen.blit(text_surface, (draw_position.x + self.multiplier * 4, draw_position.y + self.multiplier * 4))
			text_surface = font.render(text, True, color)
			text_surface.set_alpha(alpha)
			self.screen.blit(text_surface, draw_position.tuple())

	def manage_event(self, event_name, arg=None):
		"""Manages a provided event, used mainly for button clicks"""
		if event_name == None:
			return
		if event_name == "quit":
			self.running = False
		elif event_name == "singleplayer":
			self.change_menu("game")
			self.game_type = "singleplayer"
		elif event_name == "multiplier":
			self.change_menu("game")
			self.game_type = "multiplier"
		else:
			print("Unavailible event command:  '" + event_name + "', with the argument:  '" + str(arg) + "'")

	def measure_text(self, text, font=None):
		"""Returns the size (in pixels) of the provided text"""
		if font == None:
			font = self.font
		if font == self.massive_font:
			print("YES")
		text_width, text_height = self.font.size(text)
		return Vector2(text_width, text_height)

	def collides(self, x, y, r, b, x2, y2, r2, b2):
		return not (r <= x2 or x > r2 or b <= y2 or y > b2);

	def box_collides(self, pos, pos2, size1, size2):
		"""Returns true if two boxes collide"""
		return self.collides(pos.x, pos.y,
			pos.x + size1.x, pos.y + size1.y,
			pos2.x, pos2.y,
			pos2.x + size2.x, pos2.y + size2.y);
