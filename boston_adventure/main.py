import sys
import pygame
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS,
    SKY_BLUE, GROUND_GREEN, GROUND_HEIGHT,
)
from player import Player


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Boston Terrier Adventure")
        self.clock = pygame.time.Clock()
        self.player = Player()
        self.player_group = pygame.sprite.GroupSingle(self.player)

    def run(self):
        while True:
            self._handle_events()
            self._update()
            self._draw()
            self.clock.tick(FPS)

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def _update(self):
        self.player_group.update()

    def _draw(self):
        # Sky
        self.screen.fill(SKY_BLUE)
        # Ground
        ground_rect = pygame.Rect(0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT)
        pygame.draw.rect(self.screen, GROUND_GREEN, ground_rect)
        # Player
        self.player_group.draw(self.screen)

        pygame.display.flip()


if __name__ == "__main__":
    Game().run()
