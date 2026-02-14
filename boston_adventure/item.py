import math
import pygame
from settings import (
    ITEM_SIZE, ITEM_GRAVITY, HEART_COLOR,
    SCREEN_HEIGHT, GROUND_HEIGHT,
    ITEM_FADE_DURATION, ITEM_BLINK_INTERVAL, ITEM_PICKUP_DELAY,
    POOP_WIDTH, POOP_HEIGHT, POOP_COLOR,
    POOP_FLY_DISTANCE, POOP_FLY_SPEED,
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


class PoopItem(pygame.sprite.Sprite):
    """Cute poop obstacle that defeats enemies on contact."""

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((POOP_WIDTH, POOP_HEIGHT), pygame.SRCALPHA)
        self._draw_poop()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = y
        self.visible = True
        self.flying = False
        self.fly_remaining = 0

    def _draw_poop(self):
        w, h = POOP_WIDTH, POOP_HEIGHT
        c = POOP_COLOR
        light = (180, 130, 70)
        # Bottom layer (widest)
        pygame.draw.ellipse(self.image, c, (1, h - 8, w - 2, 8))
        # Middle layer
        pygame.draw.ellipse(self.image, c, (3, h - 14, w - 6, 8))
        # Top swirl
        pygame.draw.ellipse(self.image, c, (5, h - 18, w - 10, 7))
        # Tip
        pygame.draw.circle(self.image, c, (w // 2, 2), 3)
        # Cute highlight
        pygame.draw.circle(self.image, light, (w // 2 - 2, h - 12), 2)
        # Eyes
        pygame.draw.circle(self.image, (0, 0, 0), (w // 2 - 3, h - 9), 1)
        pygame.draw.circle(self.image, (0, 0, 0), (w // 2 + 3, h - 9), 1)
        # Smile
        pygame.draw.arc(self.image, (0, 0, 0), (w // 2 - 3, h - 8, 6, 4), 3.14, 6.28, 1)

    def launch(self):
        self.flying = True
        self.fly_remaining = POOP_FLY_DISTANCE

    def update(self):
        if self.flying and self.fly_remaining > 0:
            step = min(POOP_FLY_SPEED, self.fly_remaining)
            self.rect.x -= step
            self.fly_remaining -= step
            if self.fly_remaining <= 0:
                self.flying = False
