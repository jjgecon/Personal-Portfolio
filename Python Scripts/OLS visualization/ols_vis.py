import pygame
from pygame import gfxdraw
import random
import numpy as np

def display_some_text(intext,fontsize,x,y,color,bg,win):
    font = pygame.font.Font('freesansbold.ttf', fontsize)
    text = font.render(intext, True, color, bg) 
    win.blit(text,(x, y))

class Point():

    def __init__(self,x,y,win,w):
        self.pos = pygame.math.Vector2(int(x), int(y))
        self.win = win
        self.winhieght = w
        self.white = (255,255,255)
        self.black = (0,0,0)

    def show(self):
        r = 6
        # pygame.draw.circle(self.win,black,(int(self.pos.x),int(self.pos.y)),r)
        pygame.gfxdraw.aacircle(self.win,int(self.pos.x),int(self.pos.y),r,self.black)
        pygame.gfxdraw.filled_circle(self.win,int(self.pos.x),int(self.pos.y),r,self.black)
        
    def text_point(self):
        ptext = "(" + str(round(self.pos.x)) + ' , '+ str(round(self.winhieght - self.pos.y)) + ")" 
        display_some_text(ptext,12,self.pos.x + 10, self.pos.y - 10,self.black,self.white,self.win)

class Line():

    def __init__(self,slope,intercept,win,w,h,points):
        self.lw = 10
        self.white = (255,255,255)
        self.black = (0,0,0)
        self.winwidth = w
        self.winhieght = h
        self.win = win
        self.intercept = intercept
        self.slope = slope
        self.active = True
        self.color = (255,0,255)
        self.points = points
        self.xystart = pygame.math.Vector2(0, self.intercept)
        self.xyend = pygame.math.Vector2(self.winwidth, self.intercept + self.slope*self.winwidth)
        # Now to compate the points I need the discrete values
        self.x = np.linspace(0,self.winwidth,self.winwidth)
        self.y = np.zeros_like(self.x)
        self.yreal = np.zeros_like(self.x)
        for i in range(self.winwidth):
            self.yreal[i] = intercept + slope*self.x[i]

    def show(self):
        if self.intercept < 0:
            for i in range(len(self.yreal)):
                if self.yreal[i] <= 5 and self.yreal[i] >= - 5:
                    self.xystart = pygame.math.Vector2(i, self.yreal[i])
                    self.xyend = pygame.math.Vector2(self.winwidth, self.yreal[-1])
                    break
        elif self.winhieght < self.intercept:
            for i in range(len(self.yreal)): 
                if self.yreal[i] <= self.winhieght + 5 and self.yreal[i] >= self.winhieght-5:
                    self.xystart = pygame.math.Vector2(i, self.yreal[i])
                    self.xyend = pygame.math.Vector2(self.winwidth, self.yreal[-1])
                    break
        else:
            self.xystart = pygame.math.Vector2(0, self.intercept)
            self.xyend = pygame.math.Vector2(self.winwidth, self.intercept + self.slope*self.winwidth)

        pygame.draw.aaline(self.win,self.color,(self.xystart.xy),(self.xyend.xy),self.lw)


    def inactive(self):
        self.active = False
        self.color = (150,150,150)

    def activate(self):
        self.active = True
        self.color = (255,0,255)
        self.colorline = (255,200,255)

    def calculate_distance_p(self,show_dist = True):
        totald = np.zeros(len(self.points))
        offsetx = .38
        for p,i in zip(self.points,range(len(self.points))):
            if show_dist:
                pygame.draw.aaline(self.win,self.colorline,(int(p.pos.x),self.yreal[int(p.pos.x)]),
                (p.pos.xy),self.lw)
            totald[i] =  p.pos.y - self.yreal[int(p.pos.x)]
        
        se = np.sum(totald**2)
        # Show the Squared Error
        ff = 22
        display_some_text(f"Intercept = {self.winhieght - self.intercept:.1f}",ff,self.winwidth*offsetx, self.winhieght - 65,self.color,self.white,self.win)
        display_some_text(f"Slope value = {self.slope*(-1):.3f}",ff,self.winwidth*offsetx, self.winhieght - 45,self.color,self.white,self.win)
        display_some_text(f"SE = {(se/1000):.1f}",ff,self.winwidth*offsetx, self.winhieght - 25,self.color,self.white,self.win)

    def ols_calculation(self):
        self.color = (0,200,0)
        self.colorline = (180,200,180)
        self.lw = 1

        Y = np.zeros(len(self.points))
        X = np.ones((len(self.points),2))
        for i in range(len(self.points)):
            Y[i] = self.points[i].pos.y
            X[i][1] = self.points[i].pos.x
        XX_1 = np.linalg.inv(np.dot(X.T,X))
        XY = np.dot(X.T,Y)
        beta = np.dot(XX_1,XY)
        self.intercept = beta[0]
        self.slope = beta[1]

        x = np.linspace(0,self.winwidth,self.winwidth)
        self.yreal = np.zeros_like(x)
        for i in range(self.winwidth):
            self.yreal[i] = self.intercept + self.slope*x[i]




