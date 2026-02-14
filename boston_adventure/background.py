import random
import pygame
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, GROUND_HEIGHT,
    CLOUD_COUNT, CLOUD_COLOR, CLOUD_PARALLAX,
    TREE_COUNT, TREE_TRUNK_COLOR, TREE_LEAF_COLOR,
    WORLD_WIDTH,
)


class Background:
    def __init__(self):
        self.clouds = self._generate_clouds()
        self.trees = self._generate_trees()

    def _generate_clouds(self):
        clouds = []
        for _ in range(CLOUD_COUNT):
            x = random.randint(0, WORLD_WIDTH)
            y = random.randint(20, 120)
            w = random.randint(60, 120)
            h = random.randint(24, 40)
            clouds.append((x, y, w, h))
        return clouds

    def _generate_trees(self):
        trees = []
        ground_top = SCREEN_HEIGHT - GROUND_HEIGHT
        for _ in range(TREE_COUNT):
            x = random.randint(50, WORLD_WIDTH)
            trunk_h = random.randint(30, 50)
            leaf_r = random.randint(14, 22)
            trees.append((x, ground_top, trunk_h, leaf_r))
        return trees

    def draw(self, surface, camera_x):
        self._draw_clouds(surface, camera_x)
        self._draw_trees(surface, camera_x)

    def _draw_clouds(self, surface, camera_x):
        parallax_x = camera_x * CLOUD_PARALLAX
        for x, y, w, h in self.clouds:
            sx = x - parallax_x
            # Wrap clouds so they always appear on screen
            sx = sx % (WORLD_WIDTH * CLOUD_PARALLAX + SCREEN_WIDTH) - SCREEN_WIDTH * 0.2
            if -w < sx < SCREEN_WIDTH + w:
                # Draw cloud as overlapping ellipses
                pygame.draw.ellipse(surface, CLOUD_COLOR, (sx, y, w, h))
                pygame.draw.ellipse(surface, CLOUD_COLOR, (sx + w * 0.2, y - h * 0.3, w * 0.6, h * 0.8))
                pygame.draw.ellipse(surface, CLOUD_COLOR, (sx - w * 0.15, y + h * 0.1, w * 0.5, h * 0.7))

    def _draw_trees(self, surface, camera_x):
        for x, ground_top, trunk_h, leaf_r in self.trees:
            sx = x - camera_x
            if -40 < sx < SCREEN_WIDTH + 40:
                trunk_w = 8
                trunk_x = sx - trunk_w // 2
                trunk_y = ground_top - trunk_h
                # Trunk
                pygame.draw.rect(surface, TREE_TRUNK_COLOR, (trunk_x, trunk_y, trunk_w, trunk_h))
                # Leaves
                pygame.draw.circle(surface, TREE_LEAF_COLOR, (sx, trunk_y - leaf_r // 2), leaf_r)
