# Platformer 3
import pygame, sys, random
from pygame.locals import *
BOARDHEIGHT = BOARDWIDTH = 20
SQUAREHEIGHT = SQUAREWIDTH = 20
WINDOWHEIGHT = BOARDHEIGHT * SQUAREHEIGHT
WINDOWWIDTH = BOARDWIDTH * SQUAREWIDTH
DISPLAYWIDTH = DISPLAYHEIGHT = (WINDOWWIDTH * 3)//2
PLAYERHEIGHT = 15
PLAYERWIDTH = 15
PLAYERSPEED = 1
SHADOWSPEED = 1
ENEMYSPEED = 1
TERMINALVEL = 4
JUMPVEL = 5
SOLIDTILES = ['1','P','b','g','m']
#JUMPVEL = 15
WEIGHT = 0.5
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
TEXTCOLOR = (200,200,200)
GREY = (200,100,100)
FPS = 60


def terminate():
    pygame.quit()
    sys.exit()
def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return
def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x,y)
    surface.blit(textobj,textrect)

pygame.init()
main_clock = pygame.time.Clock()
#screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
window_surface = pygame.display.set_mode((DISPLAYWIDTH,DISPLAYHEIGHT))
screen = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT))
font = pygame.font.SysFont(None, 48)
#pygame.mixer.music.load('music.mid') (add music here)

'''static_images = []
for i in range(2*SQUAREWIDTH):
    frame_surface = pygame.Surface((2*SQUAREWIDTH,2*SQUAREHEIGHT))
    pygame.draw.lines(frame_surface, (255,255,255), 0, ((i,0),(0,i)))
    static_surface = pygame.Surface((SQUAREWIDTH, SQUAREHEIGHT))
    static_surface.blit(frame_surface, (0,0), (0,0,SQUAREWIDTH,SQUAREHEIGHT))
    static_images.append(static_surface)

static_images = []
for i in range(2*SQUAREWIDTH):
    static_surface = pygame.Surface((SQUAREWIDTH, SQUAREHEIGHT))
    pygame.draw.lines(static_surface, (255,255,255), 0, ((i,0),(0,i)))
    pygame.draw.lines(static_surface, (255,255,255), 0, ((SQUAREWIDTH-i,SQUAREWIDTH),(SQUAREWIDTH,SQUAREWIDTH-i)))
    static_images.append(static_surface)'''
cloud_image = pygame.image.load('cloud.png')
wood_image = pygame.image.load('wood.png')
static_image = pygame.image.load('static.png')
static_image_2 = pygame.image.load('static_2.png')
spinner_image = pygame.image.load('spinner.png')
#spinner_image.set_masks((255, 65280, 16711680, 0))
walker_image = pygame.image.load('walker.png')
flyer_image = pygame.image.load('evil_eye.png')
exit_image = pygame.image.load('exit.png')
button_image = pygame.image.load('button.png')
pushed_button_image = pygame.image.load('pushed_button.png')
closed_image = pygame.image.load('closed.png')
open_image = pygame.image.load('open.png')
button_image_B = pygame.image.load('button_B.png') #blue button
button_image_G = pygame.image.load('button_G.png') #green
button_image_M = pygame.image.load('button_M.png') #magenta
button_images = {'B': button_image_B,
                 'G': button_image_G,
                 'M': button_image_M}
closed_image_B = pygame.image.load('closed_B.png')
closed_image_G = pygame.image.load('closed_G.png')
closed_image_M = pygame.image.load('closed_M.png')
closed_images = {'b': closed_image_B,
                 'g': closed_image_G,
                 'm': closed_image_M}
"""open_image_B = pygame.image.load('closed_M.png')
open_image_G = pygame.image.load('closed_M.png')
open_image_M = pygame.image.load('closed_M.png')
open_images = {'B': open_image_B,
                 'G': open_image_G,
                 'M': open_image_M}"""
shadow_image_B = pygame.image.load('shadow_B.png')
shadow_image_G = pygame.image.load('shadow_G.png')
shadow_image_M = pygame.image.load('shadow_M.png')
shadow_images = {'C': shadow_image_B,
                 'H': shadow_image_G,
                 'N': shadow_image_M}

