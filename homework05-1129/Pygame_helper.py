# import the pygame module
import pygame

# import random for random numbers!
import random

# import pygame.locals for easier access to key coordinates
from pygame.locals import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.image = pygame.image.load('jet.png').convert()
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.image.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[0]:  # Up
            self.rect.move_ip(0, -5)
        if pressed_keys[1]:  # Down
            self.rect.move_ip(0, 5)
        if pressed_keys[2]:  # Left
            self.rect.move_ip(-5, 0)
        if pressed_keys[3]:  # Right
            self.rect.move_ip(5, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > 800:
            self.rect.right = 800
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= 600:
            self.rect.bottom = 600

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.image = pygame.image.load('missile.png').convert()
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.image.get_rect(
            center=(random.randint(820, 900), random.randint(0, 600)))
        self.speed = random.randint(5, 20)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.image = pygame.image.load('cloud.png').convert()
        self.image.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.image.get_rect(center=(
            random.randint(820, 900), random.randint(0, 600))
        )

    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()

class Game(object):
    def __init__(self, width = 800, height = 600):
        # initialize pygame
        pygame.init()

        # create the screen object
        # here we pass it a size of 800x600
        self.screen = pygame.display.set_mode((width, height))

        # Create a custom event for adding a new enemy.
        self.ADDENEMY = pygame.USEREVENT + 1
        pygame.time.set_timer(self.ADDENEMY, 250)
        self.ADDCLOUD = pygame.USEREVENT + 2
        pygame.time.set_timer(self.ADDCLOUD, 1000)

        # create our 'player', right now he's just a rectangle
        self.player = Player()

        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill((135, 206, 250))

        self.enemies = pygame.sprite.Group()
        self.clouds = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        self.running = True
        self.framecount = 0

    def get_frame(self, Key_press, QuitFlag = False):
        if self.running:
            self.framecount += 1
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                elif event.type == self.ADDENEMY:
                    new_enemy = Enemy()
                    self.enemies.add(new_enemy)
                    self.all_sprites.add(new_enemy)
                elif event.type == self.ADDCLOUD:
                    new_cloud = Cloud()
                    self.all_sprites.add(new_cloud)
                    self.clouds.add(new_cloud)
            self.screen.blit(self.background, (0, 0))
            if QuitFlag == True:
                self.running = False
            self.player.update(Key_press)
            self.enemies.update()
            self.clouds.update()
            for entity in self.all_sprites:
                self.screen.blit(entity.image, entity.rect)

            if pygame.sprite.spritecollideany(self.player, self.enemies):
                self.player.kill()
            image_name = '{}.jpg'.format(self.framecount)
            pygame.image.save(self.screen, image_name)

            return image_name
