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

        # Build combined image: GOAL! text + house + 3 people
        people_area = 50
        total_w = house_w + people_area
        text_h = 30
        total_h = GOAL_HEIGHT + text_h
        self.image = pygame.Surface((total_w, total_h), pygame.SRCALPHA)

        # "GOAL!" text above house
        font = pygame.font.SysFont(None, 28)
        goal_text = font.render("GOAL!", True, (255, 50, 50))
        tx = house_w // 2 - goal_text.get_width() // 2
        self.image.blit(goal_text, (tx, 0))

        # House
        self.image.blit(house_img, (0, text_h))

        # 3 people to the right of the house
        ground_bottom = text_h + GOAL_HEIGHT
        colors = [(200, 100, 100), (100, 150, 200), (150, 200, 100)]
        for i, color in enumerate(colors):
            px = house_w + 8 + i * 14
            py = ground_bottom - PERSON_HEIGHT
            # Head
            pygame.draw.circle(self.image, (240, 200, 160), (px + 4, py + 3), 3)
            # Body
            pygame.draw.rect(self.image, color, (px + 1, py + 6, 6, 8))
            # Legs
            pygame.draw.rect(self.image, (80, 80, 80), (px + 1, py + 14, 2, 6))
            pygame.draw.rect(self.image, (80, 80, 80), (px + 5, py + 14, 2, 6))

        self.rect = self.image.get_rect()
        self.rect.x = GOAL_X
        self.rect.bottom = SCREEN_HEIGHT - GROUND_HEIGHT
