# By Javier Gonzalez 5/24/2020 javierj.g18@gmail.com
# A small visualiztion to understand better how do simple linear regresions work

# I Have a little visualization problem here. As the display is upside down, so does the line are displayed!

import pygame
from pygame import gfxdraw
import random
import numpy as np

pygame.init()
clock = pygame.time.Clock()
run = True
winwidth, winhieght = 800,800

win = pygame.display.set_mode((winwidth,winhieght))

white = (255,255,255)
black = (0,0,0)

class Point():

    def __init__(self,x,y,win):
        self.pos = pygame.math.Vector2(int(x), int(y))
        self.win = win

    def show(self):
        r = 6
        # pygame.draw.circle(self.win,black,(int(self.pos.x),int(self.pos.y)),r)
        pygame.gfxdraw.aacircle(self.win,int(self.pos.x),int(self.pos.y),r,black)
        pygame.gfxdraw.filled_circle(self.win,int(self.pos.x),int(self.pos.y),r,black)
        
    def text_point(self):
        ptext = "(" + str(round(self.pos.x)) + ' , '+ str(round(winhieght - self.pos.y)) + ")" 
        display_some_text(ptext,12,self.pos.x + 10, self.pos.y - 10,black,white)

class Fitline():

    def __init__(self,slope,intercept,win):
        self.lw = 10
        self.win = win
        self.intercept = intercept
        self.slope = slope
        self.active = True
        self.color = (255,0,255)
        self.xystart = pygame.math.Vector2(0, intercept)
        self.xyend = pygame.math.Vector2(winwidth, intercept + slope*winwidth)
        # Now to compate the points I need the discrete values
        self.x = np.linspace(0,winwidth,winwidth)
        self.y = np.zeros_like(self.x)
        self.yreal = np.zeros_like(self.x)
        for i in range(winwidth):
            self.yreal[i] = intercept + slope*self.x[i]

    def show(self):
        pygame.draw.aaline(self.win,self.color,(self.xystart.xy),(self.xyend.xy),self.lw)


    def inactive(self):
        self.active = False
        self.color = (150,150,150)

    def activate(self):
        self.active = True
        self.color = (255,0,255)

    def calculate_distance_p(self,points,show_dist = True):
        totald = np.zeros(len(points))
        offsetx = .38
        for p,i in zip(points,range(len(points))):
            if show_dist:
                pygame.draw.aaline(self.win,(255,200,255),(int(p.pos.x),self.yreal[int(p.pos.x)]),
                (p.pos.xy),self.lw)
            totald[i] =  p.pos.y - self.yreal[int(p.pos.x)]
        
        se = np.sum(totald**2)
        # Show the Squared Error
        ff = 22
        display_some_text(f"Intercept = {winhieght - self.intercept:.1f}",ff,winwidth*offsetx, winhieght - 65,self.color,white)
        display_some_text(f"Slope value = {self.slope*(-1):.3f}",ff,winwidth*offsetx, winhieght - 45,self.color,white)
        display_some_text(f"SE = {(se/1000):.1f}",ff,winwidth*offsetx, winhieght - 25,self.color,white)

class OLS:

    def __init__(self,win,points):
        self.points = points
        self.win = win
        self.color = (0,200,0)
        self.lw = 1
        Y = np.zeros(len(points))
        X = np.ones((len(points),2))
        for i in range(len(points)):
            Y[i] = points[i].pos.y
            X[i][1] = points[i].pos.x
        XX_1 = np.linalg.inv(np.dot(X.T,X))
        XY = np.dot(X.T,Y)
        self.beta = np.dot(XX_1,XY)
        x = np.linspace(0,winwidth,winwidth)
        self.yhat = np.zeros_like(x)
        self.yreal = np.zeros_like(x)
        for i in range(winwidth):
            self.yreal[i] = self.beta[0] + self.beta[1]*x[i]
    
    def show(self):
        # Something is off with this fucntion!
        if self.beta[0] < 0:
            for i in range(len(self.yhat)):
                if self.yreal[i] <= 5 and self.yreal[i] >= - 5:
                    self.xystart = pygame.math.Vector2(i, self.yreal[i])
                    self.xyend = pygame.math.Vector2(winwidth, self.yreal[-1])
                    break
        elif winhieght < self.beta[0]:
            for i in range(len(self.yhat)): 
                if self.yreal[i] <= winhieght + 5 and self.yreal[i] >= winhieght-5:
                    self.xystart = pygame.math.Vector2(i, self.yreal[i])
                    self.xyend = pygame.math.Vector2(winwidth, self.yreal[-1])
                    break
        else:
            self.xystart = pygame.math.Vector2(0, self.beta[0])
            self.xyend = pygame.math.Vector2(winwidth, self.beta[0] + self.beta[1]*winwidth)

        pygame.draw.aaline(self.win,self.color,(self.xystart.xy),(self.xyend.xy),self.lw)

    def calculate_distance_p(self,show_dist = True):
        totald = np.zeros(len(self.points))
        for p,i in zip(self.points,range(len(self.points))):
            if show_dist:
                pygame.draw.aaline(self.win,(175,200,175),(int(p.pos.x),self.yreal[int(p.pos.x)]),
                (p.pos.xy),self.lw)
            totald[i] =  p.pos.y - self.yreal[int(p.pos.x)]

        se = np.sum(totald**2)
        # Show the Squared Error
        offsetx = .38
        ff = 22 
        display_some_text(f"Intercept = {winhieght - self.beta[0]:.1f}",ff,winwidth*offsetx, winhieght - 65,self.color,white)
        display_some_text(f"Slope value = {self.beta[1]*(-1):.3f}",ff,winwidth*offsetx, winhieght - 45,self.color,white)
        display_some_text(f"SE = {(se/1000):.1f}",ff,winwidth*offsetx, winhieght - 25,self.color,white)