images = [static_image,static_image_2,walker_image,spinner_image,flyer_image,cloud_image,wood_image,open_image,pushed_button_image]
for x in shadow_images: images.append(shadow_images[x])
for x in closed_images: images.append(closed_images[x])
for x in button_images: images.append(button_images[x])
for image in images:
    image.set_colorkey((0,0,0))
    a,b,c,d = image.get_masks()

    image.set_masks((a,b,c,0))
    image.convert_alpha()
    
    image.convert_alpha()

'''button_image.set_colorkey(BLACK)
pushed_button_image.convert()
pushed_button_image.set_colorkey(BLACK)
pushed_button_image.convert()
button_image.convert()
button_image.set_colorkey(BLACK)
button_image.convert()'''
def letter_to_number(string):
    if string in['B','b','C']:
        return 0
    elif string in ['G','g','H']:
        return 1
    elif string in ['M','m','N']:
        return 2
def copy(matrix):
    copy = []
    for row in matrix:
        copy.append(row)
    return copy

def toggle(x,y,level, entities):
    #x,y are board positions
    anvil = level
    if level[y][x] not in ('1', 'P', 'C', 'D', '.', 'E') and check_if_empty(x,y,entities):
        anvil[y][x] = '1'
    elif level[y][x] == '1':
        anvil[y][x] = ' '
    return anvil

def check_if_empty(x,y,entities):
    rectangle = pygame.Rect(x*SQUAREWIDTH, y*SQUAREHEIGHT, SQUAREWIDTH, SQUAREHEIGHT)
    for e in entities:
        if e.rect.colliderect(rectangle):
            return False
    return True
###title screen:
#drawText('Platformer 3', font, screen, 0,0)
#pygame.display.update()
#waitForPlayerToPressKey()

class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)    

class Platform(Entity):
    def __init__(self,x,y,color):
        Entity.__init__(self)
        self.x = x
        self.y = y
        self.image = pygame.Surface((SQUAREHEIGHT, SQUAREWIDTH))
        self.image.fill(color)
        self.rect = pygame.Rect(x,y,SQUAREWIDTH,SQUAREHEIGHT)

class Button(Entity):
    def __init__(self,x,y,hue):
        Entity.__init__(self)
        self.hue = hue
        self.image = button_images[hue]
        self.rect = pygame.Rect(x,y,SQUAREWIDTH, SQUAREHEIGHT)

class Flyer(Entity):
    
    def __init__(self,x,y, facing = 'up'):
        Entity.__init__(self)
        self.x = x
        self.y = y
        self.facing = facing
        self.xvel = self.yvel = 0
        self.image = flyer_image
        self.rect = pygame.Rect(x,y,SQUAREWIDTH,SQUAREHEIGHT+1)

    def board_location_left(self):
            xpos = self.rect.left//SQUAREWIDTH
            ypos = self.rect.centery//SQUAREHEIGHT
            return (xpos, ypos)

    def board_location_right(self):
            xpos = (self.rect.right-1)//SQUAREWIDTH
            ypos = self.rect.centery//SQUAREHEIGHT
            return (xpos, ypos)

    def update(self, level):
        if self.facing == 'down': self.yvel = ENEMYSPEED
        else: self.yvel = -ENEMYSPEED
        yvel = self.yvel
        self.rect.top += yvel  # used to move_ip
        self.collide(0,yvel,level)

    def collide(self, xvel, yvel, level):
        a,b = self.board_location_left()
        for x in range(0,20):
            for y in range(0,20):
                if level[y][x] in SOLIDTILES:
                    rectangle = pygame.Rect(x*SQUAREWIDTH,y*SQUAREHEIGHT, SQUAREWIDTH,SQUAREHEIGHT)
                    
                    if self.rect.colliderect(rectangle):
                        if yvel > 0:
                            self.rect.bottom = rectangle.top
                            self.yvel = -self.yvel
                            self.facing = 'up'
                        elif yvel < 0:
                            self.rect.top = rectangle.bottom
                            self.yvel = -self.yvel
                            self.facing = 'down'
    
