import pygame
import random
from settings import (
    ENEMY_WIDTH, ENEMY_HEIGHT, ENEMY_ROWS, ENEMY_COLS,
    ENEMY_H_SPACING, ENEMY_V_SPACING, ENEMY_START_X, ENEMY_START_Y,
    ENEMY_H_SPEED, ENEMY_V_STEP, ENEMY_SHOOT_INTERVAL,
    ENEMY_COLOR_TOP, ENEMY_COLOR_BOTTOM, SCREEN_WIDTH,
    ENEMY_BULLET_SPEED, ENEMY_BULLET_COLOR,
    ENEMY_SCORE, ENEMY_SCORE_TOP,
)
from bullet import Bullet


class Enemy(pygame.sprite.Sprite):
    def __init__(self, row, col):
        super().__init__()
        self.row = row
        color = ENEMY_COLOR_TOP if row < 2 else ENEMY_COLOR_BOTTOM
        self.score_value = ENEMY_SCORE_TOP if row < 2 else ENEMY_SCORE
        self.image = pygame.Surface((ENEMY_WIDTH, ENEMY_HEIGHT), pygame.SRCALPHA)
        # Draw a symbolic full-body cat
        w, h = ENEMY_WIDTH, ENEMY_HEIGHT
        # Body (oval)
        pygame.draw.ellipse(self.image, color, (4, h // 3, w - 12, h * 2 // 3))
        # Head (circle)
        head_cx, head_cy = 8, h // 3
        pygame.draw.circle(self.image, color, (head_cx, head_cy), 7)
        # Ears (triangles)
        pygame.draw.polygon(self.image, color, [(3, head_cy - 5), (1, head_cy - 13), (8, head_cy - 7)])
        pygame.draw.polygon(self.image, color, [(13, head_cy - 5), (15, head_cy - 13), (8, head_cy - 7)])
        # Tail (curved upward)
        pygame.draw.arc(self.image, color, (w - 16, 0, 14, h // 2), 0, 2.5, 2)
        # Legs (small rectangles)
        pygame.draw.rect(self.image, color, (8, h - 5, 3, 5))
        pygame.draw.rect(self.image, color, (18, h - 5, 3, 5))
        # Eyes (small dots)
        eye_color = (0, 0, 0)
        pygame.draw.circle(self.image, eye_color, (6, head_cy - 1), 1)
        pygame.draw.circle(self.image, eye_color, (10, head_cy - 1), 1)
        self.rect = self.image.get_rect(
            x=ENEMY_START_X + col * ENEMY_H_SPACING,
            y=ENEMY_START_Y + row * ENEMY_V_SPACING,
        )


class EnemyGroup:
    def __init__(self):
        self.group = pygame.sprite.Group()
        self.direction = 1  # 1=right, -1=left
        self.last_shot_time = 0
        self._create_formation()

    def _create_formation(self):
        for row in range(ENEMY_ROWS):
            for col in range(ENEMY_COLS):
                self.group.add(Enemy(row, col))

    def update(self):
        # Check if any enemy hit the edge
        drop = False
        for enemy in self.group:
            if self.direction == 1 and enemy.rect.right >= SCREEN_WIDTH - 10:
                drop = True
                break
            if self.direction == -1 and enemy.rect.left <= 10:
                drop = True
                break

        if drop:
            self.direction *= -1
            for enemy in self.group:
                enemy.rect.y += ENEMY_V_STEP
        else:
            for enemy in self.group:
                enemy.rect.x += ENEMY_H_SPEED * self.direction

    def shoot(self, enemy_bullets):
        now = pygame.time.get_ticks()
        if now - self.last_shot_time < ENEMY_SHOOT_INTERVAL:
            return
        if not self.group:
            return

        # Find bottom-most enemy in each column and pick one randomly
        columns = {}
        for enemy in self.group:
            col_key = enemy.rect.centerx // ENEMY_H_SPACING
            if col_key not in columns or enemy.rect.bottom > columns[col_key].rect.bottom:
                columns[col_key] = enemy

        if columns:
            shooter = random.choice(list(columns.values()))
            bullet = Bullet(
                shooter.rect.centerx, shooter.rect.bottom,
                ENEMY_BULLET_SPEED, ENEMY_BULLET_COLOR,
            )
            enemy_bullets.add(bullet)
            self.last_shot_time = now

    def reached_bottom(self, y_limit):
        for enemy in self.group:
            if enemy.rect.bottom >= y_limit:
                return True
        return False
