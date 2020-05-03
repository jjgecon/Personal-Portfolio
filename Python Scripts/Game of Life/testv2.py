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
        elif self.b > 0:
            self.b -= v 

    def revive(self):
        self.r,self.g,self.b = 0,random.randint(180,220),0

    def on(self):
        self.revive()
        pygame.draw.rect(win,(self.r,self.g,self.b),(self.x,self.y,self.w,self.h))
        self.alive = True
        self.color_degrade()
        if self.r == 0 and self.g == 0 and self.b == 0:
            self.off()

    def off(self):
        pygame.draw.rect(win,(0,0,0),(self.x,self.y,self.w,self.h))
        self.alive = False

    def isalive(self):
        return self.alive

# MAIN
pygame.init()

winwidth, winhieght = 500,500
win = pygame.display.set_mode((winwidth,winhieght))
pp = 3
alive_list = create_alive_list(pp)

# Probs
live_prob = .5
die_prob = .7

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

grid_list[pp+1].on()
alive_list[pp+1] = True
grid_list[0].on()
alive_list[0] = True

# Main Loop
run = True
while run:
    pygame.time.delay(100)

    for point,a in zip(grid_list,alive_list):
        if a == True:
            point.on()
        if a == False:
            point.off()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

# Need to check for the nearest pixels
#   - Case 1: Corners 2 Compare 2 things (4 cases) [0,pp-1,(pp*(pp-1))+1,(pp**2)-1]
#   - Case 2: Inner cases (the other cases)
#   - Case 3: the border conditions

    for point,a,i in zip(grid_list,alive_list,range(len(alive_list))):
        # Case 1.1
        if i == 0:
            if (alive_list[0] == True or alive_list[pp] == True) \
                and random.randint(0,1) >= live_prob:
                point.on()
            elif random.randint(0,1) >= die_prob:
                point.off()
        # Case 1.2
        elif i == pp-1:
            if (alive_list[pp-2] == True or alive_list[(pp**2)-1] == True) \
                and random.randint(0,1) >= live_prob:
                point.on()
            elif random.randint(0,1) >= die_prob:
                point.off()
        # Case 1.3
        elif i == ((pp-1)**2) + (pp-1):
            if (alive_list[(pp*(pp-2))] == True or alive_list[((pp-1)**2) + (pp-1) + 1]  == True) \
                and random.randint(0,1) >= live_prob:
                point.on()
            elif random.randint(0,1) >= die_prob:
                point.off()
        # Case 1.4
        elif i == (pp**2)-1:
            if (alive_list[(pp**2)-1] == True or alive_list[(pp*(pp-1))] == True) \
                and random.randint(0,1) >= live_prob:
                point.on()
            elif random.randint(0,1) >= die_prob:
                point.off()
        # Case 2.1 1st row
        elif i > 0 and i < pp-1:
            if (alive_list[i-1] == True or alive_list[i+1] == True \
                or alive_list[i+pp] == True) and random.randint(0,1) >= live_prob:
                point.on()
            elif random.randint(0,1) >= die_prob:
                point.off()
        # Case 2.2 column 1
        elif i in column1_index:
            if (alive_list[i+1] == True or alive_list[i+pp] == True \
                or alive_list[i-pp] == True) and random.randint(0,1) >= live_prob:
                point.on()
            elif random.randint(0,1) >= die_prob:
                point.off()
        # Case 2.3 final row
        elif i > ((pp-1)**2) + (pp-1) and i < (pp**2)-1:
            if (alive_list[i-1] == True or alive_list[i+1] == True \
                or alive_list[i-pp] == True) and random.randint(0,1) >= live_prob:
                point.on()
            elif random.randint(0,1) >= die_prob:
                point.off()
        # Case 2.4 final column
        elif i in columnpp_index:
            if (alive_list[i-1] == True or alive_list[i+pp] == True \
                or alive_list[i-pp] == True) and random.randint(0,1) >= live_prob:
                point.on()
            elif random.randint(0,1) >= die_prob:
                point.off()
        # Case 3 in the middle
        else:
            if (alive_list[i-1] == True or alive_list[i+1] == True or \
                alive_list[(i-pp)] == True or alive_list[(i+pp)] == True) \
                and random.randint(0,1) >= live_prob:
                point.on()
            elif random.randint(0,1) >= die_prob:
                point.off()
    
    # This is the way toget the pixel at 0,0 to turn off
    # grid_list[0].off()
    # alive_list[0] = False

    pygame.display.update()