class Enemy(Entity):
    def __init__(self,x,y, facing = 'right'):
        Entity.__init__(self)
        self.x = x
        self.y = y
        self.facing = facing
        self.xvel = self.yvel = 0
        self.image = spinner_image
        self.rect = pygame.Rect(x,y,SQUAREWIDTH+1,SQUAREHEIGHT)

    def board_location_left(self):
            xpos = self.rect.left//SQUAREWIDTH
            ypos = self.rect.centery//SQUAREHEIGHT
            return (xpos, ypos)

    def board_location_right(self):
            xpos = (self.rect.right-1)//SQUAREWIDTH
            ypos = self.rect.centery//SQUAREHEIGHT
            return (xpos, ypos)

    def update(self, level):
        if self.facing == 'right': self.xvel = ENEMYSPEED
        else: self.xvel = -ENEMYSPEED
        xvel = self.xvel
        self.rect.left += xvel  # used to move_ip
        self.collide(xvel,0,level)

    def collide(self, xvel, yvel, level):
        a,b = self.board_location_left()
        for x in range(0,20):
            for y in range(0,20):
                if level[y][x] in SOLIDTILES:
                    rectangle = pygame.Rect(x*SQUAREWIDTH,y*SQUAREHEIGHT, SQUAREWIDTH,SQUAREHEIGHT)
                    
                    if self.rect.colliderect(rectangle):
                        if xvel > 0:
                            self.rect.right = rectangle.left
                            self.xvel = -self.xvel
                            self.facing = 'left'
                        elif xvel < 0:
                            self.rect.left = rectangle.right
                            self.xvel = -self.xvel
                            self.facing = 'right'
                        if yvel > 0:
                            self.rect.bottom = rectangle.top
                            self.grounded = True
                            self.yvel = 0
                            
                        elif yvel < 0:
                            self.rect.top = rectangle.bottom
                            self.yvel = 0        
        
        

class Player(Entity):
    def __init__(self,x,y, dead):
        Entity.__init__(self)
        self.xvel = self.yvel = 0
        self.x = x
        self.y = y
        self.dead = dead
        self.grounded = False
        self.image = pygame.Surface((PLAYERWIDTH, PLAYERHEIGHT))
        self.image.fill((255,255,255))
        self.image.convert()
        self.rect = pygame.Rect(x,y,PLAYERWIDTH,PLAYERHEIGHT)
        self.facing = 'right'
        
    def board_location_left(self):
            xpos = self.rect.left//SQUAREWIDTH
            ypos = self.rect.centery//SQUAREHEIGHT
            return (xpos, ypos)

    def board_location_right(self):
            xpos = (self.rect.right-1)//SQUAREWIDTH
            ypos = self.rect.centery//SQUAREHEIGHT
            return (xpos, ypos)
        
    def update(self, up, left, right, level, enemies):
        if up:
            if self.grounded: self.yvel -= JUMPVEL
        if left:
            self.xvel = -PLAYERSPEED
        if right:
            self.xvel = PLAYERSPEED
        if not self.grounded and self.yvel < TERMINALVEL:
            self.yvel += WEIGHT
        if not (left or right):
            self.xvel = 0
        
        self.rect.left += self.xvel
        self.collide(self.xvel,0,level)
        self.rect.top += self.yvel
        self.grounded = False
        self.collide(0,self.yvel,level)

        self.threats(enemies)

    def collide(self, xvel, yvel, level):
        a,b = self.board_location_left()
        for x in range(0,20):
            for y in range(0,20):
                if level[y][x] in SOLIDTILES:
                    rectangle = pygame.Rect(x*SQUAREWIDTH,y*SQUAREHEIGHT, SQUAREWIDTH,SQUAREHEIGHT)
                    
                    if self.rect.colliderect(rectangle):
                        if xvel > 0:
                            self.rect.right = rectangle.left
                        elif xvel < 0:
                            self.rect.left = rectangle.right
                        if yvel > 0:
                            self.rect.bottom = rectangle.top
                            self.grounded = True
                            self.yvel = 0
                            
                        elif yvel < 0:
                            self.rect.top = rectangle.bottom
                            self.yvel = 0

    def threats(self, enemies):
        for e in enemies:
            if self.rect.colliderect(e.rect):
                self.dead = True

