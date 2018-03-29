import pygame
import pygameutils
from pygame.locals import *
pygame.init()
import random

GAME_RES = WIDTH, HEIGHT = 1900, 720
FPS = 60
GAME_TITLE = 'Default Game Title'

window = pygame.display.set_mode(GAME_RES, HWACCEL | HWSURFACE | DOUBLEBUF)
pygame.display.set_caption(GAME_TITLE)
clock = pygame.time.Clock()
myfont = pygame.font.SysFont("monospace", 20)

images = dict(
    dino_1=pygame.image.load('./images/dino1.png'),
    cactus_1=pygame.image.load('./images/single_cactus.png'),
    bgd=pygame.image.load('./images/sandBG.png')
)
images['bgd'] = pygame.transform.scale(images['bgd'], (WIDTH, HEIGHT))
images['dino_1'] = pygame.transform.scale(images['dino_1'], (73, 80))
images['cactus_1'] = pygame.transform.scale(images['cactus_1'], (60, 60))


# Game Values
def spawn_catuses():
    # spawn randomically cactuses
    cactus_group.add(*[Cactus(images['cactus_1'], random.randint(300, 1300)) for _ in range(random.randint(1, 4))])


class Cactus(pygame.sprite.Sprite):
    def __init__(self, image, x=500, y=587):
        super().__init__()
        self.image = image
        self.rect = image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.rect.width
        self.height = self.rect.height


class Dino(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = image.get_rect()
        self.rect.x = 100
        self.rect.y = 567
        self.width = self.rect.width
        self.height = self.rect.height
        self.is_jumping = False
        self.prev_jump = False
        self.max_jump = 180
        self.curr_jump = 0
        self.curr_image = 1
        self.speed = 8
        self.jump_speed = 12

    def update(self):
        # movement
        self.rect.x += self.speed

        # jump
        if self.is_jumping:
            if self.curr_jump < self.max_jump:
                self.curr_jump += self.jump_speed
                self.rect.y -= self.jump_speed
            else:
                self.is_jumping = False
                self.prev_jump = True
                self.curr_jump = 0
        elif self.prev_jump:
            if self.curr_jump < self.max_jump:
                self.curr_jump += self.jump_speed
                self.rect.y += self.jump_speed
            else:
                self.is_jumping = False
                self.prev_jump = False
                self.curr_jump = 0

        # collision with border
        if self.rect.x > WIDTH:
            self.rect.x = 0 - self.width
            cactus_group.empty()
            spawn_catuses()


player = Dino(images['dino_1'])
dino_group = pygame.sprite.GroupSingle(player)
cactus_group = pygame.sprite.Group()

# generates randomically cactuses into the map
spawn_catuses()
points = 0

# End of Game Values

# Game loop
game_ended = False
while not game_ended:
    # Event handling
    for event in pygame.event.get():
        if event.type == QUIT:
            game_ended = True
            break
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                game_ended = True
                break
            if event.key == K_SPACE:
                if not player.is_jumping and not player.prev_jump:
                    player.is_jumping = True
                    player.prev_jump = False

    # Game logic
    player.update()
    points += player.speed
    if pygame.sprite.groupcollide(dino_group, cactus_group, False, False):
        print('collide')
    # Display update
    window.blit(images['bgd'], (0, 0))
    cactus_group.draw(window)
    dino_group.draw(window)

    text_points = myfont.render(str(points), 1, (0, 0, 0))
    window.blit(text_points, (WIDTH // 2 - 20, 20))
    # attached_camera.keep_attached()
    # camera.draw_onscreen(window)
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
exit(0)
