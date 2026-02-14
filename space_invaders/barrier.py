import pygame
from settings import (
    BARRIER_BLOCK_SIZE, BARRIER_COUNT, BARRIER_Y,
    BARRIER_WIDTH, BARRIER_HEIGHT, BARRIER_COLOR, SCREEN_WIDTH,
)


class BarrierBlock(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((BARRIER_BLOCK_SIZE, BARRIER_BLOCK_SIZE))
        self.image.fill(BARRIER_COLOR)
        self.rect = self.image.get_rect(topleft=(x, y))


def create_barriers():
    """Create all barrier groups and return them as a single sprite group."""
    barriers = pygame.sprite.Group()
    spacing = SCREEN_WIDTH // (BARRIER_COUNT + 1)

    for i in range(BARRIER_COUNT):
        center_x = spacing * (i + 1)
        start_x = center_x - BARRIER_WIDTH // 2
        start_y = BARRIER_Y

        cols = BARRIER_WIDTH // BARRIER_BLOCK_SIZE
        rows = BARRIER_HEIGHT // BARRIER_BLOCK_SIZE

        for row in range(rows):
            for col in range(cols):
                # Cut out a notch at the bottom center
                if row >= rows - 2 and cols // 3 <= col < cols * 2 // 3:
                    continue
                bx = start_x + col * BARRIER_BLOCK_SIZE
                by = start_y + row * BARRIER_BLOCK_SIZE
                barriers.add(BarrierBlock(bx, by))

    return barriers
