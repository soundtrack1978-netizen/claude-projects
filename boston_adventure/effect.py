import math
import random
import pygame
from settings import (
    SPARKLE_DURATION, SPARKLE_COUNT, SPARKLE_SPEED, SPARKLE_COLOR,
    ATTACK_RANGE, ATTACK_DURATION, GAS_COLOR, GAS_PARTICLE_COUNT,
)


class SparkleEffect:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.start_time = pygame.time.get_ticks()
        self.alive = True
        # Generate particles in radial directions
        self.particles = []
        for i in range(SPARKLE_COUNT):
            angle = (2 * math.pi / SPARKLE_COUNT) * i
            vx = math.cos(angle) * SPARKLE_SPEED
            vy = math.sin(angle) * SPARKLE_SPEED
            self.particles.append([float(x), float(y), vx, vy])

    def update(self):
        elapsed = pygame.time.get_ticks() - self.start_time
        if elapsed >= SPARKLE_DURATION:
            self.alive = False
            return
        for p in self.particles:
            p[0] += p[2]
            p[1] += p[3]

    def draw(self, surface, camera_x):
        elapsed = pygame.time.get_ticks() - self.start_time
        # Fade out: reduce size over time
        progress = elapsed / SPARKLE_DURATION
        size = max(1, int(4 * (1 - progress)))
        alpha = int(255 * (1 - progress))
        color = (SPARKLE_COLOR[0], SPARKLE_COLOR[1], SPARKLE_COLOR[2], alpha)
        for p in self.particles:
            sx = int(p[0] - camera_x)
            sy = int(p[1])
            spark = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(spark, color, (size, size), size)
            surface.blit(spark, (sx - size, sy - size))


class GasEffect:
    """Yellow fart gas cloud expanding to the left of the player."""

    def __init__(self, x, y):
        self.start_time = pygame.time.get_ticks()
        self.alive = True
        # Particles spread leftward with some vertical scatter
        self.particles = []
        for _ in range(GAS_PARTICLE_COUNT):
            vx = -random.uniform(2, 5)
            vy = random.uniform(-1.5, 1.5)
            size = random.randint(6, 12)
            self.particles.append([float(x), float(y), vx, vy, size])
        # Hit rect for enemy collision (left of player, ATTACK_RANGE wide)
        self.hit_rect = pygame.Rect(x - ATTACK_RANGE, y - 15, ATTACK_RANGE, 30)

    def update(self):
        elapsed = pygame.time.get_ticks() - self.start_time
        if elapsed >= ATTACK_DURATION:
            self.alive = False
            return
        for p in self.particles:
            p[0] += p[2]
            p[1] += p[3]

    def draw(self, surface, camera_x):
        elapsed = pygame.time.get_ticks() - self.start_time
        progress = elapsed / ATTACK_DURATION
        alpha = int(180 * (1 - progress))
        for p in self.particles:
            sx = int(p[0] - camera_x)
            sy = int(p[1])
            size = int(p[4] * (1 + progress * 0.5))
            cloud = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(cloud, (GAS_COLOR[0], GAS_COLOR[1], GAS_COLOR[2], alpha), (size, size), size)
            surface.blit(cloud, (sx - size, sy - size))
