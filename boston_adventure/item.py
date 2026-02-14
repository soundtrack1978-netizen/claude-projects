import math
import pygame
from settings import (
    ITEM_SIZE, ITEM_GRAVITY, HEART_COLOR,
    SCREEN_HEIGHT, GROUND_HEIGHT,
    ITEM_FADE_DURATION, ITEM_BLINK_INTERVAL, ITEM_PICKUP_DELAY,
)


class HeartItem(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((ITEM_SIZE, ITEM_SIZE), pygame.SRCALPHA)
        self._draw_heart()
        self.rect = self.image.get_rect(centerx=x, top=y)
        self.ground_y = SCREEN_HEIGHT - GROUND_HEIGHT - ITEM_SIZE
        self.vel_y = -4  # small pop upward
        self.landed = False
        self.collected = False
        self.collected_time = 0
        self.visible = True
        self.spawn_time = pygame.time.get_ticks()
        self.pickable = False

    def _draw_heart(self):
        cx, cy = ITEM_SIZE // 2, ITEM_SIZE // 2
        points = []
        for deg in range(360):
            t = math.radians(deg)
            hx = 16 * math.sin(t) ** 3
            hy = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
            px = cx + hx * ITEM_SIZE / 36
            py = cy + hy * ITEM_SIZE / 36
            points.append((px, py))
        if len(points) > 2:
            pygame.draw.polygon(self.image, HEART_COLOR, points)

    def collect(self):
        self.collected = True
        self.collected_time = pygame.time.get_ticks()

    def update(self):
        if self.collected:
            elapsed = pygame.time.get_ticks() - self.collected_time
            if elapsed >= ITEM_FADE_DURATION:
                self.kill()
            else:
                self.visible = (elapsed // ITEM_BLINK_INTERVAL) % 2 == 0
            return
        if not self.pickable and pygame.time.get_ticks() - self.spawn_time >= ITEM_PICKUP_DELAY:
            self.pickable = True
        if self.landed:
            return
        self.vel_y += ITEM_GRAVITY
        self.rect.y += self.vel_y
        if self.rect.y >= self.ground_y:
            self.rect.y = self.ground_y
            self.vel_y = 0
            self.landed = True
