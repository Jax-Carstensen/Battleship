from time import time
import json
from os import listdir
from os.path import isfile, join

#These 2 libraries are for installing other libraries
from subprocess import run
from sys import executable

print("Loading libraries. . . Please wait")

run([executable, "-m", "pip", "-q", "install", "pygame"])

import pygame