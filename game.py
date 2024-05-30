import pgzero, pgzrun, pygame
import math, sys, random
from myactors import Player, Monster, Bat, Weapon, Knife, Armor , Princess , Homing , Powerup , Health , Shield , Double_XP , Fast_attacks , Homing_weapon
from constants import *
from pygame.math import Vector2
from enum import Enum
from pgzero.builtins import Actor, keyboard, keys
class Game:
    def __init__(self):
        ## spawn player in the middle of the screen
        self.player = Player(HALF_LEVEL_W, HALF_LEVEL_H)
        ## activate lists for each of the entities (except for player)
        self.monster = []
        self.powerups = []
        self.weapon = []

        ## declaring variables for the time in game, gametime counts each tick and adds to seconds, seconds adds to waves.
        self.timer = 0
        self.gametime = 0
        self.wave = 0
        self.seconds = 0
        self.night = False
    
    def draw(self,screen):
      offset_x = max(0, min(LEVEL_W - WIDTH, self.player.vposx - WIDTH / 2))
      offset_y = max(0, min(LEVEL_H - HEIGHT, self.player.vposy - HEIGHT / 2))
      offset = Vector2(offset_x, offset_y)
      # if day, use day sprite and vice versa
      if self.wave % 2 == 0:
        screen.blit("grass-day", (-offset_x, -offset_y))
      else:
        screen.blit("grass-night", (-offset_x, -offset_y))
      ## hp and xp bar images are selected based on the percentage of players health and percentage of progress to the next level
      hp_bar = int(self.player.health / 10)
      Xpbar = int(((self.player.xp / self.player.xp_required) * 100))
      ## show player with shield sprite if the shield powerup is active
      if self.player.shield == True:
        self.player.myimg = "playershield"
      else:
        self.player.myimg = "player"

      
      ## draw player according to which sprite is selected beforehand
      self.player.draw(offset_x, offset_y)

      ## draw hp bar above player, updated based on the proportion of the hp that is filled
      hp_status = "hp-" + str(hp_bar)
      screen.blit(hp_status, ((self.player.x - 10), (self.player.y - 10)))
      ## draw xp bar on the bottom of the screen, Xpbar variable is the percentage of the bar that is filled split into 20, as there are 20 images for the bar
      xp_status = "xpbar_" + str(round(Xpbar*0.2))
      screen.blit(xp_status, (0, 465))
      #print(round(Xpbar*0.2)) -- TESTING
      ## draw each item in the list of monsters, powerups and attacks that are on screen
      for mob in self.monster:
        mob.draw(offset_x, offset_y)
      for attack in self.weapon:
        attack.draw(offset_x, offset_y)
      for powerup in self.powerups:
        powerup.draw(offset_x, offset_y)

    # find the closest mob to the given x and y values, pass in the list of monsters
    def findClosest(self, moblist, x, y):
      closest = WIDTH
      closestmob= ""
      for mob in moblist:
        mob.distance = math.sqrt(((x - mob.vposx) ** 2) + ((y - mob.vposy) ** 2))
        if mob.distance < closest:
          closest = mob.distance
          closestmob = mob
      return closestmob
    

    # updates will only happen when the game is NOT in the pause state which is triggered every time the player levels up and can upgrade or acquire a weapon. 
    def update(self):
      # if self.wave = even set night to false and vice versa
      if self.wave % 2 == 0:
        self.night == False
      else:self.night == True
      self.player.update()
      ## pup is used to select a random powerup to spawn from this list
      Pup = [Health, Shield, Double_XP, Fast_attacks , Homing_weapon]
      ## powerup timers are reduced if they are activated, this occurs for each powerup.
      ## once homing upgrade is purchased the homing weapon timer stops 
      if self.player.shield == True:
        self.player.shield_timer -= 1
      if self.player.double_xp == True:
        self.player.double_xp_timer -= 1
      if self.player.fast_attacks == True:
        self.player.fast_attacks_timer -= 1
      if self.player.homing_weapon == True:
        if self.player.homing_flag == False:
          self.player.homing_weapon_timer -= 1
      ## closest mob gets the list of monsters to compare each monsters position to the players position
      closestmob = self.findClosest(self.monster, self.player.vposx, self.player.vposy)
      ## timer for internal stuff and second timer to count seconds
      self.timer += 1
      self.gametime += 1
      ## each time a second passes add one to the counter and begin counting again
      if (self.gametime == 60): 
        self.seconds += 1 
        self.gametime = 0 
      ## every minute add one to wave.
      if (self.seconds == 60):
        self.seconds = 0 
        self.wave += 1 
