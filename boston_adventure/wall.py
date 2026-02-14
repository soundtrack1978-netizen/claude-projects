import pygame
from settings import (
    WALL_WIDTH, WALL_HEIGHT, WALL_COLOR,
    SCREEN_HEIGHT, GROUND_HEIGHT,
)


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, height=WALL_HEIGHT):
        super().__init__()
        self.image = pygame.Surface((WALL_WIDTH, height))
        self.image.fill(WALL_COLOR)
        # Brick pattern
        brick_color = (100, 65, 40)
        for row in range(0, height, 12):
            offset = 0 if (row // 12) % 2 == 0 else WALL_WIDTH // 2
            for col in range(-offset, WALL_WIDTH, WALL_WIDTH // 2):
                pygame.draw.rect(self.image, brick_color, (col, row, WALL_WIDTH // 2 - 1, 11), 1)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = SCREEN_HEIGHT - GROUND_HEIGHT - height
