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

    if (self.olddirection != direction):
      self.imgno = direction

    if (self.timer==10):
      self.timer = 0
      if (self.olddirection == direction):
        self.imgno +=1
        if ((self.imgno==4) or (self.imgno==7) or (self.imgno==10) or (self.imgno==13)):
          self.imgno -= 3   

    self.image = f'{self.myimg}_{self.imgno}'
    self.olddx = self.dx
    self.olddirection = direction


    # Return vector representing amount of movement that should occur
    self.dx = self.dx * self.speed
    self.dy = self.dy * self.speed

    self.vposx += self.dx
    self.vposx = max(0+PLAYER_W,min(self.vposx, LEVEL_W-PLAYER_W))    
    self.vposy += self.dy
    self.vposy = max(0+PLAYER_H,min(self.vposy, LEVEL_H-PLAYER_H))

  def draw(self, offset_x, offset_y):
    self.pos = (self.vposx - offset_x, self.vposy - offset_y)
    super().draw()

class Player(MyActor):
  def __init__(self, x, y):
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
    #declaring variables for each powerup to accessn
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
    #self.timer -= 1
  
    if self.upgrade_self >= 1:
      self.speed = 5

    if self.upgrade_self >= 3:
      self.speed = 7

    if self.upgrade_weapon >= 1:
      self.damage = 7

    if self.upgrade_weapon >= 3:
      self.damage = 10
    if self.upgrade_weapon >= 4:
      self.homing_flag = True
    

    if self.shield_timer == 0:
      self.shield = False
    if self.fast_attacks_timer == 0:
      self.fast_attacks = False
    if self.homing_weapon_timer == 0:
      self.homing_weapon = False
      
    #print(self.damage) -- TESTING


    self.dx, self.dy = 0, 0
    if keyboard.a:
        self.dx = -1
    elif keyboard.d:
        self.dx = 1
    if keyboard.w:
        self.dy = -1
    elif keyboard.s:
        self.dy = 1
    #print(self.level)
    super().update()
  # is used to process damage from mobs, reduces player health by amount passed in.
  def hurt(self,damage):
    if self.shield == False:
      self.health -= damage
    #print(self.health)
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
    ## print("xp=" + str(self.xp))
    ## xp required to level up scales exponentially, when the required amount is reached the player level increases.
    ## once the level is reached the scaling kicks in and reallocates the required xp amount.
    if self.xp > self.xp_required:
      self.level += 1
      
      self.xp_required = (self.xp_required * 1.3)
      self.xp = 0
      if self.upgrade_self and self.upgrade_weapon == 4:
        pass
      else:
        self.leveluptrigger = True
      #print(self.xp_required)
      #print("lvl" + str(self.level))
class Monster(MyActor):
  def __init__(self, img, posx, posy,spd):
    super().__init__(img, posx, posy, spd)
    self.invuln = False
    self.invuln_timer = 0
    self.alive = True
  
    #print(damage)

    
  def hurt(self,dmg):
      #print(self.health)
      if self.invuln == False:
        self.health -= dmg
        self.invuln = True
        self.invuln_timer = 10

  def update(self,player,knife):
    # Return vector representing amount of movement that should occur    
    super().update()   
    

    if (self.collidelist(knife)) != -1:
      self.hurt(player.damage)
      #self.alive = False
      #player.experience(25)
    if self.invuln == True:
        self.invuln_timer -= 1
    if self.invuln_timer == 0:
      self.invuln = False
    if (self.health<=0):
      self.alive = False
      player.experience(25)
    
    
    if (self.colliderect(player)):
        player.hurt(self.damage)
        if player.shield == False:
          self.alive = False      

    

class Bat(Monster):
  def __init__(self, screencoords, wave):
    self.mode = wave
    # if self.wave = even:
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
  
  #def hurt(self):
    #self.health -= self.player.damage
    #if (self.health <= 0):
      #self.alive = False

  def update(self,player,knife): 
    # if self.wave = even:
    
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
      # if self.wave = odd:
    
      #print(self.health)
    if self.invuln == True:
      self.myimg = "bat_invuln"
    else:
      self.myimg = "bat"


    

    

    super().update(player,knife)   


class Armor(Monster):
  def __init__(self, screencoords, wave):
    self.mode = wave
    # if self.wave = even:
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
    # if self.wave = even:
    
    
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
      self.dy = 0
      self.dx = 0
    ## If the mob has invincibility, show damaged sprite, otherwise keep regular sprite
    if self.invuln == True:
      self.myimg = "armor_invuln"
    else:
      self.myimg = "armor"
    
    
    

    super().update(player,knife)  

