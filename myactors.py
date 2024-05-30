from pgzero.builtins import Actor, keyboard, keys
import math, sys, random
from constants import *

## global damage variable used by player and monsters (corresponds to how much damage weapons will do)

class MyActor(Actor):
  def __init__(self,img,x,y,speed):
    self.myimg = img
    self.imgno = 1
    myimg = f'{self.myimg}_{self.imgno}'
    super().__init__(myimg, (x,y))    
    self.vposx, self.vposy = x, y
    self.dx, self.dy = 0, 0
    self.speed = speed
    self.timer = 0    
    self.olddx = -100
    self.olddirection = -100
    self.state = 1,1,1
  def update(self):

    self.timer += 1

    if (self.dx < 0): 
      direction = 4
    elif (self.dx == 0): 
      if (self.dy < 0):
        direction = 10
      elif (self.dy >= 0):
        direction = 1            
    else:
      direction = 7
  ## if direction has changed, reset the animation cycle.
    if (self.olddirection != direction):
      self.imgno = direction
  ## every 10 ticks, add one to image number if direction is the same, or if the last image is reached afterwards go back to the first image.
    if (self.timer==10):
      self.timer = 0
      if (self.olddirection == direction):
        self.imgno +=1
        if ((self.imgno==4) or (self.imgno==7) or (self.imgno==10) or (self.imgno==13)):
          self.imgno -= 3   
    ## use image number and myimg value to create final image, which is then used by the draw function in game.py
    self.image = f'{self.myimg}_{self.imgno}'
    ## defining direction variables for calculating movement.
    self.olddx = self.dx
    self.olddirection = direction

    # Return vector representing amount of movement that should occur
    self.dx = self.dx * self.speed
    self.dy = self.dy * self.speed
    ## define vpos value (x and y values in relation to the rendered area)
    self.vposx += self.dx
    self.vposx = max(0+PLAYER_W,min(self.vposx, LEVEL_W-PLAYER_W))    
    self.vposy += self.dy
    self.vposy = max(0+PLAYER_H,min(self.vposy, LEVEL_H-PLAYER_H))

  ## define draw position 
  def draw(self, offset_x, offset_y):
    self.pos = (self.vposx - offset_x, self.vposy - offset_y)
    super().draw()

class Player(MyActor):
  def __init__(self, x, y):
    ## declaring players properties.
    self.img = "player"
    self.health = 100
    self.leveluptrigger = False
    self.xp = 0
    self.level = 0
    self.xp_required = 400
    self.upgrade_self = 0
    self.upgrade_weapon = 0
    self.damage= 5
    self.homing_flag = False
    self.speed = 4
    #declaring variables for each powerup to access
    self.shield_timer = 0 
    self.shield = False
    self.double_xp = False
    self.double_xp_timer = 0
    self.fast_attacks = False
    self.fast_attacks_timer = 0
    self.homing_weapon = False
    self.homing_weapon_timer = 0

    super().__init__(self.img,x,y,self.speed)

  
  def update(self):
    # Return vector representing amount of movement that should occur
    # self.timer -= 1 (TESTING)

    ## change player speed depending on upgrades
    if self.upgrade_self >= 1:
      self.speed = 5
    if self.upgrade_self >= 3:
      self.speed = 7
    ## increase player damage depending on upgrades
    if self.upgrade_weapon >= 1:
      self.damage = 7
    if self.upgrade_weapon >= 3:
      self.damage = 10
    ## if all weapon upgrades acquired, always have homing weapon active
    if self.upgrade_weapon >= 4:
      self.homing_flag = True
    
    ## if timers run out, deactivate powerups
    if self.shield_timer == 0:
      self.shield = False
    if self.fast_attacks_timer == 0:
      self.fast_attacks = False
    if self.homing_weapon_timer == 0:
      self.homing_weapon = False
      
    #print(self.damage) (TESTING)

    ## depending on keys pressed, set direction
    self.dx, self.dy = 0, 0
    if keyboard.a:
        self.dx = -1
    elif keyboard.d:
        self.dx = 1
    if keyboard.w:
        self.dy = -1
    elif keyboard.s:
        self.dy = 1
    #print(self.level) (TESTING)
    super().update()
  ## is used to process damage from mobs, reduces player health by amount passed in provided shield powerup is NOT active.
  def hurt(self,damage):
    if self.shield == False:
      self.health -= damage
  ## heals player to full, but no more than the max value (100)
  def heal (self,healing):
    self.health += healing
    if (self.health >= 100):
      self.health = 100
  ## if double xp is active double each gained xp amount.
  def experience(self, XP):
    if self.double_xp == True:
      self.xp += (XP * 2)
    else:
      self.xp += XP
    # print("xp=" + str(self.xp)) (TESTING)

    ## xp required to level up scales exponentially, when the required amount is reached the player level increases.
    ## once the level is reached the scaling kicks in and reallocates the required xp amount.
    if self.xp > self.xp_required:
      self.level += 1
      ## when the amount of xp required to level up is met
      self.xp_required = (self.xp_required * 1.5)
      self.xp = 0
      ## if all upgrades are acquired dont trigger upgrade screen, otherwise trigger pause state.
      if self.upgrade_self and self.upgrade_weapon == 4:
        pass
      else:
        self.leveluptrigger = True
      #print(self.xp_required) (TESTING)
      #print("lvl" + str(self.level)) (TESTING)
