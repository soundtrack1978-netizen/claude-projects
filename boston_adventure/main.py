import sys
import pygame
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS,
    SKY_BLUE, GROUND_GREEN, GROUND_HEIGHT, CAMERA_OFFSET_X,
    STOMP_BOUNCE,
)
from player import Player
from background import Background
from enemy import create_enemies


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Boston Terrier Adventure")
        self.clock = pygame.time.Clock()
        self.player = Player()
        self.player_group = pygame.sprite.GroupSingle(self.player)
        self.background = Background()
        self.enemies = create_enemies()
        self.camera_x = 0

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
        self.enemies.update()
        self._check_collisions()
        # Camera follows player
        self.camera_x = max(0, self.player.rect.x - CAMERA_OFFSET_X)

    def _check_collisions(self):
        hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
        for enemy in hits:
            # Stomp: player is falling and feet are above enemy's mid-point
            if self.player.vel_y > 0 and self.player.rect.bottom <= enemy.rect.centery + 5:
                enemy.kill()
                self.player.vel_y = STOMP_BOUNCE
            else:
                # Hit from side/below: reset player position
                self.player.reset_position()

    def _draw(self):
        # 1. Sky
        self.screen.fill(SKY_BLUE)
        # 2. Clouds (parallax) + 3. Trees
        self.background.draw(self.screen, self.camera_x)
        # 4. Ground
        ground_rect = pygame.Rect(0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT)
        pygame.draw.rect(self.screen, GROUND_GREEN, ground_rect)
        # 5. Enemies
        for enemy in self.enemies:
            ex = enemy.rect.x - self.camera_x
            if -enemy.rect.width < ex < SCREEN_WIDTH + enemy.rect.width:
                self.screen.blit(enemy.image, (ex, enemy.rect.y))
        # 6. Player (foreground)
        screen_x = self.player.rect.x - self.camera_x
        self.screen.blit(self.player.image, (screen_x, self.player.rect.y))

        pygame.display.flip()


if __name__ == "__main__":
    Game().run()