class Princess(Monster):

  def __init__(self, screencoords, wave):
    self.mode = wave
    # if self.wave = even:
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
    #use a timer to make sure monster only moves at certain intervals.
    #distance from player = square root of ((x of object - x of player)squared + (y of object - y of player)squared)
    self.distance = math.sqrt(((self.vposx - player.vposx) ** 2) + ((self.vposy - player.vposy) ** 2))
    
    
    # adjust this value to choose how close the mob should be before it moves towards the player.
    # if distance from the player is short enough the mob will move towards player as usual.
    # if mode is even
    if self.mode % 2 == 0:
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
    #if mode is odd
    else:
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
    ## If the mob has invincibility, show damaged sprite, otherwise keep regular sprite
    if self.invuln == True:
      self.myimg = "princess_invuln"
    else:
      self.myimg = "princess"

    super().update(player,knife) 



class Weapon(MyActor):
  def __init__(self, img, posx, posy,spd):
    
    super().__init__(img, posx, posy, spd,)

    self.alive = True

  def update(self):
      
    super().update()   
    

class Knife(Weapon):
  
  #figure out how to get the player pos values and assign them to the weapon when initialised.
  def __init__(self, x, y):
    self.damage = 10
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
    
    #initialize with the direction that player is facing, at the players position.
    super().__init__("basic_pink", x, y, 10)
  #adapted from player update code
  def update(self):
    # Return vector representing amount of movement that should occur
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
  
  #figure out how to get the player pos values and assign them to the weapon when initialised.
  def __init__(self, x, y, mob):
  
    #closest = WIDTH
    #closestmob = ""

    #for mob in moblist:
      #mob.distance = math.sqrt(((x - mob.vposx) ** 2) + ((y - mob.vposy) ** 2))
      #if mob.distance < closest:
        #closest = mob.distance
        #closestmob = mob

      #print(y)
    self.damage = 10
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
    #else:
      #self.diry = 1
      #self.dirx = 1
    #initialize with the direction that player is facing, at the players position.
    super().__init__("basic_blue", x, y, 10)
  #adapted from player update code
  def update(self):
    # Return vector representing amount of movement that should occur

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


# Powerup class will be used for XP and ofc powerups, similar to an enemy this will just check for collision and then dissapear if detected
# Need to find a way for this to change some values i.e. adding XP to the player or changing thier speed values, affecting weapon speed or damage ect.
class Powerup(MyActor):
  def __init__(self, img, posx, posy,spd):

    super().__init__(img, posx, posy, spd)
    self.alive = True

  def update(self, player):
    
    super().update()
    

class Health(Powerup):
  def __init__(self):
    
    x = random.randint(21,979)
    y = random.randint(26,975)
    
    super().__init__("powerup_green", x, y, 0)

  def update(self,player):
    
    if (self.colliderect(player)):
      player.heal(50)
      self.alive = False
      
    super().update(player)

class Shield(Powerup):
  def __init__(self):
    
    x = random.randint(21,979)
    y = random.randint(26,975)
    
    super().__init__("powerup_blue", x, y, 0)

  def update(self,player):
    
    if (self.colliderect(player)):
      if player.upgrade_self >= 4:
        player.shield_timer = 300
      player.shield_timer = 200
      player.shield = True
      self.alive = False
      
    super().update(player)

class Double_XP(Powerup):
  def __init__(self):
    
    x = random.randint(21,979)
    y = random.randint(26,975)
    
    super().__init__("powerup_yellow", x, y, 0)

  def update(self,player):
    
    if (self.colliderect(player)):
      if player.upgrade_self >= 4:
        player.Double_XP_timer = 400
      player.Double_XP_timer = 200
      player.Double_XP = True
      self.alive = False
      
    super().update(player)

class Fast_attacks(Powerup):
  def __init__(self):
    
    x = random.randint(21,979)
    y = random.randint(26,975)
    
    super().__init__("powerup_red", x, y, 0)

  def update(self,player):
    
    if (self.colliderect(player)):
      if player.upgrade_self >= 4:
        player.fast_attacks_timer = 400
      player.fast_attacks_timer = 200
      player.fast_attacks = True
      
      self.alive = False
      
    super().update(player)

class Homing_weapon(Powerup):
  def __init__(self):
    
    x = random.randint(21,979)
    y = random.randint(26,975)
    
    super().__init__("powerup_pink", x, y, 0)

  def update(self,player):
    
    if (self.colliderect(player)):
      if player.upgrade_self >= 4:
        player.fast_attacks_timer = 400
      player.homing_weapon_timer = 200
      player.homing_weapon = True
      self.alive = False
      
    super().update(player)
#min vposy =26:
#max vposy = 1374:
#max vposx = 979:     
#min vposx = 21:

      