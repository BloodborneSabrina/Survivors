import pgzero, pgzrun, pygame
import math, sys, random
from enum import Enum
from game import Game
from constants import *

if sys.version_info < (3,5):
    print("This game requires at least version 3.5 of Python. Please download it from www.python.org")
    sys.exit()

pgzero_version = [int(s) if s.isnumeric() else s for s in pgzero.__version__.split('.')]
if pgzero_version < [1,2]:
    print("This game requires at least version 1.2 of Pygame Zero. You have version {0}. Please upgrade using the command 'pip3 install --upgrade pgzero'".format(pgzero.__version__))
    sys.exit()
def update():
    game.update()
def draw():
    game.draw(screen)


game = Game()
pgzrun.go()