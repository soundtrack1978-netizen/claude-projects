import pygame
from settings import (
    PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_SPEED, PLAYER_COLOR,
    PLAYER_Y, SCREEN_WIDTH, PLAYER_BULLET_SPEED,
    PLAYER_BULLET_COLOR, SHOOT_COOLDOWN,
)
from bullet import Bullet


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT), pygame.SRCALPHA)
        # Draw a Boston Terrier face
        cx, cy = PLAYER_WIDTH // 2, PLAYER_HEIGHT // 2 + 2
        BLK = (20, 20, 20)
        WHT = (255, 255, 255)
        # Face (black oval)
        pygame.draw.ellipse(self.image, BLK, (cx - 16, cy - 10, 32, 24))
        # White muzzle stripe
        pygame.draw.ellipse(self.image, WHT, (cx - 6, cy - 10, 12, 22))
        # Ears (black triangles)
        pygame.draw.polygon(self.image, BLK, [(cx - 14, cy - 8), (cx - 20, cy - 18), (cx - 6, cy - 10)])
        pygame.draw.polygon(self.image, BLK, [(cx + 14, cy - 8), (cx + 20, cy - 18), (cx + 6, cy - 10)])
        # Eyes (white with black pupils)
        pygame.draw.circle(self.image, WHT, (cx - 8, cy - 2), 4)
        pygame.draw.circle(self.image, WHT, (cx + 8, cy - 2), 4)
        pygame.draw.circle(self.image, BLK, (cx - 8, cy - 2), 2)
        pygame.draw.circle(self.image, BLK, (cx + 8, cy - 2), 2)
        # Nose (black)
        pygame.draw.circle(self.image, BLK, (cx, cy + 5), 3)
        self.rect = self.image.get_rect(centerx=SCREEN_WIDTH // 2, top=PLAYER_Y)
        self.last_shot = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += PLAYER_SPEED

    def shoot(self, bullet_group):
        now = pygame.time.get_ticks()
        if now - self.last_shot >= SHOOT_COOLDOWN:
            self.last_shot = now
            bullet = Bullet(
                self.rect.centerx, self.rect.top,
                PLAYER_BULLET_SPEED, PLAYER_BULLET_COLOR,
            )
            bullet_group.add(bullet)

    def reset_position(self):
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.top = PLAYER_Y
