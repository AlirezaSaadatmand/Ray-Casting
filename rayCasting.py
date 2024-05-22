import pygame
from sys import exit
import random
import math

WIDTH , HEIGHT = 1300 , 700

boundary_lst = []

particle_lst = []


class Particle:
    def __init__(self , x , y):
        self.x = x
        self.y = y
        self.ray_lst = []
        for i in range(0 , 360 , 1):
            self.ray_lst.append(Ray(WIDTH/ 2 , HEIGHT/2 , math.cos(math.radians(i)) , math.sin(math.radians(i))))
            
    def show(self , pos):
        self.x , self.y = pos
        pygame.draw.circle(screen, "white" , (self.x , self.y), 10)
        
        for ray in self.ray_lst:
            dis = []
            ray.update(self.x , self.y)
            pts = ray.cast()
            if pts:

                for pt in pts:
                    dis.append(math.sqrt((self.y - pt[1])**2 + (self.x - pt[0])**2))
                pygame.draw.line(surface , (255 , 255 , 255 , 150) , (self.x , self.y) , pts[dis.index(min(dis))])

class Ray:
    def __init__(self , x , y , ix , iy):
        self.x = x
        self.y = y
        self.ix = ix
        self.iy = iy
    
    def update(self ,x , y):
        self.x = x
        self.y = y

    def cast(self):
        lst = []
        for wall in boundary_lst:
            x1 = wall.a[0]
            y1 = wall.a[1]
            x2 = wall.b[0]
            y2 = wall.b[1]
            
            x3 = self.x
            y3 = self.y
            x4 = self.x + self.ix
            y4 = self.y + self.iy
        
            den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
            if den != 0:
                t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
                u = (-1)*((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den
                if 0 < t < 1 and u > 0:
                    ptx = x1 + t * (x2 - x1)
                    pty = y1 + t * (y2 - y1)
                    lst.append((ptx , pty))
        return lst

class Boundary:
    def __init__(self , x1 , y1 , x2 , y2):
        self.a = (x1 , y1)
        self.b = (x2 , y2)
    
    def draw(self):
        pygame.draw.line(screen , "white" , self.a , self.b)
        
for _ in range(5):
    boundary_lst.append(Boundary(random.randint(0 , WIDTH) , random.randint(0 , HEIGHT) , random.randint(0 , WIDTH) , random.randint(0 , HEIGHT)))
boundary_lst.append(Boundary(0 , 0 , 0 , HEIGHT))
boundary_lst.append(Boundary(0 , 0 , WIDTH , 0))
boundary_lst.append(Boundary(WIDTH , 0 , WIDTH , HEIGHT))
boundary_lst.append(Boundary(0 , HEIGHT , WIDTH , HEIGHT))
def draw():
    pos = pygame.mouse.get_pos()
    for b in boundary_lst:
        b.draw()
    for particle in particle_lst:
        particle.show(pos)

pygame.init()
screen = pygame.display.set_mode( (WIDTH , HEIGHT)) 
surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
pygame.display.set_caption("Ray Casting")
clock = pygame.time.Clock()

while True:
    screen.fill("black")
    screen.blit(surface,(0,0))
    surface.fill("black")
    pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    if not particle_lst:
        particle_lst.append(Particle(*pos))
    draw()
    pygame.display.update()
    clock.tick(60)