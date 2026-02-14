import math
import pygame
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, HEART_COLOR, HEART_SIZE, WHITE, BLACK,
)


def draw_heart(surface, x, y, size):
    """Draw a heart shape at (x, y) with given size."""
    points = []
    for deg in range(360):
        t = math.radians(deg)
        # Heart parametric equation
        hx = 16 * math.sin(t) ** 3
        hy = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
        px = x + hx * size / 32
        py = y + hy * size / 32
        points.append((px, py))
    if len(points) > 2:
        pygame.draw.polygon(surface, HEART_COLOR, points)


def draw_lives(surface, lives):
    """Draw heart icons at top-left of screen."""
    for i in range(lives):
        hx = 20 + i * (HEART_SIZE + 8)
        hy = 20
        draw_heart(surface, hx, hy, HEART_SIZE)


def draw_game_over(surface):
    """Draw game over screen."""
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    surface.blit(overlay, (0, 0))

    font_big = pygame.font.SysFont(None, 64)
    font_small = pygame.font.SysFont(None, 28)

    go_text = font_big.render("GAME OVER", True, WHITE)
    prompt = font_small.render("Press R to Restart", True, WHITE)

    cx = SCREEN_WIDTH // 2
    surface.blit(go_text, (cx - go_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
    surface.blit(prompt, (cx - prompt.get_width() // 2, SCREEN_HEIGHT // 2 + 20))
