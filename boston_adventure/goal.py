import pygame
from settings import (
    GOAL_X, GOAL_FLAG_COLOR, GOAL_POLE_COLOR,
    SCREEN_HEIGHT, GROUND_HEIGHT,
)


class Goal(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        width = 40
        height = 80
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        # Pole
        pole_x = width // 2 - 2
        pygame.draw.rect(self.image, GOAL_POLE_COLOR, (pole_x, 0, 4, height))
        # Flag (triangle)
        pygame.draw.polygon(self.image, GOAL_FLAG_COLOR, [
            (pole_x + 4, 4),
            (pole_x + 30, 16),
            (pole_x + 4, 28),
        ])
        self.rect = self.image.get_rect()
        self.rect.x = GOAL_X
        self.rect.y = SCREEN_HEIGHT - GROUND_HEIGHT - height
