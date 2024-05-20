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
        ## print("menu")
        
        if space_pressed:
        ## Switch to play state, and create a new Game object, passing it the controls function for
        ## player 1, and if we're in 2 player mode, the controls function for player 2 (otherwise the
        ## 'None' value indicating this player should be computer-controlled)a
            state = State.PLAY
            
    elif state == State.PLAY:
        ## when player health hits 0 trigger game over state.
        if game.player.health <= 0:
            state = State.GAME_OVER
        ## when the player levels up trigger the pause state.
        if game.player.leveluptrigger == True:
            game.player.leveluptrigger = False
        ## print("level up trigger")
            state = State.PAUSED
        else:
            game.update()

    elif state == State.PAUSED:
    ## print("pausa")
    ## if space_pressed:
    ## Reset to menu state
    ## state = State.PLAY

        ## depending on the upgrade selected increase the upgrade value and return to normal gameplay, if all upgrades are unlocked, they must choose the other upgrade.
        if keyboard.K_1:
            if game.player.upgrade_self <= 3:
                game.player.upgrade_self += 1
                state = State.PLAY
            else:
                pass
        
        if keyboard.K_2:
            if game.player.upgrade_weapon <= 3:
                game.player.upgrade_weapon += 1
                state = State.PLAY
            else:
                pass




    elif state == State.GAME_OVER:
        if space_pressed:
    ## Reset to menu state
            state = State.MENU
            game = Game()
def draw():
    game.draw(screen)
    if state == state.PLAY:
        screen.draw.text((str(game.wave) + ":" + str(game.seconds)), ((HALF_WINDOW_W - 30), 10), fontsize=32)
    if state == State.MENU:
    ## menu_image = "menu" + str(num_players - 1)
        screen.blit("menu", (0,0))
    if state == State.PAUSED:
        screen.blit("upgrade_menu", (0,0))

        if game.player.upgrade_weapon == 0:
            screen.draw.text("Increase weapon damage", (456,258))
        elif game.player.upgrade_weapon == 1:
            screen.draw.text("Increase fire rate", (456,258))
        elif game.player.upgrade_weapon == 2:
            screen.draw.text("Increase weapon damage", (456,258))
        elif game.player.upgrade_weapon == 3:
            screen.draw.text("Add homing weapon permanently", (456,258))
        elif game.player.upgrade_weapon == 4:
            screen.draw.text("all upgrades earned", (456,258))

        if game.player.upgrade_self == 0:
            screen.draw.text("Increase player speed", (56,258))
        elif game.player.upgrade_self == 1:
            screen.draw.text("Increase powerup spawn rate", (56,258))
        elif game.player.upgrade_self == 2:
            screen.draw.text("Further Increase player speed", (56,258))
        elif game.player.upgrade_self == 3:
            screen.draw.text("Increase duration of powerups", (56,258))
        elif game.player.upgrade_self == 4:
            screen.draw.text("All upgrades earned", (56,258))

    elif state == State.GAME_OVER: 
        screen.blit("game_over", (0,0))

state = State.MENU
game = Game()
pgzrun.go()