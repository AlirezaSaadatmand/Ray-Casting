import pygame
from sys import exit
import random

WIDTH , HEIGHT = 1000 , 600

boundary_lst = []

particle_lst = []

class Particle:
    def __init__(self , x , y):
        self.x = x
        self.y = y
    def update(self , pos):
        self.x , self.y = pos
    def show(self):
        pygame.draw.circle(screen, "white" , (self.x , self.y), 10)
        
class Boundary:
    def __init__(self , x1 , y1 , x2 , y2):
        self.a = (x1 , y1)
        self.b = (x2 , y2)
    
    def draw(self):
        pygame.draw.line(screen , "white" , self.a , self.b)
        
for _ in range(5):
    boundary_lst.append(Boundary(random.randint(0 , WIDTH) , random.randint(0 , WIDTH) , random.randint(0 , HEIGHT) , random.randint(0 , HEIGHT)))
        
def draw():
    pos = pygame.mouse.get_pos()
    for b in boundary_lst:
        b.draw()
    for particle in particle_lst:
        particle.update(pos)
        particle.show()
        
pygame.init()
screen = pygame.display.set_mode( (WIDTH , HEIGHT) ) 
pygame.display.set_caption("Ray Casting")
clock = pygame.time.Clock()

while True:
    screen.fill("black")
    pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    if not particle_lst:
        particle_lst.append(Particle(*pos))
    draw()
    pygame.display.update()
    clock.tick()