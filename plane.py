import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

###################################################################################################

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 25))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        #self.rect.x = SCREEN_WIDTH/2 - self.rect.width/2
        #self.rect.y = SCREEN_HEIGHT/2 - self.rect.height/2
        self.movement_speed = 1

    
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
           self.rect.move_ip(0, -self.movement_speed)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, self.movement_speed)
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

###################################################################################################

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((20, 10))
        self.surf.fill((255, 255, 255))
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

pygame.init()

screen_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Create a custom event for adding a new enemy
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 1000)


player = Player()


# Create groups to hold enemy sprites and all sprites
# - enemies is used for collision detection and position updates
# - all_sprites is used for rendering
enemies = pygame.sprite.Group()
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
            print("enemy added")
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

    
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    
    # Update enemy position
    #for enemy in enemies:
    #    enemy.update()
    enemies.update()


    screen_surface.fill((0, 0, 0))
    
    for entity in all_sprites:
        screen_surface.blit(entity.surf, entity.rect)

# Check if any enemies have collided with the player
    if pygame.sprite.spritecollideany(player,enemies):
        player.kill()
        running = False
    # If so, then remove the player and stop the loop

    #screen_surface.blit(player.surf, player.rect)
    #screen_surface.blit(player.surf, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
    
    pygame.display.flip()