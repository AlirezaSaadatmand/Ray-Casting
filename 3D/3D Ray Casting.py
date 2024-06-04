import pygame
from sys import exit
import math


mainWidth , mainHeight = 1200 , 700

WIDTH , HEIGHT = 500 , 500

PIXEL_UNIT = 1

FIELD_OF_VIEW = 140

boundary_lst = []

particle_lst = []

block_lst = []

ground_lst = []

MAP = [
        [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0],
        [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0],
        [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0],
        [0 , 0 , 0 , 0 , 1 , 0 , 1 , 0 , 0],
        [0 , 0 , 1 , 0 , 1 , 0 , 1 , 0 , 0],
        [0 , 0 , 1 , 0 , 0 , 0 , 1 , 0 , 0],
        [0 , 0 , 1 , 0 , 1 , 1 , 1 , 0 , 0],
        [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0]
                                            ]

X_UNIT = WIDTH / (len(MAP[0]))
Y_UNIT = HEIGHT / (len(MAP))

class Particle:
    def __init__(self , x , y):
        self.x = x
        self.y = y
        self.main_ray_lst = []
        self.ray_lst = []
        
        self.goingForward = False
        self.goingBackward = False
        self.goingRight = False
        self.goingLeft = False
        
        self.turningRight = False
        self.turningLeft = False
        
        self.startView = FIELD_OF_VIEW // 2
        
        self.fullAngle = 360
        
        self.mutipule = 2
        
        for i in range(0 , self.fullAngle * self.mutipule , 1):
            i /= self.mutipule
            
            self.ray_lst.append(Ray(WIDTH/ 2 , HEIGHT/2 , math.cos(math.radians(i)) , math.sin(math.radians(i)) , i))
    
    def update_pos(self):
        self.main_ray_lst = []
        
        if self.turningLeft:
            self.startView -= self.mutipule
            if self.startView - self.mutipule < 0:
                self.startView = self.fullAngle * self.mutipule
            
        if self.turningRight:
            self.startView += self.mutipule
            if self.startView + self.mutipule > self.fullAngle * self.mutipule:
                self.startView = 0
            
        start = self.startView - FIELD_OF_VIEW // 2
        if start < 0:
            start = self.fullAngle * self.mutipule + start
        end = self.startView + FIELD_OF_VIEW // 2
        if end > self.fullAngle * self.mutipule:
            end = end - self.fullAngle * self.mutipule

        count2 = start
        c = 0
        while c < FIELD_OF_VIEW:
            count2 += 1
            if count2 + 1 > self.fullAngle * self.mutipule:
                count2 = 0

            self.main_ray_lst.append(self.ray_lst[count2])
            c += 1

