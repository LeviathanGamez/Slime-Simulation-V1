from random import randint, shuffle
import pygame
import math
pygame.init()
import sys
#Screen
screen_width =  1400
screen_height = 850

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Slime Sim')
# TESTING MODE for data
total = 0
#Global Variables
wait_time = 100
#DO NOT CHANGE WAIT TIME
running = True
mult = 8
delta_time = 0.1
clock = pygame.time.Clock()
time_stop = False
rect_width = 500
rect_height = 200
mutation = 100
multiplier = 1
multiplier2 = 1
#Font
font = pygame.font.Font('assets/JetBrainsMono-Regular.ttf', 32)
mini_font = pygame.font.Font('assets/JetBrainsMono-Regular.ttf', 20)
tiny_font = pygame.font.Font('assets/JetBrainsMono-Regular.ttf', 12)

all_speed = 0
all_range = 0
all_hunger = 0
all_water = 0
zoom = 1
#Functions
def draw(obj,win):
   win.blit(obj.img, (obj.x-obj.img.get_width() /2, obj.y-obj.img.get_height() /2))
   obj.rect.topleft=(obj.x-obj.img.get_width() /2, obj.y-obj.img.get_height() /2)
def mouse_col(obj):
   global mouse
   if obj.rect.collidepoint(mouse):
      if pygame.mouse.get_pressed()[0]:
         global target_slime
         if type(obj) == type(Cells[0]):
            target_slime = obj
