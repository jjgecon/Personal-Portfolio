import pygame
import random

def create_alive_list(pp):
    alive = []
    for a in range(pp**2):
        alive.append(False)
    return alive

def create_grid(winwidth,winhieght,pixels):
    gwidht = winwidth/pixels
    gheight = winhieght/pixels

    grid_points = []

    for r in range(pixels):
        for c in range(pixels):
            grid_points.append([r*gwidht,c*gheight])
    
    return [grid_points,gwidht,gheight]

class gridentity:
    def __init__(self,x,y,w,h,alive = False):
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        self.alive = alive
        self.r,self.g,self.b = 0,random.randint(180,220),0

    def color_degrade(self):
        v = 1
        if self.r > 0:
            self.r -= v 
        elif  self.g > 0:
            self.g -= v 
        elif self.b > v:
            self.b -= v 

    def revive(self):
        self.r,self.g,self.b = 0,random.randint(180,220),0

    def on(self):
        pygame.draw.rect(win,(self.r,self.g,self.b),(self.x,self.y,self.w,self.h))
        self.alive = True
        self.color_degrade()

    def off(self):
        pygame.draw.rect(win,(0,0,0),(self.x,self.y,self.w,self.h))
        self.alive = False

    def isalive(self):
        return self.alive

# MAIN
pygame.init()

winwidth, winhieght = 500,500
win = pygame.display.set_mode((winwidth,winhieght))
a = False
pp = 10
alive_list = create_alive_list(pp)

grid_points,gwidht,gheight = create_grid(winwidth, winhieght,pp)
grid_list = []

for (x,y),a in zip(grid_points,alive_list):
    grid_list.append(gridentity(x,y,gwidht,gheight,a))

run = True
while run:
    pygame.time.delay(30)

    for point,a in zip(grid_list,alive_list):
        if a == True:
            point.on()
        if a == False:
            point.off()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        for point,i in zip(grid_list,range(len(alive_list))):
            point.revive()
            alive_list[i] = True

    if keys[pygame.K_RIGHT]:
        for point,i in zip(grid_list,range(len(alive_list))):
            point.off()
            alive_list[i] = False

    if keys[pygame.K_UP]:
        print('\n')
        status = []
        for point in grid_list:
            status.append(point.isalive())
        print(status)
         
    if keys[pygame.K_SPACE]:
        print('\n')
        print(f'Grid List: {len(grid_list)}')
        print(f'Grid List: {len(alive_list)}')
    
    # This is the way toget the pixel at 0,0 to turn off
    # grid_list[0].off()
    # alive_list[0] = False

    pygame.display.update()