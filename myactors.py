from pgzero.builtins import Actor, keyboard, keys
import math, sys, random
from constants import *

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
    self.img = "princess"
    self.health = 100
    
    self.xp = 0
    self.level = 0
    self.xp_required = 500
    super().__init__(self.img,x,y,5)

  def update(self):
    # Return vector representing amount of movement that should occur
    self.dx, self.dy = 0, 0
    if keyboard.a:
        self.dx = -1
    elif keyboard.d:
        self.dx = 1
    if keyboard.w:
        self.dy = -1
    elif keyboard.s:
        self.dy = 1
    
    super().update()
  # is used to process damage from mobs, reduces player health by amount passed in.
  def hurt(self,damage):
    self.health -= damage
    #print(self.health)
    if (self.health<=0):
      print("game over")
    if (self.health >= 100):
      self.health = 100

  def experience(self, XP):
    self.xp += XP
    #print("xp=" + str(self.xp))
#xp required to level up scales exponentially, when the required amount is reached the player level increases.
#once the level is reached the scaling kicks in and reallocates the required xp amount.
    if self.xp > self.xp_required:
      self.level += 1
      self.xp_required = (self.xp_required * 1.2)
      self.xp = 0
      #print(self.xp_required)
      #print("lvl" + str(self.level))
class Monster(MyActor):
  def __init__(self, img, posx, posy,spd):
    super().__init__(img, posx, posy, spd)
    self.alive = True
    
  def update(self,player,knife):
    # Return vector representing amount of movement that should occur    
    super().update()   
    if (self.colliderect(player)):
      player.hurt(self.damage)
      self.alive = False

    if (self.collidelist(knife)) != -1:
      player.experience(25)
      self.alive = False
      

class Bat(Monster):
  def __init__(self, screencoords):
    self.damage = 10
    self.health = 10

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

    super().__init__("bat", posx, posy, 1)
  
  def hurt(self,damage):
    self.health -= damage
    if (self.health<=0):
      self.alive = False

  def update(self,player,knife): 

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
    

    super().update(player,knife)   


class Lion(Monster):
  def __init__(self, screencoords):
    self.health = 10
    self.damage = 10
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
    super().__init__("bat", posx, posy, 3)

  def hurt(self,damage):
    self.health -= damage
    if (self.health<=0):
      self.alive = False

  def update(self,player,knife): 
    #use a timer to make sure monster only moves at certain intervals.
    self.movementTimer += 1

    if self.movementTimer == 90:
      self.movementTimer = 0

    if self.movementTimer > 31:
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

    super().update(player,knife)  

class Totem(Monster):

  def __init__(self, screencoords):
    self.health = 10
    self.distance = 0
    self.damage = 10

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
    super().__init__("bat", posx, posy, 3)


  def hurt(self,damage):
    self.health -= damage
    if (self.health<=0):
      self.alive = False

  def update(self,player,knife): 
    #use a timer to make sure monster only moves at certain intervals.
    #distance from player = square root of ((x of object - x of player)squared + (y of object - y of player)squared)
    self.distance = math.sqrt(((self.vposx - player.vposx) ** 2) + ((self.vposy - player.vposy) ** 2))
    

    # adjust this value to choose how close the mob should be before it moves towards the player.
    # if distance from the player is short enough the mob will move towards player as usual.
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
    super().__init__("arrow", x, y, 10)
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
    if self.vposy > 975:
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
    super().__init__("arrow", x, y, 10)
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
    if self.vposy > 975:
      self.alive = False
    
    super().update()

#class Weapon(MyActor):
  #def __init__(self, x , y ,player):
    #super().__init__("bat", x, y, 1)
    #self.x == player.vposx
    #self.y == player.vposy
    #self.alive = True
  #def update(self,Monster):
    # Return vector representing amount of movement that should occur    
    
    #self.dx = 1
    #self.dy = 0
    #if (self.colliderect(Monster)):
      #Monster.alive = False
      #self.alive = False

#class tKnife(Weapon):
  #def __init__(self, player):
    #posx == player.vposx
    #posy == player.vposy
    #super().__init__("bat", posx, posy, 1)


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
    #self.posx = x
    #self.posy = y
    super().__init__("bat", x, y, 0)

  def update(self,player):
    #if (self.colliderect(player)):
    if (self.colliderect(player)):
      player.hurt(-50)
      self.alive = False
      
    super().update(player)

#min vposy =26:
#max vposy = 1374:
#max vposx = 979:     
#min vposx = 21:

      