import os
import pygame
from settings import (
    PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_SPEED,
    GRAVITY, JUMP_POWER, SCREEN_WIDTH, SCREEN_HEIGHT, GROUND_HEIGHT,
)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Load Boston Terrier image
        base_dir = os.path.dirname(__file__)
        img_path = os.path.join(base_dir, "assets", "lucas.png")
        raw = pygame.image.load(img_path).convert_alpha()
        scaled = pygame.transform.scale(raw, (PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image = pygame.transform.flip(scaled, True, False)
        self.rect = self.image.get_rect()
        self.ground_y = SCREEN_HEIGHT - GROUND_HEIGHT - PLAYER_HEIGHT
        self.rect.x = 100
        self.rect.y = self.ground_y
        self.vel_y = 0
        self.on_ground = True

    def update(self):
        keys = pygame.key.get_pressed()

        # Horizontal movement (world coordinates, no screen limit)
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED

        # Jump
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = JUMP_POWER
            self.on_ground = False

        # Gravity
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        # Land on ground
        if self.rect.y >= self.ground_y:
            self.rect.y = self.ground_y
            self.vel_y = 0
            self.on_ground = True
