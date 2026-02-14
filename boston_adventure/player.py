import os
import pygame
from settings import (
    PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_SPEED,
    GRAVITY, JUMP_POWER, DOUBLE_JUMP_POWER, MAX_JUMPS,
    SCREEN_WIDTH, SCREEN_HEIGHT, GROUND_HEIGHT,
    INVINCIBLE_DURATION, BLINK_INTERVAL,
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
        self.jump_count = 0
        self.space_pressed_last = False
        self.start_x = 100
        self.invincible = False
        self.invincible_start = 0
        self.visible = True

    def update(self):
        keys = pygame.key.get_pressed()

        # Horizontal movement (world coordinates, no screen limit)
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED

        # Jump (trigger on new press only, not hold)
        # Support both Space and Up arrow to avoid IME conflict
        space_now = keys[pygame.K_SPACE] or keys[pygame.K_UP]
        if space_now and not self.space_pressed_last:
            if self.on_ground:
                self.vel_y = JUMP_POWER
                self.on_ground = False
                self.jump_count = 1
            elif self.jump_count < MAX_JUMPS:
                self.vel_y = DOUBLE_JUMP_POWER
                self.jump_count += 1
        self.space_pressed_last = space_now

        # Gravity
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        # Land on ground
        if self.rect.y >= self.ground_y:
            self.rect.y = self.ground_y
            self.vel_y = 0
            self.on_ground = True
            self.jump_count = 0

        # Invincibility timer and blink
        if self.invincible:
            elapsed = pygame.time.get_ticks() - self.invincible_start
            if elapsed >= INVINCIBLE_DURATION:
                self.invincible = False
                self.visible = True
            else:
                self.visible = (elapsed // BLINK_INTERVAL) % 2 == 0

    def start_invincible(self):
        self.invincible = True
        self.invincible_start = pygame.time.get_ticks()
