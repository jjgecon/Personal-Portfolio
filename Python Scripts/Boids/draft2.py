# By Javier Gonzalez
# CLosely following the physics and vector explanations of The Coding Train YouTube Challenge
# https://www.youtube.com/watch?v=mhjuuHl6qHM&list=WL&index=6

import pygame
import random

pygame.init()
clock = pygame.time.Clock()
run = True
winwidth, winhieght = 900,900
win = pygame.display.set_mode((winwidth,winhieght))
white = (255,255,255)

class Boid():
    def __init__(self,color,win):
        self.color = color
        self.win = win
        self.v = pygame.math.Vector2(random.uniform(-.5, .5),random.uniform(-.5, .5)) # Velocity in x and y
        self.a = pygame.math.Vector2(random.uniform(-.1, .1),random.uniform(-.1, .1)) # Acceleration in x and y
        self.position = pygame.math.Vector2(random.uniform(0, winwidth),random.uniform(0, winhieght)) #Center of the boid
        self.steeringpos = self.a
        self.steeringv = self.a
        self.visionRadious = 50
        self.MaxForce = 4

    def draw(self):
        pygame.draw.line(self.win, self.color,(self.position.xy),(self.position.xy+4*self.v.xy),2)
        pygame.draw.circle(self.win, self.color, (int(self.position.x),int(self.position.y)), 10)
        if self.position.x <= 0:
            self.position.x = winwidth
        elif self.position.x >= winwidth:
            self.position.x = 0
        if self.position.y <= 0:
            self.position.y = winhieght
        elif self.position.y >= winhieght:
            self.position.y = 0

    def get_nearby_boids(self,BOID_LIST):
        self.visual = []
        for b in BOID_LIST:
            distance = self.position - b.position
            if distance.magnitude() <= self.visionRadious and b != self and \
               (distance.angle_to(self.v) < -50 or distance.angle_to(self.v) > 50):
                self.visual.append(b)
    
    def cohesion(self):
        self.steeringpos = pygame.math.Vector2()
        for vboid in self.visual:
            self.steeringpos += vboid.position
        
        if not self.visual:
            pass
        else:
            self.steeringpos = self.steeringpos/len(self.visual)
            self.mean_p = self.steeringpos
            self.steeringpos = self.steeringpos - self.position
            self.steeringpos.scale_to_length(self.MaxForce)
            self.steeringpos = self.steeringpos - self.v
            self.steeringpos.normalize_ip()
    
    def aling(self):
        self.steeringv = pygame.math.Vector2()
        if not self.visual:
            pass
        else:
            for vboid in self.visual:
                self.steeringv += vboid.v
            
            self.steeringv = self.steeringv/len(self.visual)
            self.steeringv = self.steeringv - self.v
            self.steeringv.normalize_ip()


    def visualize(self, chn = True):
        # Draw the local circle
        pygame.draw.circle(self.win, self.color, (int(self.position.x),int(self.position.y)), self.visionRadious,1)
        
        # Draw mean position
        if not self.visual:
            pass
        elif chn:
            pygame.draw.circle(self.win,(200,0,0),(int(self.mean_p.x),int(self.mean_p.y)),7)
        
        # Draw nearby boids
        for vboid in self.visual:
            pygame.draw.line(win, white,(self.position.xy),(vboid.position.xy))

    def update(self):
        # Cohesion
        # self.a = self.a.lerp(self.steeringpos,1)
        # Aling
        # self.a = self.a.lerp(self.steeringv,.2)

        self.position = self.position.lerp(self.position + self.v,.8)
        self.v =  self.v.lerp(self.v + self.a,.8)
        self.v.scale_to_length(self.MaxForce)
        self.draw()

# Main Drawing Function
def re_draw_gw(current, vis = True):
    win.fill((0,0,0)) # Use a black bg
    for b in boid_list:
        b.update()
        b.get_nearby_boids(boid_list)
        # b.cohesion()
        # b.aling()

    if vis:
        boid_list[current].visualize(chn=True)

    pygame.display.update()

# Create objects
n_boids = 80
boid_list = []
cc = 0
vis = True

for i in range(n_boids):
    boid_list.append(Boid((0,random.randint(150,255),0),win))

while run:

    clock.tick(30)
    keys = pygame.key.get_pressed()
    #Out check
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Turn on/off visualization
    if keys[pygame.K_UP]:
        vis = True
    if keys[pygame.K_DOWN]:
        vis = False
    # Cicle through boids visualization
    if keys[pygame.K_RIGHT]:
        if cc == n_boids-1:
            cc = 0
        else:
            cc += 1
    if keys[pygame.K_LEFT]:
        if cc == 0:
            cc = n_boids-1
        else:
            cc -= 1

    re_draw_gw(cc,vis)

pygame.quit()