#Clases
class Cell_:
   def __init__(self,coords, speed, range, hunger, water,insta_mate):
      global total
      total += 1
      self.number = total
      #base values 
      ''' max_hunger = 20 max_water = 20 speed = 100 range = 120 '''
      self.img = pygame.image.load('assets/SlimeNoBg.png').convert()
      self.img = pygame.transform.scale(self.img,
                                          (self.img.get_width() / 8*zoom,
                                          self.img.get_height() / 8*zoom))
      
      self.x = coords[0] 
      self.y = coords[1]
      if hunger ==0 or water ==0:
         self.max_hunger = hunger+1
         self.max_water = water+1
      else:
         self.max_hunger = hunger
         self.max_water = water
      self.og_speed = speed
      self.speed = speed * mult
      self.range = range 
      self.can_mate = insta_mate
      if insta_mate:
         self.hunger = self.max_hunger
      else:
         self.hunger = 24
      self.water = 24
      
      self.hunger_ratio = self.hunger/self.max_hunger
      self.water_ratio = self.water/self.max_water
      self.rand = 0
      self.old_rand = self.rand
      self.state = "idle"
      self.target = "none"
      self.rect=self.img.get_rect()
      self.babies = 0
      
      self.count = 0
      self.countdown = 0
   

   def out_of_bounds(self):
            return (
               self.x+ wait_time/4*math.cos(self.rand)*self.og_speed*delta_time < 0
               or self.x+ wait_time/4*math.cos(self.rand)*self.og_speed*delta_time > screen_width
               or self.y+ wait_time/4*math.sin(self.rand)*self.og_speed*delta_time < 0
               or self.y+ wait_time/4*math.sin(self.rand)*self.og_speed*delta_time > screen_height
            )
   def behavior(self):
      if  self.state == "idle":
         if self.hunger >= 25 and self.water >= 25:
            for Cell in Cells:
               if (Cell.x -self.x)**2+(Cell.y- self.y)**2 <= self.range**2 and Cell != self:
                  if self.can_mate and Cell.can_mate:
                     self.state = "lock-in"
                     self.target = Cell
                     break
         elif self.hunger_ratio <= 0.7 and self.hunger_ratio < self.water_ratio:
            for Plant in Plants:
               if (Plant.x -self.x)**2+(Plant.y- self.y)**2 <= self.range**2 and Plant.food > 0:
                  self.state = "lock-in"
                  self.target = Plant
                  break
         elif self.water_ratio <= 0.7:
            for Lake in Lakes:
               if (Lake.x -self.x)**2+(Lake.y- self.y)**2 <= self.range**2:
                  self.state = "lock-in"
                  self.target = Lake
                  break
         else:
            if self.hunger_ratio < 0.4:
               for Plant in Plants:
                  if (Plant.x -self.x)**2+(Plant.y- self.y)**2 <= self.range**2 and Plant.food > 0:
                     self.state = "lock-in"
                     self.target = Plant
                     break
            elif self.water_ratio < 0.4:
               for Lake in Lakes:
                  if (Lake.x -self.x)**2+(Lake.y- self.y)**2 <= self.range**2:
                     self.state = "lock-in"
                     self.target = Lake
                     break
         

         if self.state == "idle":
               self.state = "random"
      elif  self.state == "lock-in":
         #X
         if  self.target.x >  self.x:
             self.x +=  self.speed*delta_time
         elif (self.target.x- self.x)**2+(self.target.y- self.y)**2 < 40**2: # og 40**2
            if type(self.target) == plant_type and self.target.food > 0:
               self.state = "eating"
               self.target.food -= 10
            elif type(self.target) == type(Lakes[0]):
               self.state = "drinking"
            elif type(self.target) == type(Cells[0]):
               self.state = "mating"
            else:
               self.state = "random"
            
            
         else:
             self.x -=  self.speed*delta_time
         #Y
         if  self.target.y >  self.y:
             self.y +=  self.speed*delta_time
         else:
             self.y -=  self.speed*delta_time
      elif  self.state == "mating":
         self.countdown += 1 * mult
         if self.countdown == 40 :
            if randint(0,1) == 1:
               self.babies += 1
               Cells.append(Cell_([(self.target.x+self.x)//2,(self.target.y+self.y)//2],(self.og_speed+self.target.og_speed)//2+randint(0,mutation)-mutation/2,(self.range+self.target.range)//2+randint(0,mutation)-mutation/2,(self.max_hunger+self.target.max_hunger)//2+randint(0,mutation//2)-mutation//4,(self.max_water+self.target.max_water)//2+randint(0,mutation//2)-mutation//4,False))
            self.state = "random"
            self.countdown = 0
            self.can_mate = False

      elif  self.state == "eating":
         self.countdown += 1 * mult 
         if self.countdown % 24 == 0:
            self.hunger += 3 + self.max_hunger/50
         if self.countdown >= wait_time:
            self.state = "random"
            self.countdown = 0
      elif  self.state == "drinking":
         self.countdown += 1 * mult
         if self.countdown % 24 == 0:
            self.water += 3 + self.max_water/50
         if self.countdown >= wait_time:
            self.state = "random"
            self.countdown = 0
      elif  self.state == "random":
         self.countdown += 1 *mult
         if self.countdown == 8 :
            self.old_rand = self.rand
            self.rand = math.radians(randint(0,360))
            while self.out_of_bounds() and self.rand not in [(self.old_rand - 210) - i for i in range(30)]:
               self.rand = math.radians(randint(0,360))

            self.x += math.cos(self.rand)* self.speed*delta_time
            self.y += math.sin(self.rand)* self.speed*delta_time
         elif self.countdown < wait_time*3/4:
            while self.out_of_bounds():
               self.rand = math.radians(randint(0,360))
            self.x += math.cos(self.rand)* self.speed*delta_time
            self.y += math.sin(self.rand)* self.speed*delta_time
         elif self.countdown >= wait_time*3/4:
            self.countdown = 0
            self.state = "idle"
      


   def update(self):
      self.count += 1 * mult
      if self.count % 160 == 0 and (self.state != "drinking" and self.state != "eating"):
         self.hunger -= 0.5
      if self.count % 160 == 0 and (self.state != "drinking" and self.state != "eating"):
         self.water -= 0.5
      if self.count == 800:
         self.count = 0
         self.can_mate = True
      self.hunger_ratio = self.hunger/self.max_hunger
      self.water_ratio = self.water/self.max_water
      self.behavior()
      if self.hunger > self.max_hunger:
         self.hunger = self.max_hunger
      if self.water > self.max_water:
         self.water = self.max_water

   def visual(self, target):
      pygame.draw.line(screen, (227, 23, 23), (self.x, self.y), (self.x +math.cos(self.rand)*self.og_speed*delta_time*wait_time*3/4 , self.y +math.sin(self.rand)*self.og_speed*delta_time*wait_time*3/4  ))
      pygame.draw.circle(screen, (65, 85, 224), (self.x  , self.y), self.range, 1)
      # ID then Can_mate
      if target:
         screen.blit(mini_font.render(f"#{Cells.index(self)}", True,(255,255,255) ), pygame.Rect(self.x-20,self.y-self.img.get_height()-self.img.get_height()*0.2,80,100))
      else:
         screen.blit(mini_font.render(f"#{Cells.index(self)}", True,(10,10,10) ), pygame.Rect(self.x-20,self.y-self.img.get_height()-self.img.get_height()*0.2,80,100))


   
class Plant_:
   def __init__(self,coords):
      self.img = pygame.image.load('assets/potato.png').convert()
      self.img = pygame.transform.scale(self.img,
                                          (self.img.get_width() * 4*zoom,
                                          self.img.get_height() * 4*zoom))
      self.img.set_colorkey((0,0,0))
      self.x = coords[0] 
      self.y = coords[1] 
      self.food = 300
      self.rect=self.img.get_rect()
   ''' def update(self):
      
      if self.food == 30 and self.can_breed:
         self.can_breed = False
         for i in range(randint(0,2)):
            rand_x = self.x +randint(0,100)-50
            while rand_x > screen_width or rand_x < 0:
               rand_x = self.x +randint(0,100)-50
            rand_y = self.y +randint(0,100)-50
            while rand_y > screen_height or rand_y < 0:
               rand_y = self.y +randint(0,100)-50
            Plants.append(Plant_([rand_x,rand_y]))'''



class Lake_:
   def __init__(self,coords):
      self.img = pygame.image.load('assets/lake.png').convert()
      self.img = pygame.transform.scale(self.img,
                                          (self.img.get_width() / 4*zoom,
                                          self.img.get_height() / 4*zoom))
      self.img.set_colorkey((0,0,0))
      self.x = coords[0] 
      self.y = coords[1] 
      self.rect=self.img.get_rect()

Cells_coords= [[160,160],[640,500], [160, 200], [1096,620],[1097,630],[600,550],[845,254],[850,260],[160,160],[640,500], [160, 200], [1096,620],[1097,630],[600,550],[845,254],[850,260]]
Plants_coords = [[128,162],[648, 708,255],[1230, 220]]
Lakes_coords = [[230, 696],[646, 213],[1165, 568]]
shuffle(Cells_coords)
# Initializing Classes
# argyments self,coords, speed, range, hunger, water
#Cells = [Cell_(Cells_coords[i], 140/len(Cells_coords)*(i+1)+randint(10,20), (20*(len(Cells_coords)+1)-(20*(i+1)))+randint(20,30),randint(20,40),randint(20,40),True) for i in range(len(Cells_coords))]
Cells = [Cell_(Cells_coords[i], 80/len(Cells_coords)*i+randint(35,45), 140/len(Cells_coords)*i+randint(35,45),randint(25,50),randint(25,50),True) for i in range(len(Cells_coords))]

Plants = [Plant_(Plants_coords[i]) for i in range(len(Plants_coords))]
Lakes = [Lake_(Lakes_coords[i]) for i in range(len(Lakes_coords))]
All = Lakes + Plants + Cells
target_slime = Cells[0]
plant_type = type(Plants[0])
# Game loop
f = open("assets/data.txt","w")
f.write(f"Starting Sim")
f.close()

while running:
   #key + quit
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         running = False
      elif event.type == pygame.KEYDOWN:
         if event.key == pygame.K_SPACE:
            if time_stop:
               time_stop = False
            else:
               time_stop = True
         elif event.key == pygame.K_o:
            if mult != 8:
               mult *= 2
               for Cell in Cells:
                  if Cell.hunger > 0 and Cell.water > 0:
                     Cell.speed *= 2
                     if Cell.countdown % mult != 0:
                        Cell.countdown -= (Cell.countdown % mult)
                     if Cell.count % mult != 0:
                        Cell.count -= (Cell.count % mult)
         elif event.key == pygame.K_p:
            if mult != 1:
               mult /= 2
               for Cell in Cells:
                  if Cell.hunger > 0 and Cell.water > 0:
                     Cell.speed /= 2
                     if Cell.countdown % mult != 0:
                        Cell.countdown -= Cell.countdown % mult
                     if Cell.count % mult != 0:
                        Cell.count -= (Cell.count % mult)

   mouse = pygame.mouse.get_pos()
   All = Cells + Plants + Lakes
   #Display
   screen.fill((113, 227, 68))
   living_potato = 0
   for item in All:
         if type(item) == type(Cells[0]):
            if item.hunger <= 0 or item.water <= 0:
               Cells.remove(item)
            else:
               draw(item,screen)
               if not time_stop:
                  item.update() 
         else:
            if type(item) == plant_type:
               if item.food <= 0:
                  Plants.remove(item)
               else:
                  living_potato += 1
                  draw(item,screen)
                  mouse_col(item)
                  #if not time_stop:
                  #      item.update()
            else:
               draw(item,screen)
               mouse_col(item)
   if len(Cells) < 300:
      for Cell in Cells:
         mouse_col(Cell)
         if Cell == target_slime:
            Cell.visual(True)
         else:
            Cell.visual(False)

   
   time = pygame.time.get_ticks()
   if  time > 5000 * multiplier:
      multiplier += 1
      all_speed = 0
      all_range = 0
      all_hunger = 0
      all_water = 0
      for Cell in Cells:
         all_speed += Cell.og_speed
         all_range += Cell.range
         all_hunger += Cell.hunger
         all_water += Cell.water
               
      f = open("assets/data.txt","a")
                              # time population living avg speed avg range, avg food, avg water, 
      try:
         f.write(f"\n{int(time/1000)},{total},{len(Cells)},{int(all_speed//len(Cells))},{int(all_range//len(Cells))},{int(all_hunger//len(Cells))},{int(all_water//len(Cells))},{living_potato}")
      except:
         print("They are all Dead")
         running = False
      f.close()

   
   if time > 8000* multiplier2:
      multiplier2 += 1
      for i in range(randint(1,2)):
         rand_x = randint(200,screen_width-200)
         while rand_x > screen_width or rand_x < 0:
            rand_x = randint(0,screen_width)
         rand_y = randint(150,screen_height-150)
         while rand_y > screen_height or rand_y < 0:
            rand_y = randint(0,screen_height)
         Plants.append(Plant_([rand_x,rand_y]))

   
   #Control Panel 
   
   texts = [
         f"Cell: {target_slime.number:05} State: {  target_slime.state[0].upper()}{  target_slime.state[1:]}",
         f"X: {round(  target_slime.x,2):07.2f} Y: {round(target_slime.y,2):06.2f}",
         f'Mult: {mult} FPS:{round(clock.get_fps())} Time: {time//1000:04}',
         f'Countdown: {target_slime.countdown:02} Count: {target_slime.count}',
         f'Speed: {target_slime.og_speed} Range: {target_slime.range}',
         f'Can_mate: {target_slime.can_mate} Potato: {living_potato}',
         f'Total: {total} Living: {len(Cells)}',
         f'Avg Speed: {int(all_speed//len(Cells))} Range: {int(all_range//len(Cells))}',
         f'Avg Hunger: {int(all_hunger//len(Cells))} Water: {int(all_water//len(Cells))}']
   s= pygame.Surface((rect_width,32*len(texts)+10))
   #pygame.Rect(screen_width-rect_width,0,rect_width,32*len(texts)+10)
   s.set_alpha(128)
   s.fill((32,32,32))
   screen.blit(s,(screen_width-rect_width,0))
   if target_slime.hunger >0 and target_slime.water >0:
      pygame.draw.rect(screen, (250,255,255), (target_slime.x-target_slime.img.get_width()/2,target_slime.y-target_slime.img.get_height()/2,target_slime.img.get_width(),target_slime.img.get_height()), 1)
   else:
      target_slime = Cells[-1]
   for i in range(len(texts)):
      text = font.render(texts[i], True, (244,244,244) )
      screen.blit(text, pygame.Rect(screen_width-rect_width,32*i,rect_width,rect_height))
   text = font.render(f"X:{mouse[0]}, Y: {mouse[1]}",True,(244,244,244))
   screen.blit(text, pygame.Rect(6,screen_height-42,rect_width,42))
   opacity = 0.1
   # Max hunger + water
   screen.blit(mini_font.render(f"Max:{target_slime.max_hunger}", (10,10,10),(10,10,10) ), pygame.Rect(screen_width-155,screen_height-130,80,100))
   screen.blit(mini_font.render(f"Max:{target_slime.max_water}", (10,10,10),(10,10,10) ), pygame.Rect(screen_width-75,screen_height-130,80,100))
   #Hunger Bar
   pygame.draw.rect(screen,(207, 207, 207),pygame.Rect(screen_width-160,screen_height-100,80,100))
   pygame.draw.rect(screen,(255, 176, 18),pygame.Rect(screen_width-160,screen_height-100*  target_slime.hunger_ratio,80,100))
   #Water Bar
   pygame.draw.rect(screen,(207, 207, 207),pygame.Rect(screen_width-80,screen_height-100,80,100))
   pygame.draw.rect(screen,(33, 70, 233),pygame.Rect(screen_width-80,screen_height-100*  target_slime.water_ratio,80,100))
   #Percentage
   screen.blit(mini_font.render(f"{target_slime.hunger_ratio*100:04.1f}%", (10,10,10),(10,10,10) ), pygame.Rect(screen_width-153,screen_height-70,80,100))
   screen.blit(mini_font.render(f"{target_slime.water_ratio*100:04.1f}%", (10,10,10),(10,10,10) ), pygame.Rect(screen_width-73,screen_height-70,80,100))
   
   
   

   pygame.display.update()
   delta_time = clock.tick(60) / 1000
   delta_time = max(0.001, min(0.1, delta_time))




pygame.quit()
sys.exit()