class Monster(MyActor):
  def __init__(self, img, posx, posy,spd):
    super().__init__(img, posx, posy, spd)
    self.invuln = False
    self.invuln_timer = 0
    self.alive = True
  
    #print(damage) (TESTING)

    
  def hurt(self,dmg):
      #print(self.health) (TESTING)
      ## if monster is vulnerable, reduce mob health by players damage amount
      if self.invuln == False:
        self.health -= dmg
        self.invuln = True
        self.invuln_timer = 10

  def update(self,player,weapon):
    super().update()   
    
    ## if mob collides with a weapon, mob is hurt. 
    if (self.collidelist(weapon)) != -1:
      self.hurt(player.damage)
      #self.alive = False
      #player.experience(25)
    ## handles invulnerability state after the mob is hurt
    if self.invuln == True:
        self.invuln_timer -= 1
    if self.invuln_timer == 0:
      self.invuln = False
    ## when the mob dies, reward the player with XP
    if (self.health<=0):
      self.alive = False
      player.experience(25)
    ## if mob touches player, hurt player by mobs damage value, otherwise if player shield is active, do nothing.
    if (self.colliderect(player)):
        player.hurt(self.damage)
        if player.shield == False:
          self.alive = False      

class Bat(Monster):
  def __init__(self, screencoords, wave):
    self.mode = wave
    ## set mob damage and health values when they are spawned, change the values depending on whether its day or night.
    ## if wave = even: (daytime)
    if self.mode % 2 == 0:
      self.damage = (5 + wave)
      self.health = (10 + wave)
      self.speed = (0.65 + wave * 0.1)
    else:
      self.damage = (9 + wave)
      self.health = (20 + wave)
      self.speed = (0.9 + wave * 0.1)

    LEFT = 0
    TOP = 1
    RIGHT = 2
    BOTTOM = 3

    side = random.randint(0,3)    
    
    if (side == LEFT):
      posx = max(screencoords[LEFT] - 50, 0)
      #max is used to ensure that enemy will be spawned at the edge of the screen if the screencoords to the left would be negative number.
      posy = random.randint(screencoords[TOP],screencoords[BOTTOM])   
      #above line chooses a random number in the range from the top of the screen to the bottom.   
    elif (side == TOP): 
      posx = random.randint(screencoords[LEFT],screencoords[RIGHT])
      posy = max(screencoords[TOP] - 50, 0)
    elif (side == RIGHT): 
      posx = min(screencoords[RIGHT] + 50, LEVEL_W)
      posy = random.randint(screencoords[TOP],screencoords[BOTTOM])
    elif (side == BOTTOM):
      posx = random.randint(screencoords[LEFT],screencoords[RIGHT])
      posy = min(screencoords[BOTTOM] + 50, LEVEL_H)

    super().__init__("bat", posx, posy, self.speed)
  

  def update(self,player,knife): 
    
    ## always move toward the players position.
    if (self.vposx > player.vposx):
      self.dx = -1
    elif (self.vposx < player.vposx):
      self.dx = 1
    else:
      self.dx = 0
    if (self.vposy > player.vposy):
      self.dy = -0.5
    elif (self.vposy < player.vposy):
      self.dy = 0.5
    else:
      self.dy = 0
    ## if mob is invulnerable, use the invincible version of the sprite
    if self.invuln == True:
      self.myimg = "bat_invuln"
    else:
      self.myimg = "bat"

    super().update(player,knife)   


