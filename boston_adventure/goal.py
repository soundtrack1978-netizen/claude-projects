import os
import pygame
from settings import (
    GOAL_X, SCREEN_HEIGHT, GROUND_HEIGHT,
)

GOAL_HEIGHT = 100
PERSON_HEIGHT = 20


class Goal(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        base_dir = os.path.dirname(__file__)
        img_path = os.path.join(base_dir, "assets", "house.png")
        raw = pygame.image.load(img_path).convert_alpha()
        # Scale proportionally to GOAL_HEIGHT
        ratio = GOAL_HEIGHT / raw.get_height()
        house_w = int(raw.get_width() * ratio)
        house_img = pygame.transform.scale(raw, (house_w, GOAL_HEIGHT))

        # Build image: GOAL! text + house (no people - drawn separately)
        text_h = 30
        total_h = GOAL_HEIGHT + text_h
        self.image = pygame.Surface((house_w, total_h), pygame.SRCALPHA)

        # "GOAL!" text above house
        font = pygame.font.SysFont(None, 28)
        goal_text = font.render("My Home", True, (255, 50, 50))
        tx = house_w // 2 - goal_text.get_width() // 2
        self.image.blit(goal_text, (tx, 0))

        # House
        self.image.blit(house_img, (0, text_h))

        self.rect = self.image.get_rect()
        self.rect.x = GOAL_X
        self.rect.bottom = SCREEN_HEIGHT - GROUND_HEIGHT + 14  # snug to ground

        # People data (world coordinates, drawn by main.py)
        self.people_colors = [(200, 100, 100), (100, 150, 200), (150, 200, 100)]
        ground_y = SCREEN_HEIGHT - GROUND_HEIGHT - PERSON_HEIGHT
        self.people = []
        for i, color in enumerate(self.people_colors):
            px = GOAL_X + house_w + 8 + i * 14
            self.people.append({
                "x": px,
                "ground_y": ground_y,
                "y": float(ground_y),
                "color": color,
            })

    @staticmethod
    def draw_person(surface, x, y, color):
        """Draw a small person at the given screen position."""
        # Head
        pygame.draw.circle(surface, (240, 200, 160), (x + 4, int(y) + 3), 3)
        # Body
        pygame.draw.rect(surface, color, (x + 1, int(y) + 6, 6, 8))
        # Legs
        pygame.draw.rect(surface, (80, 80, 80), (x + 1, int(y) + 14, 2, 6))
        pygame.draw.rect(surface, (80, 80, 80), (x + 5, int(y) + 14, 2, 6))
