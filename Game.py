import pygame
import sys

pygame.init()

CLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode((800, 500))
pygame.display.set_caption("Quit the School_BETA.exe")

X_POSITION, Y_POSITION, Y_START, Y_START_P = 400, 400, 400, 400

sprung = False
run = False
runl = False
i1 = True
COLLIDE = False
di_npc = False
col_npc = False
TIMER_C = 0.1
TIMER_A = 400
TIMER_B = 10
on= False
exit0 = True
col = False

Y_GRAVITY = 0.6
JUMP_HEIGHT = 10
Y_VELOCITY = JUMP_HEIGHT
NPC1 = pygame.transform.scale(pygame.image.load("images/NPC1.png"), (142, 206))

STANDING_CHARACTER = pygame.transform.scale(pygame.image.load("images/c1.png"), (70, 128))
JUMPING_CHARACTER = pygame.transform.scale(pygame.image.load("images/c1_jump.png"), (96, 128))
RUNNING_CHARACTER = pygame.transform.scale(pygame.image.load("images/c1_run.png"), (96, 128))
RUNNINGL_CHARACTER = pygame.transform.scale(pygame.image.load("images/c1_runl.png"), (96, 128))
TEXT = pygame.transform.scale(pygame.image.load("images/Text1.png"), (300, 128))
TABLE = pygame.transform.scale(pygame.image.load("images/tisch.png"), (66, 64))
REGAL = pygame.transform.scale(pygame.image.load("images/regal.png"), (256,256))
collect = pygame.mixer.Sound("sounds/collect.mp3")
#SLIDING_CHARACTER = pygame.transform.scale(pygame.image.load("images/c1_run.png"), (96, 128))
KEY = pygame.transform.scale(pygame.image.load("images/key.png"), (48, 64))
BG = pygame.transform.scale(pygame.image.load("images/boden.png"), (4000, 100))
#BACKGROUND = pygame.transform.scale(pygame.image.load("images/hintergrund.jpg"), (1000,571.5)) -> Hat Johann nicht mehr eingereicht

character_rect = STANDING_CHARACTER.get_rect(center=(X_POSITION, Y_POSITION))
npc_rect = NPC1.get_rect(center=(X_POSITION-150, Y_POSITION))


class Table(object):
    def __init__(self, pos_x, pos_y):
        print("Tisch wird an")
        print(pos_x , pos_y)
        print("erzeugt")
        self.COLLIDE = False
    def update(self, pos_x, pos_y, character_rect):
        self.table_rect = TABLE.get_rect(center=(pos_x, pos_y))
        SCREEN.blit(TABLE, self.table_rect)
        if self.table_rect.colliderect(character_rect):
            self.COLLIDE = True
            #print("Nein")
        else:
            self.COLLIDE = False
class Regal_Hintergrund(object):
    def __init__(self):
        pass
    def update(self, x_pos, y_pos):
        self.bg = REGAL.get_rect(center=(x_pos, y_pos))
        SCREEN.blit(REGAL, self.bg)


t1 = Table(300, Y_START-50)
t0 = Table(300, Y_START-50)
t2 = Table(300, Y_START-50)

r1 = Regal_Hintergrund()
r2 = Regal_Hintergrund()

print(t0)
print(type(t0))

def Collide_Objects(X_POSITION, Y_POSITION, sprung, on, Y_START_P, COLLIDE):
    character_rect = STANDING_CHARACTER.get_rect(center=(X_POSITION, Y_POSITION))
    if col and keys_pressed[pygame.K_d] and on==False:
        COLLIDE = True
        X_POSITION -=1
        #print("Nein")
    elif col and keys_pressed[pygame.K_a] and on==False:
        COLLIDE = True
        X_POSITION +=1
    elif col and sprung==True:
        sprung=False
        on=True
        Y_START_P = Y_POSITION
        #print(Y_POSITION)
    elif sprung==False and on==True and not col:
        sprung=True
        Y_POSITION = Y_START_P
        on=False
        Y_START_P = Y_START
    elif sprung==True and on==True and not col:
        Y_POSITION = Y_START
        on=False
        Y_START_P = Y_START
    elif col and keys_pressed[pygame.K_d] and on==False:
        COLLIDE = True
        X_POSITION -=1
        #print("Nein")
    elif col and keys_pressed[pygame.K_a] and on==False:
        COLLIDE = True
        X_POSITION +=1
       #print("Nein")
    else:
        COLLIDE = False
        #Y_POSITION = Y_START
    
    return COLLIDE, on, sprung, Y_START_P, character_rect, X_POSITION