class Walker(Entity):
    def __init__(self,x,y,facing='right'):
        Entity.__init__(self)
        self.x = x
        self.y = y
        self.xvel = SHADOWSPEED
        self.yvel = SHADOWSPEED
        self.image = walker_image
        self.image.convert()
        self.rect = pygame.Rect(x,y,SQUAREWIDTH,SQUAREHEIGHT)
        self.facing = facing
        self.grounded = False
        self.falling = True

    def board_location_left(self):
            xpos = self.rect.left//SQUAREWIDTH
            ypos = self.rect.centery//SQUAREHEIGHT
            return (xpos, ypos)

    def update(self, level):
        
        xvel, yvel = self.xvel, self.yvel
        if self.grounded:
            if self.facing == 'right': self.xvel = SHADOWSPEED
            else: self.xvel = -SHADOWSPEED
            self.rect.move_ip(xvel,0)
            self.collide(xvel,0,level)
        else:
            self.rect.move_ip(0, yvel) # FALLING
            self.collide(0,yvel,level)
        self.grounded = False

        if not self.falling:
            self.rect.left += self.xvel
            self.collide(self.xvel,0,level)
        self.rect.top += self.yvel
        self.grounded = False
        self.collide(0,self.yvel,level)

    def collide(self, xvel, yvel, level):
        a,b = self.board_location_left()
        self.falling = True
        for x in range(0,20):
            for y in range(0,20):
                if level[y][x] in SOLIDTILES:
                    rectangle = pygame.Rect(x*SQUAREWIDTH,y*SQUAREHEIGHT, SQUAREWIDTH,SQUAREHEIGHT)
                    
                    if self.rect.colliderect(rectangle):
                        if xvel > 0:
                            self.rect.right = rectangle.left
                            self.xvel = -self.xvel
                            self.facing = 'left'
                        elif xvel < 0:
                            self.rect.left = rectangle.right
                            self.xvel = -self.xvel
                            self.facing = 'right'
                        if yvel > 0:
                            self.rect.bottom = rectangle.top
                            self.grounded = True
                            #self.yvel = 0
                            self.falling = False
                            
                        elif yvel < 0:
                            self.rect.top = rectangle.bottom
                            self.yvel = 0
                            
class Shadow(Walker):
    def __init__(self,x,y,hue,facing='right'):
        Walker.__init__(self,x,y,facing)
        self.hue = hue
        self.image = shadow_images[hue]

        
    