class Armor(Monster):
  def __init__(self, screencoords, wave):
    self.mode = wave
    ## set mob damage and health values when they are spawned, change the values depending on whether its day or night.
    ## if wave = even: (daytime)
    if self.mode % 2 == 0:
      self.damage = (6 + wave)
      self.health = (8 + wave)
      self.speed = (1 + wave * 0.1)
    else:
      self.damage = (10 + wave)
      self.health = (13 + wave)
      self.speed = (1.4 + wave * 0.1)

    self.movementTimer = 0

    LEFT = 0
    TOP = 1
    RIGHT = 2
    BOTTOM = 3

    side = random.randint(0,3)    
    
    if (side == LEFT):
      posx = max(screencoords[LEFT] - 50, 0)
      #max is used to ensure that enemy will be spawned at the edge of the screen if the screencoords to the left would be negative number.
      posy = random.randint(screencoords[TOP],screencoords[BOTTOM])   
      #above line chooses a random number in the range from the top of the screen to the bottom.   
    elif (side == TOP): 
      posx = random.randint(screencoords[LEFT],screencoords[RIGHT])
      posy = max(screencoords[TOP] - 50, 0)
    elif (side == RIGHT): 
      posx = min(screencoords[RIGHT] + 50, LEVEL_W)
      posy = random.randint(screencoords[TOP],screencoords[BOTTOM])
    elif (side == BOTTOM):
      posx = random.randint(screencoords[LEFT],screencoords[RIGHT])
      posy = min(screencoords[BOTTOM] + 50, LEVEL_H)
    super().__init__("armor", posx, posy, self.speed)

  
      
  def update(self,player,knife): 
    #use a timer to make sure monster only moves at certain intervals.
    self.movementTimer += 1
    if self.movementTimer == 90:
      self.movementTimer = 0
    ## move only when movement timer allows this
    if self.movementTimer > 31:
      if (self.vposx > player.vposx):
        self.dx = -1
      elif (self.vposx < player.vposx):
        self.dx = 1
      else:
        self.dx = 0
      if (self.vposy > player.vposy):
        self.dy = -0.75
      elif (self.vposy < player.vposy):
        self.dy = 0.75
      else:
        self.dy = 0
    else:
    ## stand still for the remaining third of the time
      self.dy = 0
      self.dx = 0
    ## if mob is invulnerable, use the invincible version of the sprite
    if self.invuln == True:
      self.myimg = "armor_invuln"
    else:
      self.myimg = "armor"
    
    super().update(player,knife)  

