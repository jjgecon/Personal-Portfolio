# By Javier Gonzalez 5/7/2020 javierj.g18@gmail.com
# CLosely following the physics and vector explanations of The Coding Train YouTube Challenge
# https://www.youtube.com/watch?v=mhjuuHl6qHM&list=WL&index=6
# This code uses https://www.red3d.com/cwr/boids/ approach to simluate boid behavior.

import pygame
import random

pygame.init()
clock = pygame.time.Clock()
run = True
winwidth, winhieght = 900,900

win = pygame.display.set_mode((winwidth,winhieght))

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',100)
    textsurf,text_rect = text_objects(text, largeText)
    text_rect.center = (winwidth//2,winhieght//2)
    win.blit(textsurf,text_rect)

    pygame.display.update()

def text_objects(text,font):
    textsurf = font.render(text, True, (255,255,255))
    return textsurf, textsurf.get_rect()


while run:

    clock.tick(30)

    keys = pygame.key.get_pressed()
    #Out check
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    message_display("text")

pygame.quit()