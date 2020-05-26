# By Javier Gonzalez 5/24/2020 javierj.g18@gmail.com
# A small visualiztion to understand better how do simple linear regresions work

import pygame
from pygame import gfxdraw
import random
import numpy as np
from ols_vis import display_some_text
from ols_vis import Line
from ols_vis import Point

pygame.init()
clock = pygame.time.Clock()
run = True
winwidth, winhieght = 800,800

win = pygame.display.set_mode((winwidth,winhieght))

white = (255,255,255)
black = (0,0,0)

def draw(points):
    win.fill(white) 
    ff = 15

    if lines:
        for l in lines:
            l.show()
            if l.active:
                l.calculate_distance_p(show_d)
            
    
    if ols_list:
        ols_list[0].show()
        ols_list[0].calculate_distance_p(show_d)

    for d in points:
        d.show()
        if display_point_t:
            d.text_point()
        
    # Some instructions to stay on the screen
    pygame.draw.rect(win,white,(0,winhieght-70,winwidth*(.28),winhieght-70))
    pygame.draw.rect(win,white,(winwidth*(.69),winhieght-70,winwidth*(.3),winhieght-70))
    display_some_text("Press 'd' to substract points",ff,20, winhieght-20,black,white,win)
    display_some_text("Press 'a' to add points",ff,20, winhieght-40,black,white,win)
    display_some_text("Press 'i' to show distantance",ff,20, winhieght-60,black,white,win)
    display_some_text("Press 'x' to hide point location",ff,winwidth*(.7), winhieght-20,black,white,win)
    display_some_text("Press 's' to show point location",ff,winwidth*(.7), winhieght-40,black,white,win)
    display_some_text("Press 'o' to hide distantance",ff,winwidth*(.7), winhieght-60,black,white,win)

    pygame.display.update()

# some booleans to hide and show features
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
        data.append(Point(rx,ry,win,winhieght))

    lines = []
    n_lines = 22

    ols_list = []

    while run:

        clock.tick(15)

        keys = pygame.key.get_pressed()
        #Out check
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Explore lines
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
        
        # Reset Points
        if keys[pygame.K_r]:
            resetpoints = True

        # Show Different Slopes
        if keys[pygame.K_LEFT]:
            slopes = True

        # Show Different Intercepts
        if keys[pygame.K_RIGHT]:
            intercept = True

        # Show OLS Solution
        if keys[pygame.K_SPACE]:
            ols = True

        # Display point locations
        if keys[pygame.K_s]:
            display_point_t = True
        if keys[pygame.K_x]:
            display_point_t = False

        # Increase Decrease Data
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
        
        # Hide all Lines
        if keys[pygame.K_c]:
            lines = []
            ols_list = []
        
        # Show distance between lines and points
        if keys[pygame.K_i]:
            show_d = True
        if keys[pygame.K_o]:
            show_d = False

        if ols:
            lines = []
            ols_list.append(Line(1,1,win,winwidth,winhieght,data))
            ols_list[0].ols_calculation()
            ols = False

        if resetpoints:
            data = []
            for i in range(n):
                rx = int(random.uniform(20,winwidth-70))
                ry = int(random.uniform(20,winhieght-70))
                data.append(Point(rx,ry,win,winhieght))
            resetpoints = False
            if ols_list:
                ols_list = []
                ols_list.append(Line(1,1,win,winwidth,winhieght,data))
                ols_list[0].ols_calculation()

        if intercept:
            ols_list = []
            lines = []
            for i in range(n_lines):
                lines.append(Line(.2,30*i,win,winwidth,winhieght,data))
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
                lines.append(Line(s,winhieght//2,win,winwidth,winhieght,data))
                lines[i].inactive()
            lines[0].activate()

            ols = False
            slopes = False
            intercept = False
        
        draw(data)

    pygame.quit()