class Princess(Monster):

  def __init__(self, screencoords, wave):
    self.mode = wave
    ## set mob damage and health values when they are spawned, change the values depending on whether its day or night.
    ## if wave = even: (daytime)
    if self.mode % 2 == 0:
      self.damage = (10 + wave)
      self.health = (10 + wave)
      self.speed = (1.5 + wave * 0.1)
    else:
      self.damage = (14 + wave)
      self.health = (20 + wave)
      self.speed = (2 + wave * 0.1)

    LEFT = 0
    TOP = 1
    RIGHT = 2
    BOTTOM = 3

    side = random.randint(0,3)    
    
    if (side == LEFT):
      posx = max(screencoords[LEFT] - 50, 0)
      #max is used to ensure that enemy will be spawned at the edge of the screen if the screencoords to the left would be negative number.
      posy = random.randint(screencoords[TOP],screencoords[BOTTOM])   
      #above line chooses a random number in the range from the top of the screen to the bottom.   
    elif (side == TOP): 
      posx = random.randint(screencoords[LEFT],screencoords[RIGHT])
      posy = max(screencoords[TOP] - 50, 0)
    elif (side == RIGHT): 
      posx = min(screencoords[RIGHT] + 50, LEVEL_W)
      posy = random.randint(screencoords[TOP],screencoords[BOTTOM])
    elif (side == BOTTOM):
      posx = random.randint(screencoords[LEFT],screencoords[RIGHT])
      posy = min(screencoords[BOTTOM] + 50, LEVEL_H)
    super().__init__("princess", posx, posy, self.speed)


  
  def update(self,player,knife): 
    
    ##distance from player = square root of ((x of object - x of player)squared + (y of object - y of player)squared)
    self.distance = math.sqrt(((self.vposx - player.vposx) ** 2) + ((self.vposy - player.vposy) ** 2))
    
    
    
    # if distance from the player is small enough the mob will move towards player.
    if self.mode % 2 == 0:
      # adjust distance value to choose how close the mob should be before it moves towards the player.
      if self.distance < 200:
        if (self.vposx > player.vposx):
          self.dx = -1
        elif (self.vposx < player.vposx):
          self.dx = 1
        else:
          self.dx = 0
        if (self.vposy > player.vposy):
          self.dy = -0.5
        elif (self.vposy < player.vposy):
          self.dy = 0.5
        else:
          self.dy = 0
      else:
        self.dy = 0
        self.dx = 0
    ## will start moving toward the player from further range at night
    else:
      # adjust distance value to choose how close the mob should be before it moves towards the player.
      if self.distance < 350:
        if (self.vposx > player.vposx):
          self.dx = -1
        elif (self.vposx < player.vposx):
          self.dx = 1
        else:
          self.dx = 0
        if (self.vposy > player.vposy):
          self.dy = -0.5
        elif (self.vposy < player.vposy):
          self.dy = 0.5
        else:
          self.dy = 0
      else:
        self.dy = 0
        self.dx = 0
    ## if mob is invulnerable, use the invincible version of the sprite
    if self.invuln == True:
      self.myimg = "princess_invuln"
    else:
      self.myimg = "princess"

    super().update(player,knife) 



class Weapon(MyActor):
  def __init__(self, img, posx, posy,spd):
    
    super().__init__(img, posx, posy, spd,)
    ## set alive value on spawn
    self.alive = True

  def update(self):
      
    super().update()   
    

class Knife(Weapon):
  
  ## x and y are the players coordinates, the weapon always spawns on the players position 
  def __init__(self, x, y):
    ## initialize with the direction that player is facing, at the players position. this fires out the projectile whichever way the player is going.
    if keyboard.a:
      self.dirx = -1
    elif keyboard.d:
      self.dirx = 1
    else:
      self.dirx = 0
    if keyboard.w:
      self.diry = -1
    elif keyboard.s:
      self.diry = 1
    elif self.dirx != 0:
      self.diry = 0
    else:
      self.diry = 1
    
    
    super().__init__("basic_pink", x, y, 10)
  ## adapted from player update code
  def update(self):
    ## direction does not change
    self.dx = self.dirx
    self.dy = self.diry

    ## Removes weapon instance once it reaches the edge of the map.
    if self.vposy < 26:
      self.alive = False
    if self.vposx > 979:
      self.alive = False
    if self.vposx < 21:
      self.alive = False
    if self.vposy > 974:
      self.alive = False
    
    super().update()

def findClosest(self, moblist, x, y):

      closest = WIDTH
      closestmob= ""
      for mob in moblist:
        mob.distance = math.sqrt(((x - mob.vposx) ** 2) + ((y - mob.vposy) ** 2))
        if mob.distance < closest:
          closest = mob.distance
          closestmob = mob
        else:
          pass
      return closestmob
