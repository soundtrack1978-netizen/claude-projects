import random
import pygame
from settings import (
    ENEMY_WIDTH, ENEMY_HEIGHT, ENEMY_SPEED, ENEMY_PATROL_RANGE,
    SCREEN_HEIGHT, GROUND_HEIGHT, WORLD_WIDTH, ENEMY_COUNT,
    JUMP_ENEMY_COUNT, JUMP_ENEMY_COLOR,
    JUMP_ENEMY_POWER_MIN, JUMP_ENEMY_POWER_MAX,
    JUMP_ENEMY_INTERVAL_MIN, JUMP_ENEMY_INTERVAL_MAX,
    GRAVITY, GOAL_X,
    PITS, PIT_WIDTH,
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
        # Stop at pit edges (only when actually at the edge)
        for px in PITS:
            pit_right = px + PIT_WIDTH
            if self.direction == 1 and self.rect.right >= px and self.rect.left < px:
                self.rect.right = px
                self.direction = -1
            elif self.direction == -1 and self.rect.left <= pit_right and self.rect.right > pit_right:
                self.rect.left = pit_right
                self.direction = 1


class JumpingEnemy(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface((ENEMY_WIDTH, ENEMY_HEIGHT), pygame.SRCALPHA)
        self._draw_cat()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.ground_y = SCREEN_HEIGHT - GROUND_HEIGHT - ENEMY_HEIGHT
        self.rect.y = self.ground_y
        self.vel_y = 0
        self.last_jump = pygame.time.get_ticks() + random.randint(0, 1500)
        self.jump_interval = random.randint(JUMP_ENEMY_INTERVAL_MIN, JUMP_ENEMY_INTERVAL_MAX)

    def _draw_cat(self):
        w, h = ENEMY_WIDTH, ENEMY_HEIGHT
        color = JUMP_ENEMY_COLOR
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
        # Eyes (red to distinguish)
        pygame.draw.circle(self.image, (200, 0, 0), (6, head_cy - 1), 1)
        pygame.draw.circle(self.image, (200, 0, 0), (10, head_cy - 1), 1)

    def update(self):
        now = pygame.time.get_ticks()
        # Jump at random interval with random height when on ground
        if self.rect.y >= self.ground_y and now - self.last_jump >= self.jump_interval:
            self.vel_y = random.uniform(JUMP_ENEMY_POWER_MAX, JUMP_ENEMY_POWER_MIN)
            self.last_jump = now
            self.jump_interval = random.randint(JUMP_ENEMY_INTERVAL_MIN, JUMP_ENEMY_INTERVAL_MAX)

        # Gravity
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        # Land on ground
        if self.rect.y >= self.ground_y:
            self.rect.y = self.ground_y
            self.vel_y = 0


def create_enemies():
    group = pygame.sprite.Group()

    # Patrol enemies: spread across the world (before goal area)
    patrol_area = GOAL_X - 600
    spacing = patrol_area // (ENEMY_COUNT + 1)
    for i in range(ENEMY_COUNT):
        x = spacing * (i + 1) + random.randint(-50, 50)
        group.add(Enemy(x))

    # Jumping enemies: placed just before the goal
    jump_zone_start = GOAL_X - 500
    jump_spacing = 400 // (JUMP_ENEMY_COUNT + 1)
    for i in range(JUMP_ENEMY_COUNT):
        x = jump_zone_start + jump_spacing * (i + 1)
        group.add(JumpingEnemy(x))

    return group
