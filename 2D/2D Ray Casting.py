import pygame
from sys import exit
import random
import math

WIDTH , HEIGHT = 700 , 700

PIXEL_UNIT = 3

boundary_lst = []

particle_lst = []

block_lst = []

MAP = [
        [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0],
        [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0],
        [0 , 0 , 0 , 0 , 1 , 0 , 0 , 0 , 0],
        [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0],
        [0 , 0 , 0 , 1 , 0 , 1 , 0 , 0 , 0],
        [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0],
        [0 , 0 , 0 , 0 , 1 , 0 , 0 , 0 , 0],
        [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0]
                                            ]

X_UNIT = WIDTH / (len(MAP[0]))
Y_UNIT = HEIGHT / (len(MAP))

class Particle:
    def __init__(self , x , y):
        self.x = x
        self.y = y
        self.main_ray_lstt = []
        self.ray_lst = []
        
        self.goingup = False
        self.goingdown = False
        self.goingright = False
        self.goingleft = False
        
        for i in range(0 , 360 , 1):
            if i < 360:
                self.main_ray_lstt.append(Ray(WIDTH/ 2 , HEIGHT/2 , math.cos(math.radians(i)) , math.sin(math.radians(i))))
            self.ray_lst.append(Ray(WIDTH/ 2 , HEIGHT/2 , math.cos(math.radians(i)) , math.sin(math.radians(i))))
    
    def update_pos(self):
        count = 0
        for i in [self.goingup , self.goingdown , self.goingright , self.goingleft]:
            if i == True:
                count += 1
        if count == 2:
            if self.goingup and self.goingright:
                self.x += PIXEL_UNIT
                self.y -= PIXEL_UNIT
            if self.goingup and self.goingleft:
                self.x -= PIXEL_UNIT
                self.y -= PIXEL_UNIT
            if self.goingdown and self.goingright:
                self.x += PIXEL_UNIT
                self.y += PIXEL_UNIT
            if self.goingdown and self.goingleft:
                self.x -= PIXEL_UNIT
                self.y += PIXEL_UNIT
        if count == 1:
            if self.goingup:
                self.y -= (2*(PIXEL_UNIT**2))**0.5
            if self.goingdown:
                self.y += (2*(PIXEL_UNIT**2))**0.5
            if self.goingright:
                self.x += (2*(PIXEL_UNIT**2))**0.5
            if self.goingleft:
                self.x -= (2*(PIXEL_UNIT**2))**0.5
                
    def show(self):

        pygame.draw.circle(screen, "white" , (self.x , self.y), 10)
        
        for ray in self.main_ray_lstt:
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

def block(xindex , yindex):
    x = X_UNIT * xindex
    y = Y_UNIT * yindex
    
    sur = pygame.Surface( (X_UNIT , Y_UNIT) )
    sur.fill("white")
    sur_rect = sur.get_rect(topleft = (x , y))
    block_lst.append([sur , sur_rect])
    if yindex != 0:
        if MAP[yindex - 1][xindex] != 1:
            boundary_lst.append(Boundary(x , y , x + X_UNIT , y))
    if xindex != len(MAP[0]) - 1 :
        if MAP[yindex][xindex + 1] != 1:
            boundary_lst.append(Boundary(x + X_UNIT , y , x + X_UNIT , y + Y_UNIT))
    if yindex != len(MAP) - 1:
        if MAP[yindex + 1][xindex] != 1:
            boundary_lst.append(Boundary(x + X_UNIT , y + Y_UNIT , x , y + Y_UNIT))
    if xindex != 0:
        if MAP[yindex][xindex - 1] != 1:
            boundary_lst.append(Boundary(x , y , x , y + Y_UNIT))

for yindex , row in enumerate(MAP):
    for xindex , column in enumerate(row):
        if column == 1:
            block(xindex , yindex)

boundary_lst.append(Boundary(0 , 0 , 0 , HEIGHT))
boundary_lst.append(Boundary(0 , 0 , WIDTH , 0))
boundary_lst.append(Boundary(WIDTH , 0 , WIDTH , HEIGHT))
boundary_lst.append(Boundary(0 , HEIGHT , WIDTH , HEIGHT))

def draw():
    for b in boundary_lst:
        b.draw()
    for block in block_lst:
        screen.blit(block[0] , block[1])
    PLAYER.update_pos()
    PLAYER.show()

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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                PLAYER.goingup = True
            if event.key == pygame.K_s :
                PLAYER.goingdown = True
            if event.key == pygame.K_d :
                PLAYER.goingright = True
            if event.key == pygame.K_a :
                PLAYER.goingleft = True
                          
        if event.type  == pygame.KEYUP:
            if event.key == pygame.K_w:
                PLAYER.goingup = False
            if event.key == pygame.K_s:
                PLAYER.goingdown = False
            if event.key == pygame.K_d:
                PLAYER.goingright = False
            if event.key == pygame.K_a:
                PLAYER.goingleft = False
    if not particle_lst:
        particle_lst.append(1)
        PLAYER = Particle(WIDTH/2 , HEIGHT/2)
    draw()
    pygame.display.update()
    clock.tick(60)