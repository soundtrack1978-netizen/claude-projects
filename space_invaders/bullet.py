import pygame
from settings import BULLET_WIDTH, BULLET_HEIGHT, SCREEN_HEIGHT


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, color):
        super().__init__()
        self.image = pygame.Surface((BULLET_WIDTH, BULLET_HEIGHT))
        self.image.fill(color)
        self.rect = self.image.get_rect(centerx=x, top=y)
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()