maps = (
    (
    "PPPPPPPPPPPPPPPPPPPP",
    "P                  P",
    "P  PPP            EP",
    "P               PPPP",
    "P                  P",
    "P                  P",
    "P        PPP       P",
    "P                  P",
    "P  PPP             P",
    "P                  P",
    "P          PPP     P",
    "P                  P",
    "P                  P",
    "P      PPP         P",
    "P                  P",
    "PPPPPPPPPPPP       P",
    "P          P     PPP",
    "P          1   PPPPP",
    "PS   P     1   PPPPP",
    "PPPPPPPPPPPPPPPPPPPP",
    ),
            (
    "PPPPPPPPPPPPPPPPPPPP",
    "PPE                P",
    "PPPPP              P",
    "PPPPPPPP11111111111P",
    "PPPPP             2P",
    "PP                 P",
    "P                 PP",
    "P2             PPPPP",
    "P11111111111PPPPPPPP",
    "P              PPPPP",
    "P                 PP",
    "PP2                P",
    "PPPPP              P",
    "PPPPPPPP11111111111P",
    "PPPPP              P",
    "PP                 P",
    "P                 PP",
    "P              PPPPP",
    "PS          PPPPPPPP",
    "PPPPPPPPPPPPPPPPPPPP",
    ),
            (
    "PPPPPPPPPPPPPPPPPPPP",
    "P                  P",
    "P                 EP",
    "P                3PP",
    "P                PPP",
    "P               PP P",
    "P              PP  P",
    "P             PP   P",
    "P            PP    P",
    "P           PP     P",
    "P          PP      P",
    "P         PP       P",
    "P        PP        P",
    "P       PP         P",
    "P      PP          P",
    "P     PP           P",
    "P    PP            P",
    "P   PP             P",
    "PS PP              P",
    "PPPPPPPPPPPPPPPPPPPP",
    ),
            (
    "PPPPPPPPPPPPPPPPPPPP",
    "P                  P",
    "P                  P",
    "P                  P",
    "P                  P",
    "P                  P",
    "P                  P",
    "P                  P",
    "P                  P",
    "P                  P",
    "P                  P",
    "P                  P",
    "P                  P",
    "P                  P",
    "P                  P",
    "P                  P",
    "P            P1P   P",
    "P           PP4PP  P",
    "PS             EP  P",
    "PPPPPPPPPPPPPPPPPPPP",
    ),
            (
    "PPPPPPPPPPPPPPPPPPPP",
    "PC                3P",
    "PPPPPPPPPP PPPPPPPPP",
    "P     P            P",
    "P     b  2PPPPPP   P",
    "P     PPPPP    P E P",
    "P    1P        PPP P",
    "P    1P   PP     P P",
    "P     P   PP P   P P",
    "P  11 P      P   P P",
    "P  11 P      P   P P",
    "P     P PP   P   P P",
    "P     P PP   P   P P",
    "P11   P      P   P P",
    "P11   P      P   P P",
    "P     P  PP  P   P P",
    "P     P  PP  P   P P",
    "P     P      P   P P",
    "P  11   PP   P  SPBP",
    "PPPPPPPPPPPPPPPPPPPP",
    ),
    (
    
    "PPPPPPPPPPPPPPPPPPPP",
    "P      b 31 EP P  CP",
    "P      PPPPPPP PPP1P",
    "PPP  PPPPPPPPP  4  P",
    "P    P  3          P",
    "P    P PP          P",
    "P      P      4    P",
    "P     1P1          P",
    "PPP  P3 1PPPPPPPPPPP",
    "P     P1P          P",
    "P   PPP   2        P",
    "PS    P P  P PPPP  P",
    "PPPP  P P      P   P",
    "P B   P P      P   P",
    "PPP   P P2 4  PP   P",
    "P   PPP P      P   P",
    "P     P P     PP   P",
    "P     P PPPPPPP    P",
    "P                  P",
    "PPPPPPPPPPPPPPPPPPPP",
    ),
        (
    "PPPPPPPPPPPPPPPPPPPP",
    "P C              PPP",
    "PPPPPPPPPPPPPPPP1 PP",
    "P P       PPPPP P PP",
    "P P     P  2    P PP",
    "P P     P  2    P PP",
    "P P     P  2    P  P",
    "P P      PPPPPP bE P",
    "P P   P       2PPP P",
    "P PP P2       P    P",
    "P P   PPPPPP      PP",
    "P P               PP",
    "P P   B          P P",
    "P PP  PPPPPPPPPPPP P",
    "P P  211       P P P",
    "P P  PPPP P P  P P P",
    "PP           12 PP P",
    "P  PPPPPPPPPPPP  P P",
    "PS               P P",
    "PPPPPPPPPPPPPPPPPPPP",
    ),
        (
    "PPPPPPPPPPPPPPPPPPPP",
    "P      P    C      P",
    "P      P           P",
    "P      P           P",
    "P      P           P",
    "P      P    G      P",
    "P      P           P",
    "P      P      g    P",
    "P      P           P",
    "P  3   P           P",
    "P  P   P           P",
    "P  4   P         m P",
    "P      P           P",
    "P111 11P           P",
    "P 4  4 P           P",
    "P      P           P",
    "P111111P           P",
    "P      P           P",
    "P  S   PMbN       BP",
    "PPPPPPPPPPPPPPPPPPPP",
    ),
        (
    "PPPPPPPPPPPPPPPPPPPP",
    "PC       PP H14    P",
    "P11111111PPPP    4 P",
    "P11 11 11PPP  2  P P",
    "P11411411PP     P..P",
    "P11111111PP    P ..P",
    "P        b    P GP P",
    "P        PP     P..P",
    "P S    B PP      ..P",
    "PPPPPPPPPPPPPPPPPPgP",
    "PPPPPPPPPPPPPPPPPP P",
    "P 31 ....2m        P",
    "P1P  ....PP        P",
    "P P  ....PP  1N 1  P",
    "P PPPPPPPPP 2PPP   P",
    "P     3 1PP    MP  P",
    "PPPPP1111PP   PP   P",
    "PE     11PP        P",
    "PP     11PP       4P",
    "PPPPPPPPPPPPPPPPPPPP",),
        (
    "PPPPPPPPPPPPPPPPPPPP",
    "P        PP        P",
    "P        PP        P",
    "P        PP        P",
    "P    PPPPPPPPPP    P",
    "P    P2  E   2P    P",
    "P    P11PPPP11P    P",
    "P    P  4     P    P",
    "P    P2       P    P",
    "P    P       2P    P",
    "P    P2       P    P",
    "P    P       2P    P",
    "P    P2       P    P",
    "P    P       2P    P",
    "P    PS    4  P    P",
    "P    PPPPPPPPPP    P",
    "P                  P",
    "P                  P",
    "P                  P",
    "PPPPPPPPPPPPPPPPPPPP",),
        (
    "PPPPPPPPPPPPPPPPPPPP",
    "P                  P",
    "P                  P",
    "P                  P",
    "P                  P",
    "PPPPPPPPPPPPPPPPPPPP",
    "PS                2P",
    "PPPPPPPPPPPPPPPPPPPP",
    "P                  P",
    "P                  P",
    "P                  P",
    "P                  P",
    "P                  P",
    "P                  P",
    "P                  P",
    "P                  P",
    "P                  P",
    "P                  P",
    "P                  P",
    "PPPPPPPPPPPPPPPPPPPP",
    ),
    (
    "PPPPPPPPPPPPPPPPPPPP",
    "P                  P",
    "P                  P",
    "P                  P",
    "P                  P",
    "P                  P",
    "P                  P",
    "P                  P",
    "P                  P",
    "P                  P",
    "P                  P",
    "P                  P",
    "P                  P",
    "P                  P",
    "P                  P",
    "P                  P",
    "P                  P",
    "P                  P",
    "P                  P",
    "PPPPPPPPPPPPPPPPPPPP",
    ))
            

