if __name__ == '__main__':
	from game import *
	from time import time
	import json
	from os import listdir
	from os.path import isfile, join

	game = Game()
	game.start()