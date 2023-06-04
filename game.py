import pygame
import random
import time

# Fenstergröße
WIDTH = 800
HEIGHT = 600

# Farben
BLUE = (0, 0, 255)

# Spieler Eigenschaften
PLAYER_WIDTH = 128
PLAYER_HEIGHT = 128
PLAYER_VELOCITY = 8
JUMP_VELOCITY = 10
GRAVITY = 0.5

# Plattform Eigenschaften
PLATFORM_WIDTH = 150
PLATFORM_HEIGHT = 120
PLATFORM_VELOCITY = 5
PLATFORM_GAP = 300  # Horizontaler Abstand zwischen den Plattformen
BACKGROUND = pygame.transform.scale(pygame.image.load("images/bg_2.png"), (1400, 1000))
BACKGROUNDLAVA = pygame.transform.scale(pygame.image.load("images/lava.jpg"), (1800, 50))
BACKGROUNDLAVA_END = pygame.transform.scale(pygame.image.load("images/lava.jpg"), (1600, 1200))
TUTORIAL_IMAGE = pygame.transform.scale(pygame.image.load("images/start.png"), (830, 475))


highscorer = open('./Highscore.txt')
Highscore_save = highscorer.read()
highscorer.close()

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jump and Run Spiel")

clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/c1_run.png")
        self.image = pygame.transform.scale(self.image, (PLAYER_WIDTH, PLAYER_WIDTH))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 2
        self.rect.y = HEIGHT - PLAYER_HEIGHT
        self.velocity_y = 0
        self.on_ground = False

    def update(self):
        self.velocity_y += GRAVITY

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x -= PLAYER_VELOCITY
        if keys[pygame.K_d]:
            self.rect.x += PLAYER_VELOCITY - 5

        self.rect.y += self.velocity_y

        if self.rect.y >= HEIGHT - PLAYER_HEIGHT:
            self.rect.y = HEIGHT - PLAYER_HEIGHT
            self.velocity_y = 0
            self.on_ground = True

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.x -= PLATFORM_VELOCITY
        if self.rect.right < 0:
            self.rect.x = WIDTH + 252 + random.randint(50, 250)
            self.rect.y = random.randint(490, 510)

platforms = pygame.sprite.Group()

font = pygame.font.Font(None, 36)

def draw_score(score):
    text = font.render("Score: " + str(score), True, (1,1,1))
    screen.blit(text, (500, 10))

def draw_HI_score(score):
    text = font.render("Highscore: " + str(score), True, (1,1,1))
    screen.blit(text, (10, 10))
def draw(text, w):
    text = font.render(text, True, (1,1,1))
    screen.blit(text, (300, 250+w))

all_sprites = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

# Plattformen erstellen
platform_images = ["images/table.png"]  # Liste der Plattform-Bilder

for i in range(5):
    platform_image = random.choice(platform_images)
    platform = Platform(WIDTH + i * random.randint(PLATFORM_GAP, PLATFORM_GAP + 100),
                        random.randint(550, 600), platform_image)
    platforms.add(platform)
    all_sprites.add(platform)

score = 0
running = False
startscreen = True
end = False

while startscreen:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            startscreen = False
    keys_pressed = pygame.key.get_pressed()
    
    if keys_pressed[pygame.K_SPACE]:
        startscreen = False
        running = True
    screen.fill((255, 255, 255))
    start_rect = TUTORIAL_IMAGE.get_rect(center=(400, 250))
    screen.blit(TUTORIAL_IMAGE, start_rect)
    
    clock.tick(60)
    pygame.display.flip()

S_TIME = time.time()  # Startzeit des Spiels
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and player.on_ground:
            player.image = pygame.image.load("images/c1_jump.png")
            player.image = pygame.transform.scale(player.image, (PLAYER_WIDTH-30, PLAYER_WIDTH))
            player.velocity_y -= JUMP_VELOCITY
            player.on_ground = False

    all_sprites.update()

    collision = pygame.sprite.spritecollide(player, platforms, False)
    if collision:
        # Korrigiere die Position des Spielers auf der Plattform
        player.image = pygame.image.load("images/c1_run.png")
        player.image = pygame.transform.scale(player.image, (PLAYER_WIDTH, PLAYER_WIDTH))
        player.rect.y = collision[0].rect.y - PLAYER_HEIGHT
        player.velocity_y = 0
        player.on_ground = True
        score += 10

    screen.fill((255, 255, 255))
    bg0_rect = BACKGROUND.get_rect(center=(100, 250))
    screen.blit(BACKGROUND, bg0_rect)
    bg1_rect = BACKGROUNDLAVA.get_rect(center=(0, 600))
    screen.blit(BACKGROUNDLAVA, bg1_rect)
    all_sprites.draw(screen)
    draw_score(score)
    draw_HI_score(Highscore_save)
    pygame.display.flip()
    clock.tick(60)
    print(score)

    TIMER = time.time() - S_TIME  # Verstrichene Zeit seit Spielbeginn
    if TIMER >= 3 and player.rect.y >= HEIGHT - PLAYER_HEIGHT:
        with open('Highscore.txt' , 'w') as Highscore:
            hread = Highscore_save
            print(Highscore_save)
            if Highscore_save == "":
                Highscore_save = "0"
            #print (hread1)
            if score > int(Highscore_save):
                Highscore.write(str(score))
            else:
                Highscore.write(Highscore_save)            
        running = False
        end = True
while end:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and player.on_ground:
            end = False
    screen.fill((255, 255, 255))
    bg0_rect = BACKGROUNDLAVA_END.get_rect(center=(100, 250))
    screen.blit(BACKGROUNDLAVA_END, bg0_rect)
    draw("Du bist verbrannt...", 0)
    draw("Drücke Space zum Beenden", 20)
    draw_score(score)
    draw_HI_score(Highscore_save)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()