# Some functions

def display_some_text(intext,fontsize,x,y,color,bg):
    font = pygame.font.Font('freesansbold.ttf', fontsize)
    text = font.render(intext, True, color, bg) 
    win.blit(text,(x, y))

def draw(points):
    win.fill(white) 
    ff = 15

    if lines:
        for l in lines:
            l.show()
            if l.active:
                l.calculate_distance_p(points,show_d)
            
    
    if ols_list:
        ols_list[0].show()
        ols_list[0].calculate_distance_p(show_d)

    for d in points:
        d.show()
        if display_point_t:
            d.text_point()
        

    pygame.draw.rect(win,white,(0,winhieght-70,winwidth*(.28),winhieght-70))
    pygame.draw.rect(win,white,(winwidth*(.69),winhieght-70,winwidth*(.3),winhieght-70))
    display_some_text("Press 'd' to substract points",ff,20, winhieght-20,black,white)
    display_some_text("Press 'a' to add points",ff,20, winhieght-40,black,white)
    display_some_text("Press 'i' to show distantance",ff,20, winhieght-60,black,white)
    display_some_text("Press 'x' to hide point location",ff,winwidth*(.7), winhieght-20,black,white)
    display_some_text("Press 's' to show point location",ff,winwidth*(.7), winhieght-40,black,white)
    display_some_text("Press 'o' to hide distantance",ff,winwidth*(.7), winhieght-60,black,white)

    pygame.display.update()

resetpoints = False
slopes = False
intercept = False
ols = False
display_point_t = False
show_d = False

if __name__ == "__main__":
    
    data = []
    n = 20

    for i in range(n):
        rx = int(random.uniform(20,winwidth-70))
        ry = int(random.uniform(20,winhieght-70))
        data.append(Point(rx,ry,win))

    lines = []
    n_lines = 20

    ols_list = []

    while run:

        clock.tick(15)

        keys = pygame.key.get_pressed()
        #Out check
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if keys[pygame.K_DOWN]:
            for i in range(len(lines)):
                if lines[i].active:
                    if i == len(lines)-1:
                        lines[i].inactive()
                        lines[0].activate()
                        break
                    else:
                        lines[i].inactive()
                        lines[i+1].activate()
                        break

        if keys[pygame.K_UP]:
            for i in range(len(lines)):
                if lines[i].active:
                    if i == 0:
                        lines[0].inactive()
                        lines[-1].activate()
                        break
                    else:
                        lines[i].inactive()
                        lines[i-1].activate()
                        break

        if keys[pygame.K_r]:
            resetpoints = True

        if keys[pygame.K_LEFT]:
            slopes = True

        if keys[pygame.K_RIGHT]:
            intercept = True

        if keys[pygame.K_SPACE]:
            ols = True

        if keys[pygame.K_s]:
            display_point_t = True
        if keys[pygame.K_x]:
            display_point_t = False

        if keys[pygame.K_a]:
            if n >= 100:
                n = 100
            else:
                n += 5
            resetpoints = True

        if keys[pygame.K_d]:
            if n <= 5:
                n = 5
            else:
                n -= 5
            resetpoints = True
        
        if keys[pygame.K_c]:
            lines = []
            ols_list = []
        
        if keys[pygame.K_i]:
            show_d = True
        if keys[pygame.K_o]:
            show_d = False

        if ols:
            lines = []
            ols_list.append(OLS(win,data))
            ols = False

        if resetpoints:
            data = []
            for i in range(n):
                rx = int(random.uniform(20,winwidth-70))
                ry = int(random.uniform(20,winhieght-70))
                data.append(Point(rx,ry,win))
            resetpoints = False
            if ols_list:
                ols_list = []
                ols_list.append(OLS(win,data))

        if intercept:
            ols_list = []
            lines = []
            for i in range(n_lines):
                lines.append(Fitline(.2,30*i,win))
                lines[i].inactive()

            lines[0].activate()
            
            ols = False
            slopes = False
            intercept = False

        if slopes:
            ols_list = []
            lines = []
            SSlopes =  np.linspace(-.6,.6,n_lines)
            for s,i in zip(SSlopes,range(len(SSlopes))):
                lines.append(Fitline(s,winhieght//2,win))
                lines[i].inactive()
            lines[0].activate()

            ols = False
            slopes = False
            intercept = False
        
        draw(data)

    pygame.quit()


