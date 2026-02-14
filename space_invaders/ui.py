import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, GREEN, RED, YELLOW


def get_font(size):
    return pygame.font.SysFont(None, size)


def draw_hud(surface, score, high_score, lives):
    font = get_font(28)
    score_text = font.render(f"SCORE: {score}", True, WHITE)
    high_text = font.render(f"HI: {high_score}", True, YELLOW)
    lives_text = font.render(f"LIVES: {lives}", True, GREEN)

    surface.blit(score_text, (10, 10))
    surface.blit(high_text, (SCREEN_WIDTH // 2 - high_text.get_width() // 2, 10))
    surface.blit(lives_text, (SCREEN_WIDTH - lives_text.get_width() - 10, 10))


def draw_title_screen(surface):
    font_big = get_font(64)
    font_small = get_font(28)

    title = font_big.render("SPACE INVADERS", True, GREEN)
    prompt = font_small.render("Press SPACE to Start", True, WHITE)

    surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 200))
    surface.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, 350))


def draw_game_over(surface, score, high_score):
    font_big = get_font(64)
    font_med = get_font(36)
    font_small = get_font(28)

    go_text = font_big.render("GAME OVER", True, RED)
    score_text = font_med.render(f"SCORE: {score}", True, WHITE)
    hi_text = font_med.render(f"HIGH SCORE: {high_score}", True, YELLOW)
    prompt = font_small.render("Press R to Restart", True, WHITE)

    cx = SCREEN_WIDTH // 2
    surface.blit(go_text, (cx - go_text.get_width() // 2, 180))
    surface.blit(score_text, (cx - score_text.get_width() // 2, 280))
    surface.blit(hi_text, (cx - hi_text.get_width() // 2, 330))
    surface.blit(prompt, (cx - prompt.get_width() // 2, 420))
