import pgzero, pgzrun, pygame
import math, sys, random
from myactors import Player, Monster, Bat, Weapon, Knife, Lion , Totem , Homing , Powerup , Health , Shield , Double_XP , Fast_attacks
from constants import *
from pygame.math import Vector2
from enum import Enum
from pgzero.builtins import Actor, keyboard, keys
class Game:
    def __init__(self):
        self.player = Player(HALF_LEVEL_W, HALF_LEVEL_H)
        self.monster = []
        self.powerups = []
        self.weapon = []
        ## gamestate values correspond to: stronger attack toggle, faster attack toggle, xp pup toggle, shield toggle
        ## self.gamestate = [0,0,0,0]
        self.timer = 0
        self.gametime = 0
        self.wave = 0
        self.seconds = 0


        
    
    def draw(self,screen):
      offset_x = max(0, min(LEVEL_W - WIDTH, self.player.vposx - WIDTH / 2))
      offset_y = max(0, min(LEVEL_H - HEIGHT, self.player.vposy - HEIGHT / 2))
      offset = Vector2(offset_x, offset_y)
      # if self.wave = even:
      if self.wave % 2 == 0:
        screen.blit("grassday2", (-offset_x, -offset_y))
      else:
        # different map for time of day change. 
        screen.blit("grass-day", (-offset_x, -offset_y))

      hp_bar = int(self.player.health / 10)
      Xpbar = int(((self.player.xp / self.player.xp_required) * 100))
      
      self.player.draw(offset_x, offset_y)
      hp_status = "hp-" + str(hp_bar)
      screen.blit(hp_status, ((self.player.x - 10), (self.player.y - 10)))
      xp_status = "xpbar_" + str(round(Xpbar*0.2))
      screen.blit(xp_status, (0, 0))
      #print(round(Xpbar*0.2))
      for mob in self.monster:
        mob.draw(offset_x, offset_y)

      for mob in self.weapon:
        mob.draw(offset_x, offset_y)

      for mob in self.powerups:
        mob.draw(offset_x, offset_y)

      #time = str(self.wave) + ":" + str(self.seconds)
      #imgmins = "digit1" + str(self.wave)
      #screen.blit(imgmins, (0, 0))
      #for i in 


    
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
      self.player.update()
      ## powerup timers are reduced if they are activated, this occurs for each powerup.
      if self.player.shield == True:
        self.player.shield_timer -= 1
      if self.player.double_xp == True:
        self.player.double_xp_timer -= 1
      if self.player.fast_attacks == True:
        self.player.fast_attacks_timer -= 1
      
      ## hp_bar = self.player.health / 10
      ## print(hp_bar)
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
        
        if self.player.fast_attacks == True:
          closestmob = self.findClosest(self.monster, self.player.vposx, self.player.vposy)
          self.weapon.append(Knife(self.player.vposx, self.player.vposy))
          if closestmob:
            self.weapon.append(Homing(self.player.vposx, self.player.vposy, closestmob))
        else:
          pass
      
      if (self.gametime == 20):
        
        closestmob = self.findClosest(self.monster, self.player.vposx, self.player.vposy)
        
        if len(self.monster) < 125:
          self.monster.append(Bat(self.screencoords(), self.wave))
        
        self.weapon.append(Knife(self.player.vposx, self.player.vposy))
        if closestmob:
          self.weapon.append(Homing(self.player.vposx, self.player.vposy, closestmob))      
      ## checks to see if each mob has died and if so, remove it.
      if self.gametime == 40:
        if len(self.monster) < 125:
          self.monster.append(Totem(self.screencoords(), self.wave))
      if self.gametime == 59:
        Pup = [Health, Shield, Double_XP, Fast_attacks]
        self.powerups.append(random.choice(Pup)())
        if len(self.monster) < 125:
          self.monster.append(Lion(self.screencoords(), self.wave))
      ##
      ##
      ##
      for mob in self.monster:
        
        mob.update(self.player, self.weapon)
        if (not mob.alive):
          self.monster.remove(mob)     # checks to see if each weapon has died and if so, remove it.
      for knife in self.weapon:
        knife.update()
        if (not knife.alive):
          self.weapon.remove(knife)
      
      for pup in self.powerups:
        pup.update(self.player)
        if (not pup.alive):
          self.powerups.remove(pup)
##
##
##
    def screencoords(self):
      left = int(max(0, min(LEVEL_W - WIDTH, self.player.vposx - WIDTH / 2)))
      top = int(max(0, min(LEVEL_H - HEIGHT, self.player.vposy - HEIGHT / 2)))
      right = int(max(0, min(LEVEL_W + WIDTH, self.player.vposx + WIDTH / 2)))
      bottom = int(max(0, min(LEVEL_H + HEIGHT, self.player.vposy + HEIGHT / 2)))
      coords = [left, top, right, bottom]          
      return coords


