import os
import pygame
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

import random
#import time

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

###################################################################################################

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("images/jet.png").convert()
        self.surf.set_colorkey((0,0,0), RLEACCEL)
        self.rect = self.surf.get_rect()
        #self.surf = pygame.Surface((75, 25))
        #self.surf.fill((255, 255, 255))

        #self.rect.x = SCREEN_WIDTH/2 - self.rect.width/2
        #self.rect.y = SCREEN_HEIGHT/2 - self.rect.height/2
        self.movement_speed = 1
        self.move_up_sound = pygame.mixer.Sound("sounds/Rising_putter.ogg")
        self.move_down_sound = pygame.mixer.Sound("sounds/Falling_putter.ogg")
        self.collision_sound = pygame.mixer.Sound("sounds/Collision.ogg")

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
           self.rect.move_ip(0, -self.movement_speed)
           self.move_up_sound.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, self.movement_speed)
            self.move_down_sound.play()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-self.movement_speed, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(self.movement_speed, 0)

        #Give some inbounds to the screen so the player cannot go off the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def play_collision_sound(self):
        self.collision_sound.play()
    
    def stop_navigation_sounds(self):
        self.move_up_sound.stop()
        self.move_down_sound.stop()

    #def __del__(self):
    #    self.move_up_sound.stop()
    #    self.move_down_sound.stop()

###################################################################################################

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("images/missile.png").convert()
        self.surf.set_colorkey((0,0,0), RLEACCEL)
        #self.surf = pygame.Surface((20, 10))
        #self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=( 
                    random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                    random.randint(0, SCREEN_HEIGHT)
                    )
        )

        self.speed = random.randint(5, 20)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

###################################################################################################

class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("images/cloud.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()
###################################################################################################

#set working directory 
os.chdir(os.path.dirname(os.path.realpath(__file__)))

pygame.init()

pygame.mixer.init()

# Load and play background music
# Sound source: http://ccmixter.org/files/Apoxode/59262
# License: https://creativecommons.org/licenses/by/3.0/

pygame.mixer.music.load("sounds/Apoxode_-_Electric_1.mp3")
pygame.mixer.music.play(loops=-1)

clock = pygame.time.Clock()

screen_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Create a custom event for adding a new enemy
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 1000)

ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)


player = Player()


# Create groups to hold enemy sprites and all sprites
# - enemies is used for collision detection and position updates
# - all_sprites is used for rendering
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)


running = True

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False

        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        elif event.type == ADDCLOUD:
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)

    
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    
    # Update enemy position
    #for enemy in enemies:
    #    enemy.update()
    enemies.update()
    clouds.update()

    screen_surface.fill((135,206,250))

    
    for entity in all_sprites:
        screen_surface.blit(entity.surf, entity.rect)

    # Check if any enemies have collided with the player
    if pygame.sprite.spritecollideany(player,enemies):
        player.play_collision_sound()
        player.stop_navigation_sounds()
        
        player.kill()

        running = False

    #screen_surface.blit(player.surf, player.rect)
    #screen_surface.blit(player.surf, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
    
    pygame.display.flip()

    clock.tick(30)

pygame.mixer.music.stop()
pygame.mixer.quit()
