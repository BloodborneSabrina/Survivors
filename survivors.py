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
    ## define what the state numeric values correspond to and spacebar trigger.
    MENU = 1
    PLAY = 2
    GAME_OVER = 3
    PAUSED = 4
    space_down = False
    
    
def update():
    ## define game state variable and checks to preven erroneus space presses.
    global state, game, space_down
    space_pressed = False 

    ## check when space has been released and then trigger the space pressed value.
    if keyboard.space and not space_down:
        space_pressed = True
    space_down = keyboard.space
    
    ## if the game is in the Main menu state;
    if state == State.MENU:
        # print("menu") (TESTING)
        ## when the player hits space to progress;
        if space_pressed:
        ## Switch to play state, and create a new game.
            state = State.PLAY
            
    elif state == State.PLAY:
        ## when player health hits 0 trigger game over state.
        if game.player.health <= 0:
            state = State.GAME_OVER
        ## when the player levels up trigger the paused state.
        if game.player.leveluptrigger == True:
            ## reset the level up trigger to allow the next level up
            game.player.leveluptrigger = False
        # print("level up trigger") (TESTING)
            state = State.PAUSED
        else:
            game.update()

    elif state == State.PAUSED:
    ## print("paused") (TESTING)

        ## depending on the upgrade selected increase the upgrade value and return to normal gameplay, if all upgrades are unlocked, they must choose the other upgrade.
        if keyboard.K_1:
            if game.player.upgrade_self <= 3:
                game.player.upgrade_self += 1
                state = State.PLAY
            ## pass makes it so that they can no longer select the upgrade
            else:
                pass
        
        if keyboard.K_2:
            if game.player.upgrade_weapon <= 3:
                game.player.upgrade_weapon += 1
                state = State.PLAY
            else:
                pass



    ## when in game over state
    elif state == State.GAME_OVER:
        if space_pressed:
    ## Reset to menu state
            state = State.MENU
    ## resets the game.
            game = Game()
## draw function here handles the menus
def draw():
    ## this draw handles all the entities coming from game.py
    game.draw(screen)
    ## while the game is active display the timer at the top of the screen
    if state == state.PLAY:
        screen.draw.text((str(game.wave) + ":" + str(game.seconds)), ((HALF_WINDOW_W - 30), 10), fontsize=32)
    ## display the main menu in menu state
    if state == State.MENU:
        screen.blit("menu", (0,0))
    ## display the upgrade screen while the game is paused
    if state == State.PAUSED:
        screen.blit("upgrade_menu", (0,0))
    ## add upgrade descriptions for the player and weapon upgrades over the top of the upgrade menu sprite.
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
    ## in game over state show game over screen
    elif state == State.GAME_OVER: 
        screen.blit("game_over", (0,0))

state = State.MENU
game = Game()
pgzrun.go()