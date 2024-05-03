import pgzero, pgzrun, pygame
import math, sys, random
from enum import Enum
from game import Game
from constants import *
from pgzero.builtins import Actor, keyboard, keys

if sys.version_info < (3,5):
    print("This game requires at least version 3.5 of Python. Please download it from www.python.org")
    sys.exit()

pgzero_version = [int(s) if s.isnumeric() else s for s in pgzero.__version__.split('.')]
if pgzero_version < [1,2]:
    print("This game requires at least version 1.2 of Pygame Zero. You have version {0}. Please upgrade using the command 'pip3 install --upgrade pgzero'".format(pgzero.__version__))
    sys.exit()

class State(Enum):
    MENU = 1
    PLAY = 2
    GAME_OVER = 3
    PAUSED = 4
    space_down = False
    
    
def update():
    global state, game, space_down
    space_pressed = False 
    if keyboard.space and not space_down:
        space_pressed = True
    space_down = keyboard.space
    
    
    if state == State.MENU:
        print("menu")
        
        if space_pressed:
            # Switch to play state, and create a new Game object, passing it the controls function for
            # player 1, and if we're in 2 player mode, the controls function for player 2 (otherwise the
            # 'None' value indicating this player should be computer-controlled)
            
            
            state = State.PLAY
            
    elif state == State.PLAY:
        # Has anyone won?
        
        if game.player.health == 0:
            state = State.GAME_OVER
        #if game.player.leveluptrigger == True:
            #state = State.PAUSED
        else:
            game.update()

        
        

    elif state == State.GAME_OVER:
        if space_pressed:
            # Reset to menu state
            state = State.MENU
            game = Game()
def draw():
    game.draw(screen)
    if state == State.MENU:
        #menu_image = "menu" + str(num_players - 1)
        screen.blit("menu", (0,0))

    elif state == State.GAME_OVER:
        screen.blit("over", (0,0))


state = State.MENU
game = Game()
pgzrun.go()