# ======================================= Movement ==================================
        
        count = 0
        for i in [self.goingForward , self.goingBackward , self.goingRight , self.goingLeft]:
            if i == True:
                count += 1
        if count == 2:
            if self.goingForward and self.goingRight:
                self.y += math.sin(math.radians(self.startView//2 + 45)) * PIXEL_UNIT
                self.x += math.cos(math.radians(self.startView//2 + 45)) * PIXEL_UNIT
            if self.goingForward and self.goingLeft:
                self.y += math.sin(math.radians(self.startView//2 - 45)) * PIXEL_UNIT
                self.x += math.cos(math.radians(self.startView//2 - 45)) * PIXEL_UNIT
            if self.goingBackward and self.goingRight:
                self.y -= math.sin(math.radians(self.startView//2 - 45)) * PIXEL_UNIT
                self.x -= math.cos(math.radians(self.startView//2 - 45)) * PIXEL_UNIT
            if self.goingBackward and self.goingLeft:
                self.y -= math.sin(math.radians(self.startView//2 + 45)) * PIXEL_UNIT
                self.x -= math.cos(math.radians(self.startView//2 + 45)) * PIXEL_UNIT

        if count == 1:
            
            if self.goingForward:
                self.y += math.sin(math.radians(self.startView//2)) * PIXEL_UNIT
                self.x += math.cos(math.radians(self.startView//2)) * PIXEL_UNIT
            if self.goingBackward:
                self.y -= math.sin(math.radians(self.startView//2)) * PIXEL_UNIT
                self.x -= math.cos(math.radians(self.startView//2)) * PIXEL_UNIT
            if self.goingRight:
                self.y += math.sin(math.radians(self.startView//2 + 90)) * PIXEL_UNIT
                self.x += math.cos(math.radians(self.startView//2 + 90)) * PIXEL_UNIT
            if self.goingLeft:
                self.y += math.sin(math.radians(self.startView//2 - 90)) * PIXEL_UNIT
                self.x += math.cos(math.radians(self.startView//2 - 90)) * PIXEL_UNIT
                
    def show(self):

        pygame.draw.circle(screen, "white" , (self.x , self.y), 7)

        for ray in self.main_ray_lst:
            dis = []
            ray.update(self.x , self.y)
            pts = ray.cast()
            if pts:

                for pt in pts:
                    dis.append(math.sqrt((self.y - pt[1])**2 + (self.x - pt[0])**2))
                    
                unit = 700 // FIELD_OF_VIEW 
                if HEIGHT / min(dis) * 20 < HEIGHT:
                    sur = pygame.Surface( (unit , HEIGHT / min(dis) * 20) )
                else:
                    sur = pygame.Surface( (unit , HEIGHT) )
                if min(dis) < 240:
                    code = 255 - min(dis)
                else:
                    code = 15
                sur.fill((code , code , code))
                sur_rect = sur.get_rect(center = (WIDTH + self.main_ray_lst.index(ray) * unit + unit / 2  , mainHeight // 2))
                surface.blit(sur , sur_rect)
                if ray.id == self.startView//2:
                    pygame.draw.line(surface , (255 , 0 , 0 , 150) , (self.x , self.y) , pts[dis.index(min(dis))])
                else:
                    pygame.draw.line(surface , (255 , 255 , 255 , 150) , (self.x , self.y) , pts[dis.index(min(dis))])
class Ray:
    def __init__(self , x , y , ix , iy , id):
        self.x = x
        self.y = y
        self.ix = ix
        self.iy = iy
        
        self.id = id
    
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

boundary_lst.append(Boundary(0 , mainHeight//2 - HEIGHT//2 , 0 , mainHeight//2 + HEIGHT//2))
boundary_lst.append(Boundary(0 , mainHeight//2 - HEIGHT//2 , WIDTH , mainHeight//2 - HEIGHT//2))
boundary_lst.append(Boundary(WIDTH , mainHeight//2 - HEIGHT//2 , WIDTH , mainHeight//2 + HEIGHT//2))
boundary_lst.append(Boundary(0 , mainHeight//2 + HEIGHT//2 , WIDTH , mainHeight//2 + HEIGHT//2))

def draw():
    for ground in ground_lst:
        surface.blit(ground[0] , ground[1])
    for b in boundary_lst:
        b.draw()
    for block in block_lst:
        screen.blit(block[0] , block[1])
    PLAYER.update_pos()
    PLAYER.show()

pygame.init()
screen = pygame.display.set_mode( (mainWidth , mainHeight)) 
surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
pygame.display.set_caption("Ray Casting")
clock = pygame.time.Clock()

for i in range(0 , 124):
    unit = HEIGHT//2 // 100
    ground_sur = pygame.Surface( (700 , unit) )
    ground_sur_rect = ground_sur.get_rect(topleft = (WIDTH , mainHeight//2 + i * unit))
    if i < 100:
        ground_sur.fill((55 + i * 2 , 25 + i * 2, 0))
    else:
        ground_sur.fill((255 , 225 , 0))
        
    ground_lst.append([ground_sur , ground_sur_rect])


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
                PLAYER.goingForward = True
            if event.key == pygame.K_s :
                PLAYER.goingBackward = True
            if event.key == pygame.K_d :
                PLAYER.goingRight = True
            if event.key == pygame.K_a :
                PLAYER.goingLeft = True
                
            if event.key == pygame.K_LEFT:
                PLAYER.turningLeft = True
            if event.key == pygame.K_RIGHT:
                PLAYER.turningRight = True
                          
        if event.type  == pygame.KEYUP:
            if event.key == pygame.K_w:
                PLAYER.goingForward = False
            if event.key == pygame.K_s:
                PLAYER.goingBackward = False
            if event.key == pygame.K_d:
                PLAYER.goingRight = False
            if event.key == pygame.K_a:
                PLAYER.goingLeft = False
            
            if event.key == pygame.K_RIGHT:
                PLAYER.turningRight = False
            if event.key == pygame.K_LEFT:
                PLAYER.turningLeft = False
                
    if not particle_lst:
        particle_lst.append(1)
        PLAYER = Particle(50 , 250)
    draw()
    pygame.display.update()
    clock.tick(60)