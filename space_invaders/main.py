import sys
import pygame
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK, BG_COLOR, PLAYER_LIVES, PLAYER_Y,
)
from player import Player
from enemy import EnemyGroup
from bullet import Bullet
from barrier import create_barriers
from ui import draw_hud, draw_title_screen, draw_game_over


class Game:
    STATE_TITLE = 0
    STATE_PLAYING = 1
    STATE_GAME_OVER = 2

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Space Invaders")
        self.clock = pygame.time.Clock()
        self.high_score = 0
        self.state = self.STATE_TITLE
        self._init_game()

    def _init_game(self):
        self.player = Player()
        self.player_group = pygame.sprite.GroupSingle(self.player)
        self.player_bullets = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.enemies = EnemyGroup()
        self.barriers = create_barriers()
        self.score = 0
        self.lives = PLAYER_LIVES

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

            if event.type == pygame.KEYDOWN:
                if self.state == self.STATE_TITLE:
                    if event.key == pygame.K_SPACE:
                        self.state = self.STATE_PLAYING

                elif self.state == self.STATE_PLAYING:
                    if event.key == pygame.K_SPACE:
                        self.player.shoot(self.player_bullets)

                elif self.state == self.STATE_GAME_OVER:
                    if event.key == pygame.K_r:
                        self._init_game()
                        self.state = self.STATE_PLAYING

    def _update(self):
        if self.state != self.STATE_PLAYING:
            return

        # Continuous shooting while holding space
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.player.shoot(self.player_bullets)

        self.player.update()
        self.player_bullets.update()
        self.enemy_bullets.update()
        self.enemies.update()
        self.enemies.shoot(self.enemy_bullets)

        self._check_collisions()

        # Check if enemies reached the bottom
        if self.enemies.reached_bottom(PLAYER_Y):
            self._game_over()

        # Check if all enemies defeated -> next wave
        if len(self.enemies.group) == 0:
            self.enemies = EnemyGroup()
            self.barriers = create_barriers()

    def _check_collisions(self):
        # Player bullets vs enemies
        hits = pygame.sprite.groupcollide(
            self.player_bullets, self.enemies.group, True, True,
        )
        for bullet, enemies_hit in hits.items():
            for enemy in enemies_hit:
                self.score += enemy.score_value

        # Enemy bullets vs player
        if pygame.sprite.spritecollide(self.player, self.enemy_bullets, True):
            self.lives -= 1
            if self.lives <= 0:
                self._game_over()
            else:
                self.player.reset_position()

        # Bullets vs barriers
        pygame.sprite.groupcollide(self.player_bullets, self.barriers, True, True)
        pygame.sprite.groupcollide(self.enemy_bullets, self.barriers, True, True)

        # Enemies vs barriers
        pygame.sprite.groupcollide(self.enemies.group, self.barriers, False, True)

    def _game_over(self):
        if self.score > self.high_score:
            self.high_score = self.score
        self.state = self.STATE_GAME_OVER

    def _draw(self):
        self.screen.fill(BG_COLOR)

        if self.state == self.STATE_TITLE:
            draw_title_screen(self.screen)

        elif self.state == self.STATE_PLAYING:
            self.player_group.draw(self.screen)
            self.player_bullets.draw(self.screen)
            self.enemy_bullets.draw(self.screen)
            self.enemies.group.draw(self.screen)
            self.barriers.draw(self.screen)
            draw_hud(self.screen, self.score, self.high_score, self.lives)

        elif self.state == self.STATE_GAME_OVER:
            draw_game_over(self.screen, self.score, self.high_score)

        pygame.display.flip()


if __name__ == "__main__":
    Game().run()