## each time the timer hits 20 a new monster is added to self.monster, i.e another monster is spawned
## pass in wave value to monsters to spawn powered up mobs.
      if (self.timer == 20):
        self.timer = 0
        ## if fast attacks is active, spawn additional weapon instances
        if self.player.fast_attacks == True:
          self.weapon.append(Knife(self.player.vposx, self.player.vposy))
        if closestmob and self.player.homing_flag == True:
            self.weapon.append(Homing(self.player.vposx, self.player.vposy, closestmob))
        if closestmob and self.player.homing_weapon == True:
          self.weapon.append(Homing(self.player.vposx, self.player.vposy, closestmob))
        else:
          pass
      ## dependind on weapon fire rate and if homing powerup is active spawn weapon instances
      if (self.timer == 10):
        if self.player.upgrade_weapon >= 2:
          self.weapon.append(Knife(self.player.vposx, self.player.vposy))
          if closestmob and self.player.homing_flag == True:
            self.weapon.append(Homing(self.player.vposx, self.player.vposy, closestmob))
      ## depending on if homing powerup is active spawn weapon instances
      if (self.gametime == 20):
        self.weapon.append(Knife(self.player.vposx, self.player.vposy))
        if closestmob and self.player.homing_flag == True:
          self.weapon.append(Homing(self.player.vposx, self.player.vposy, closestmob))
        if closestmob and self.player.homing_weapon == True:
          self.weapon.append(Homing(self.player.vposx, self.player.vposy, closestmob))   
      ## spawn new bat mob depending if there are too many monsters 
        if self.night == False:
          if len(self.monster) < 50:
            self.monster.append(Bat(self.screencoords(), self.wave))
          else:
            if len(self.monster) < 75:
              self.monster.append(Bat(self.screencoords(), self.wave))
        
      ## conditionally add weapon instances and add a powerup if more powerups upgrade is active
      if self.gametime == 40:
        if self.player.upgrade_self >= 2:
          self.powerups.append(random.choice(Pup)())
        ## add evil princess and armor mobs depening on day/night state
        if self.night == False:
          if len(self.monster) < 50:
            self.monster.append(Princess(self.screencoords(), self.wave))
          else:
            self.monster.append(Princess(self.screencoords(), self.wave))
            self.monster.append(Armor(self.screencoords(), self.wave))
      if self.gametime == 59:
        ## always add powerup and armor mob
        self.powerups.append(random.choice(Pup)())
        if len(self.monster) < 50:
          self.monster.append(Armor(self.screencoords(), self.wave))
      
      
      ## check if each entity had died and if so, remove them
      for mob in self.monster: 
        mob.update(self.player, self.weapon)
        if (not mob.alive):
          self.monster.remove(mob)     
      for knife in self.weapon:
        knife.update()
        if (not knife.alive):
          self.weapon.remove(knife)
      for pup in self.powerups:
        pup.update(self.player)
        if (not pup.alive):
          self.powerups.remove(pup)
## defining screencoords value for spawning entities
    def screencoords(self):
      left = int(max(0, min(LEVEL_W - WIDTH, self.player.vposx - WIDTH / 2)))
      top = int(max(0, min(LEVEL_H - HEIGHT, self.player.vposy - HEIGHT / 2)))
      right = int(max(0, min(LEVEL_W + WIDTH, self.player.vposx + WIDTH / 2)))
      bottom = int(max(0, min(LEVEL_H + HEIGHT, self.player.vposy + HEIGHT / 2)))
      coords = [left, top, right, bottom]          
      return coords


