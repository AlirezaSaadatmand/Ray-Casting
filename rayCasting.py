import pygame
from sys import exit

WIDTH , HEIGHT = 1000 , 600

boundary_lst = []

class Boundary:
    def __init__(self , x1 , y1 , x2 , y2):
        self.a = (x1 , y1)
        self.b = (x2 , y2)
    
    def draw(self):
        pygame.draw.line(screen , "white" , self.a , self.b)
        
boundary_lst.append(Boundary(300 , 300 , 500 , 500))
        
def draw():
    for b in boundary_lst:
        b.draw()
        
pygame.init()
screen = pygame.display.set_mode( (WIDTH , HEIGHT) ) 
pygame.display.set_caption("Ray Casting")
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    draw()
    pygame.display.update()
    clock.tick()