def string_to_matrix(string):
    matrix = []
    for i in string:
        matrix.append(i)
    return matrix

def map_to_level(map):
    level = []
    for string in map:
        level.append(string_to_matrix(string))
    return level

def make_level(mapp):
    level = map_to_level(mapp)
    x = y = 0
    entities = pygame.sprite.Group()
    enemies = []
    buttons = [0,0,0]
    gates = [0,0,0]
    shadows = [0,0,0]
    pushed = [1,1,1]
    anvil = copy(level)
    for row in anvil:
        for col in row:
            if col == 'S':
                player = Player(x,y,False)
                entities.add(player)
            elif col == '2':
                e = Enemy(x,y, 'left')
                entities.add(e)
                enemies.append(e)
            elif col == '3':
                w = Walker(x,y,'left')
                entities.add(w)
                enemies.append(w)
            elif col =='4':
                f = Flyer(x,y,'down')
                entities.add(f)
                enemies.append(f)
            elif col in ['B','G','M']:
                button = Button(x,y,col)
                button.image = button_images[col]
                entities.add(button)
                buttons[letter_to_number(col)] = button
            elif col in ['b','g','m']:
                gate = (y//SQUAREWIDTH,x//SQUAREWIDTH)
                gates[letter_to_number(col)] = gate
            elif col in ['C','H','N']:
                shadow = Shadow(x,y,col)
                entities.add(shadow)
                shadows[letter_to_number(col)] = shadow
                pushed[letter_to_number(col)] = False
            elif col == 'C':
                gate = (y//SQUAREWIDTH,x//SQUAREWIDTH)
                gates[letter_to_number(col)] = gate
            x += SQUAREWIDTH
        y += SQUAREHEIGHT
        x = 0
    return [anvil, entities, enemies, buttons, gates, shadows, pushed, player]
        

def main():
    #pygame.mixer.music.play(-1)
    level_number = 0
    while True:
        # set up game
        left = right = up = False
        prelevel, entities, enemies, buttons, gates, shadows, pushed, player = make_level(maps[level_number])
        level = copy(prelevel)
        cloud_mode = stilled = False
        count = -0
        
        while True:
            main_clock.tick(FPS)
            count+=1
            #play game
            for e in pygame.event.get():

                if e.type == KEYDOWN:
                    if e.key == ord('k'):
                        player.dead = True
                    if e.key == ord('p'):
                        waitForPlayerToPressKey()
                    if e.key == K_RIGHT:
                        player.facing = 'right'
                    elif e.key == K_LEFT:
                        player.facing = 'left'
                    elif e.key == K_DOWN:
                        stilled = True
                        left = right = False

                if e.type == KEYUP and e.key == K_DOWN:
                    stilled = False
                
                if e.type == QUIT:
                    terminate()
                if not cloud_mode and not stilled:
                    if e.type == KEYDOWN:
                        if e.key == K_RIGHT:
                            right = True
                            left = False
                        elif e.key == K_LEFT:
                            right = False
                            left = True
                        elif e.key == K_UP:
                            up = True
                        elif e.key == K_SPACE:
                            cloud_mode = True
                            up = left = right = False

                if cloud_mode:
                    left = right = False
                    if e.type == KEYDOWN:
                        if player.facing == 'left':
                            xpos, ypos = player.board_location_left()
                        elif player.facing == 'right':
                            xpos, ypos = player.board_location_right()
                            
                        if e.key == K_UP:
                            if player.facing == 'right':
                                level = toggle(xpos + 1, ypos-1, level, entities)
                            elif player.facing == 'left':
                                level = toggle(xpos - 1, ypos-1, level, entities)
                            #level[ypos-1][xpos] = '1'
                        elif e.key == K_DOWN:
                            if player.facing == 'right':
                                level = toggle(xpos + 1, ypos+1, level, entities)
                            elif player.facing == 'left':
                                level = toggle(xpos - 1, ypos+1, level, entities)
                                
                        elif e.key == K_LEFT:
                            #cloud = Cloud((xpos-1)*SQUAREWIDTH , ypos*SQUAREHEIGHT, WHITE)
                            level = toggle(xpos-1, ypos, level, entities)
                            
                            #p = Cloud((xpos-1)*SQUAREWIDTH , ypos*SQUAREHEIGHT, WHITE)
                            #platforms.append(p)
                            #entities.add(p)
                        elif e.key == K_RIGHT:
                            xpos, ypos = player.board_location_right()
                            level = toggle(xpos+1, ypos, level, entities)

                    elif e.type == KEYUP:
                        if e.key == K_SPACE:
                            cloud_mode = False

                if e.type == KEYUP:
                    if e.key == K_RIGHT:
                        right = False
                    elif e.key == K_LEFT:
                        left = False
                    elif e.key == K_UP:
                        up = False
                    elif e.key == K_ESCAPE:
                        terminate()


                        
            screen.fill((10,10,10))
            


            
            x = y = 0
            for row in level:
                for col in row:
                    if col == '1':
                        screen.blit(cloud_image, pygame.Rect(x,y,SQUAREWIDTH, SQUAREHEIGHT))
                    elif col == 'P':
                        screen.blit(wood_image, pygame.Rect(x,y,SQUAREWIDTH,SQUAREHEIGHT))
                    elif col == '.':
                        #if (x + y) % (2*SQUAREWIDTH)== 0:
                            #screen.blit(static_images[count%SQUAREWIDTH], pygame.Rect(x,y,SQUAREWIDTH, SQUAREHEIGHT))
                        #else: screen.blit(static_images[(-count)%SQUAREWIDTH], pygame.Rect(x,y,SQUAREWIDTH, SQUAREHEIGHT))
                        if count%10 < 5: screen.blit(static_image, pygame.Rect(x,y,SQUAREWIDTH, SQUAREHEIGHT))
                        else: screen.blit(static_image_2, pygame.Rect(x,y,SQUAREWIDTH, SQUAREHEIGHT))
                    elif col == 'E':
                        door_rect = pygame.Rect(x,y,SQUAREWIDTH,SQUAREHEIGHT)
                        screen.blit(exit_image, door_rect)
                    elif col in ['B','M','G']:
                        screen.blit(button_images[col], pygame.Rect(x,y,SQUAREWIDTH,SQUAREHEIGHT))
                    elif col in ['b','g','m']:
                        screen.blit(closed_images[col], pygame.Rect(x,y,SQUAREWIDTH,SQUAREHEIGHT))
                    elif col == 'D':
                        screen.blit(open_image, pygame.Rect(x,y,SQUAREWIDTH,SQUAREHEIGHT))
                    x += SQUAREHEIGHT
                y+= SQUAREWIDTH
                x = 0

            player.update(up, left, right, level, enemies)

            if True:
                for e in enemies:
                    e.update(level)
            
            for i in range(len(shadows)):
                if pushed[i] == False and count%2==1:
                    shadow = shadows[i]
                    shadow.update(level)
                    if shadow.rect.colliderect(buttons[i].rect):
                        shadow.remove(entities)
                        pushed[i] = True
                        level[gates[i][0]][gates[i][1]] = 'D'
                        buttons[i].image = pushed_button_image
                    
            for entity in entities:
                screen.blit(entity.image, entity.rect)

            pygame.transform.scale(screen, (DISPLAYWIDTH, DISPLAYHEIGHT), window_surface)
            pygame.display.update()
            if player.dead:
                waitForPlayerToPressKey()
                break
            elif player.rect.colliderect(door_rect):
                level_number += 1
                waitForPlayerToPressKey()
                break

                        
main()            
