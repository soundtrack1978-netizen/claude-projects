import random
import pygame
from settings import (
    ENEMY_WIDTH, ENEMY_HEIGHT, ENEMY_SPEED, ENEMY_PATROL_RANGE,
    SCREEN_HEIGHT, GROUND_HEIGHT, WORLD_WIDTH, ENEMY_COUNT,
)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface((ENEMY_WIDTH, ENEMY_HEIGHT), pygame.SRCALPHA)
        self._draw_cat()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = SCREEN_HEIGHT - GROUND_HEIGHT - ENEMY_HEIGHT
        self.origin_x = x
        self.direction = 1

    def _draw_cat(self):
        w, h = ENEMY_WIDTH, ENEMY_HEIGHT
        color = (180, 120, 60)
        # Body
        pygame.draw.ellipse(self.image, color, (4, h // 3, w - 12, h * 2 // 3))
        # Head
        head_cx, head_cy = 8, h // 3
        pygame.draw.circle(self.image, color, (head_cx, head_cy), 7)
        # Ears
        pygame.draw.polygon(self.image, color, [(3, head_cy - 5), (1, head_cy - 13), (8, head_cy - 7)])
        pygame.draw.polygon(self.image, color, [(13, head_cy - 5), (15, head_cy - 13), (8, head_cy - 7)])
        # Tail
        pygame.draw.arc(self.image, color, (w - 16, 0, 14, h // 2), 0, 2.5, 2)
        # Legs
        pygame.draw.rect(self.image, color, (8, h - 5, 3, 5))
        pygame.draw.rect(self.image, color, (18, h - 5, 3, 5))
        # Eyes
        pygame.draw.circle(self.image, (0, 0, 0), (6, head_cy - 1), 1)
        pygame.draw.circle(self.image, (0, 0, 0), (10, head_cy - 1), 1)

    def update(self):
        self.rect.x += ENEMY_SPEED * self.direction
        if self.rect.x > self.origin_x + ENEMY_PATROL_RANGE:
            self.direction = -1
        elif self.rect.x < self.origin_x - ENEMY_PATROL_RANGE:
            self.direction = 1


def create_enemies():
    group = pygame.sprite.Group()
    spacing = WORLD_WIDTH // (ENEMY_COUNT + 1)
    for i in range(ENEMY_COUNT):
        x = spacing * (i + 1) + random.randint(-50, 50)
        group.add(Enemy(x))
    return group
