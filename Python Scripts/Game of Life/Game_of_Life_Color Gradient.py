# By Javier Gonzalez 4/29/2020 javierj.g18@gmail.com
# Code that simulated the Conway's Game of Life using Pygame!

import pygame
import random

global alive_list, alive_list_aux

def create_alive_list(pp):
    alive = []
    for i in range(pp**2):
        alive.append(False)
    return alive

def create_grid(winwidth,winhieght,pixels):
    gwidht = winwidth/pixels
    gheight = winhieght/pixels

    grid_points = []

    for r in range(pixels):
        for c in range(pixels):
            grid_points.append([c*gwidht,r*gheight])
    
    return [grid_points,gwidht,gheight]

def Game_Rules(grid_p,list_index,compare,alive):
    global alive_list, alive_list_aux
    """
    Now once I have the code to compare every cell lets implement the actual rules
    R1 = Any live cell with fewer than two live neighbours dies, as if by underpopulation.
    R2 = Any live cell with two or three live neighbours lives on to the next generation.
    R3 = Any live cell with more than three live neighbours dies, as if by overpopulation.
    R4 = Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
    """
    # R1
    if compare < 2 and alive == True:
        grid_p.off()
        alive_list_aux[list_index] = False
    # R2
    elif compare in [2,3] and alive == True:
        grid_p.on()
        alive_list_aux[list_index] = True
    # R3
    elif compare > 3 and alive == True:
        grid_p.off()
        alive_list_aux[list_index] = False
    # R4
    elif compare == 3 and alive == False:
        grid_p.on()
        alive_list_aux[list_index] = True


class gridentity:
    def __init__(self,x,y,w,h,alive = False):
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        self.alive = alive
        self.r,self.g,self.b = 0,0,0

    def color_degrade(self):
        v = 10
        if self.r > 10:
            self.r -= v
        elif  self.g > 10:
            self.g -= v
        elif self.b > 10:
            self.b -= v 

    def revive(self):
        c = random.randint(230,255)
        self.r,self.g,self.b = c,c,c

    def on(self):
        self.revive()
        pygame.draw.rect(win,(self.r,self.g,self.b),(self.x,self.y,self.w,self.h))
        self.alive = True
        self.color_degrade()
        if self.r == 0 and self.g == 0 and self.b == 0:
            self.off()

    def off(self):
        self.color_degrade()
        pygame.draw.rect(win,(self.r,self.g,self.b),(self.x,self.y,self.w,self.h))
        self.alive = False

    def isalive(self):
        return self.alive

# MAIN
pygame.init()
clock = pygame.time.Clock()

winwidth, winhieght = 900,900
win = pygame.display.set_mode((winwidth,winhieght))
pp = 60
alive_list = create_alive_list(pp)

grid_points,gwidht,gheight = create_grid(winwidth, winhieght,pp)
grid_list = []

for (x,y),a in zip(grid_points,alive_list):
    grid_list.append(gridentity(x,y,gwidht,gheight,a))

column1_index = []
columnpp_index = []
for i in range(pp):
    column1_index.append(i*pp)
    if i == 0:
        x = pp-1
    else:
        x += pp
    columnpp_index.append(x)

# Let's start with some pixels
starting = []
for i in range(pp**2):
    if random.randint(0,10) >= 8:
        starting.append(i)

for index in starting:
    grid_list[index].on()
    alive_list[index] = True

# Window Loop
run = True
while run and sum(alive_list) > 0:
    clock.tick(10)

    for point,a in zip(grid_list,alive_list):
        if a == True:
            point.on()
        if a == False:
            point.off()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

# Need to check for the nearest pixels
#   - Case 1: Corners 2 Compare 3 things (4 cases) [0,pp-1,(pp*(pp-1))+1,(pp**2)-1]
#   - Case 2: Inner cases (the other cases)
#   - Case 3: the border conditions

    alive_list_aux = alive_list.copy()

    for point,i in zip(grid_list,range(len(alive_list))):
        # Case 1.1
        if i == 0:
            alive = point.isalive()
            compare = sum([alive_list[0],alive_list[pp],alive_list[pp+1]])
            Game_Rules(point,i,compare,alive)
        # Case 1.2
        elif i == pp-1:
            alive = point.isalive()
            compare = sum([alive_list[pp-2],alive_list[(2*pp)-1],alive_list[(2*pp)-2]])
            Game_Rules(point,i,compare,alive)
        # Case 1.3
        elif i == ((pp-1)**2) + (pp-1):
            alive = point.isalive()
            compare = sum([alive_list[(pp*(pp-2))],alive_list[(pp*(pp-2))+1],\
                           alive_list[((pp-1)**2) + (pp-1) + 1]])
            Game_Rules(point,i,compare,alive)
        # Case 1.4
        elif i == (pp**2)-1:
            alive = point.isalive()
            compare = sum([alive_list[(pp**2)-1],alive_list[(pp*(pp-1))-1],alive_list[(pp*(pp-1))-2]])
            Game_Rules(point,i,compare,alive)
        # Case 2.1 1st row
        elif i > 0 and i < pp-1:
            alive = point.isalive()
            compare = sum([alive_list[i-1],alive_list[i+1],alive_list[i+pp],alive_list[i+pp+1],\
                           alive_list[i+pp-1]])
            Game_Rules(point,i,compare,alive)
        # Case 2.2 column 1
        elif i in column1_index:
            alive = point.isalive()
            compare = sum([alive_list[i+1],alive_list[i-pp],alive_list[i+pp],\
                           alive_list[i-pp+1],alive_list[i+pp+1]])
            Game_Rules(point,i,compare,alive)
        # Case 2.3 final row
        elif i > ((pp-1)**2) + (pp-1) and i < (pp**2)-1:
            alive = point.isalive()
            compare = sum([alive_list[i-1],alive_list[i+1],alive_list[i-pp]])
            compare = sum([alive_list[i-1],alive_list[i+1],alive_list[i-pp],\
                           alive_list[i-pp-1],alive_list[i-pp+1]])
            Game_Rules(point,i,compare,alive)
        # Case 2.4 final column
        elif i in columnpp_index:
            alive = point.isalive()
            compare = sum([alive_list[i-1],alive_list[i-pp],alive_list[i+pp],\
                           alive_list[i-pp-1],alive_list[i+pp-1]])
            Game_Rules(point,i,compare,alive)
        # Case 3 in the middle
        else:
            alive = point.isalive()
            compare = sum([alive_list[i+1],alive_list[i-1],alive_list[i-pp],alive_list[i+pp],\
                           alive_list[i-pp+1],alive_list[i-pp-1],alive_list[i+pp+1],\
                           alive_list[i+pp-1]])
            Game_Rules(point,i,compare,alive)
    
    alive_list = alive_list_aux
    pygame.display.update()
pygame.quit()