while exit0:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys_pressed = pygame.key.get_pressed()

    #Person geht
    SCREEN.fill("white")
    
    r1.update(200, Y_START-120)
    r2.update(600, Y_START-120)

    bg_rect = BG.get_rect(center=(400, Y_START+50))
    SCREEN.blit(BG, bg_rect)
    npc_rect = NPC1.get_rect(center=(150, Y_START-50))
    SCREEN.blit(NPC1, npc_rect)

    if keys_pressed[pygame.K_SPACE]: # Springen
        sprung = True
    if keys_pressed[pygame.K_LCTRL]: # Sliden
        slide = True
    elif keys_pressed[pygame.K_LSHIFT]: # Sprinten
        if keys_pressed[pygame.K_d] and not COLLIDE:
            X_POSITION += 5
            run = True
        elif keys_pressed[pygame.K_a] and not COLLIDE:
            X_POSITION -= 5
            runl = True
    elif not keys_pressed[pygame.K_LSHIFT]: # Normales gehen
        if keys_pressed[pygame.K_d] and not COLLIDE:
            X_POSITION += 3
            run = True
        elif keys_pressed[pygame.K_a] and not COLLIDE:
            X_POSITION -= 3
            runl = True
        elif keys_pressed[pygame.K_e] and col_npc:
            di_npc = True
            print("Dialog...")
    if keys_pressed[pygame.K_ESCAPE]:
        print("Beende...")
        exit0 = False
        
    t0.update(540, Y_START+50, character_rect)
    t1.update(600, Y_START, character_rect)
    t2.update(600, Y_START+50, character_rect)
        
    if t0.table_rect.colliderect(character_rect) or t1.table_rect.colliderect(character_rect) or t2.table_rect.colliderect(character_rect):
        col = True
    else:
        col = False


    if sprung:
        Y_POSITION -= Y_VELOCITY
        Y_VELOCITY -= Y_GRAVITY
        if keys_pressed[pygame.K_d]:
            X_POSITION += 3
        elif keys_pressed[pygame.K_a]:
            X_POSITION -= 3
        if Y_VELOCITY < -JUMP_HEIGHT:
            sprung = False
            Y_VELOCITY = JUMP_HEIGHT
            Y_POSITION = Y_START_P
        character_rect = JUMPING_CHARACTER.get_rect(center=(X_POSITION, Y_POSITION))
        SCREEN.blit(JUMPING_CHARACTER, character_rect)
    elif run:
        character_rect = RUNNING_CHARACTER.get_rect(center=(X_POSITION, Y_POSITION))
        SCREEN.blit(RUNNING_CHARACTER, character_rect)
        run = False
    elif runl:
        character_rect = RUNNING_CHARACTER.get_rect(center=(X_POSITION, Y_POSITION))
        SCREEN.blit(RUNNINGL_CHARACTER, character_rect)
        runl = False
    else:
        character_rect = STANDING_CHARACTER.get_rect(center=(X_POSITION, Y_POSITION))
        SCREEN.blit(STANDING_CHARACTER, character_rect)

    if i1:
        item_rect = KEY.get_rect(center=(700, Y_START))
        character_rect = STANDING_CHARACTER.get_rect(center=(X_POSITION, Y_POSITION))
        SCREEN.blit(KEY, item_rect)
        if item_rect.colliderect(character_rect):
            i1 = False
            print("JA")
            collect.play() 
 
    if npc_rect.colliderect(character_rect):
        col_npc = True
    else:
        col_npc = False
        
    if di_npc:
        TIMER_A -= TIMER_B
        TIMER_B -= TIMER_C
        if TIMER_B < -10:
            di_npc = False
            TIMER_B = 10
            TIMER_A = 400
        text_rect = TEXT.get_rect(center=(150, Y_START-150))
        SCREEN.blit(TEXT, text_rect)

    character_rect = STANDING_CHARACTER.get_rect(center=(X_POSITION, Y_POSITION))
    COLLIDE, on, sprung, Y_START_P, character_rect, X_POSITION = Collide_Objects(X_POSITION, Y_POSITION, sprung, on, Y_START_P, COLLIDE)

    pygame.display.update()
    CLOCK.tick(60)