class Homing(Weapon):
  
  ## x and y are the players coordinates, the weapon always spawns on the players position 
  def __init__(self, x, y, mob):
  
  ## mob value is passed in and represents the closest mob to the player, the weapon travels in the direction of this mob
    if x < mob.vposx:
      self.dirx = 1
    elif x > mob.vposx:
      self.dirx = -1
    else:
      self.dirx = 0

    if y < mob.vposy:
      self.diry = 1
    elif y > mob.vposy:
      self.diry = -1
    else:
      self.diry = 0
    
    super().__init__("basic_blue", x, y, 10)
  
  def update(self):
    ## Return vector representing amount of movement that should occur
    ## direction does not change
    self.dx = self.dirx
    self.dy = self.diry
    #removes weapon instance once it reaches the edge of the map.
    if self.vposy < 26:
      self.alive = False
    if self.vposx > 979:
      self.alive = False
    if self.vposx < 21:
      self.alive = False
    if self.vposy > 974:
      self.alive = False
    
    super().update()


## Powerup class will be used for XP and ofc powerups, similar to an enemy this will just check for collision and then dissapear if detected
class Powerup(MyActor):
  def __init__(self, img, posx, posy,spd):

    super().__init__(img, posx, posy, spd)
    ## set alive value on spawn
    self.alive = True

  def update(self, player):
    
    super().update()
    

class Health(Powerup):
  def __init__(self):
    ## spawns randomly within the level size
    x = random.randint(21,979)
    y = random.randint(26,975)
    super().__init__("powerup_green", x, y, 0)

  def update(self,player):
    ## when colliding with player,remove powerup instance and heal the player for 50
    if (self.colliderect(player)):
      player.heal(50)
      self.alive = False
      
    super().update(player)

class Shield(Powerup):
  def __init__(self):
    ## spawns randomly within the level size
    x = random.randint(21,979)
    y = random.randint(26,975)
    super().__init__("powerup_blue", x, y, 0)

  def update(self,player):
    ## when colliding with player,remove powerup instance and activate the shield state and add to timer depending on if duration upgrade is active
    if (self.colliderect(player)):
      if player.upgrade_self >= 4:
        player.shield_timer = 300
      player.shield_timer = 200
      player.shield = True
      self.alive = False
      
    super().update(player)

class Double_XP(Powerup):
  def __init__(self):
    ## spawns randomly within the level size
    x = random.randint(21,979)
    y = random.randint(26,975)
    super().__init__("powerup_yellow", x, y, 0)

  def update(self,player):
    ## when colliding with player,remove powerup instance and activate the double XP state and add to timer depending on if duration upgrade is active
    if (self.colliderect(player)):
      if player.upgrade_self >= 4:
        player.Double_XP_timer = 400
      player.Double_XP_timer = 200
      player.Double_XP = True
      self.alive = False
      
    super().update(player)

class Fast_attacks(Powerup):
  def __init__(self):
    ## spawns randomly within the level size
    x = random.randint(21,979)
    y = random.randint(26,975)
    super().__init__("powerup_red", x, y, 0)

  def update(self,player):
    ## when colliding with player, remove powerup instance and activate the fast attacks state and add to timer depending on if duration upgrade is active
    if (self.colliderect(player)):
      if player.upgrade_self >= 4:
        player.fast_attacks_timer = 400
      player.fast_attacks_timer = 200
      player.fast_attacks = True
      
      self.alive = False
      
    super().update(player)

class Homing_weapon(Powerup):
  def __init__(self):
    ## spawns randomly within the level size
    x = random.randint(21,979)
    y = random.randint(26,975)
    super().__init__("powerup_pink", x, y, 0)

  def update(self,player):
    ## when colliding with player,remove powerup instance and activate the homing weapon state and add to timer depending on if duration upgrade is active
    if (self.colliderect(player)):
      if player.upgrade_self >= 4:
        player.fast_attacks_timer = 400
      player.homing_weapon_timer = 200
      player.homing_weapon = True
      self.alive = False
    super().update(player)


      