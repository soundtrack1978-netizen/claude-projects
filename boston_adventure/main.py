import sys
import pygame
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS,
    SKY_BLUE, GROUND_GREEN, GROUND_HEIGHT, CAMERA_OFFSET_X,
    STOMP_BOUNCE, PLAYER_LIVES, GRAVITY, BLACK, WHITE,
    DEATH_BOUNCE, DEATH_ROTATION_SPEED, BLACKOUT_DURATION,
    KNOCKBACK_DISTANCE, KNOCKBACK_SPEED, KNOCKBACK_JUMP,
)
from player import Player
from background import Background
from enemy import create_enemies
from ui import draw_lives, draw_game_over


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
        self.lives = PLAYER_LIVES
        self.state = "playing"
        self.knockback_remaining = 0
        self.knockback_dir = 0
        self.knockback_vel_y = 0
        self.knockback_y = 0.0

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
                if self.state == "game_over" and event.key == pygame.K_r:
                    self._restart()

    def _restart(self):
        self.player = Player()
        self.player_group = pygame.sprite.GroupSingle(self.player)
        self.enemies = create_enemies()
        self.background = Background()
        self.camera_x = 0
        self.lives = PLAYER_LIVES
        self.state = "playing"
        self.knockback_remaining = 0
        self.knockback_dir = 0
        self.knockback_vel_y = 0
        self.knockback_y = 0.0

    def _start_death(self):
        self.state = "dying"
        self.death_vel_y = DEATH_BOUNCE
        self.death_angle = 0
        self.death_y = float(self.player.rect.y)

    def _update(self):
        if self.state == "dying":
            self._update_death()
            return
        if self.state == "blackout":
            if pygame.time.get_ticks() - self.blackout_start >= BLACKOUT_DURATION:
                self.state = "game_over"
            return
        if self.state != "playing":
            return
        # Knockback animation (horizontal slide + jump arc)
        if self.knockback_remaining > 0 or self.knockback_y < self.player.ground_y:
            # Horizontal
            if self.knockback_remaining > 0:
                step = min(KNOCKBACK_SPEED, self.knockback_remaining)
                self.player.rect.x += step * self.knockback_dir
                self.player.rect.x = max(0, self.player.rect.x)
                self.knockback_remaining -= step
            # Vertical (jump arc)
            self.knockback_vel_y += GRAVITY
            self.knockback_y += self.knockback_vel_y
            if self.knockback_y >= self.player.ground_y:
                self.knockback_y = self.player.ground_y
                # Knockback fully done (landed)
                self.knockback_remaining = 0
                self.knockback_vel_y = 0
                self.player.rect.y = self.player.ground_y
            # Camera still follows during knockback
            self.camera_x = max(0, self.player.rect.x - CAMERA_OFFSET_X)
            return
        self.player_group.update()
        self.enemies.update()
        self._check_collisions()
        # Camera follows player
        self.camera_x = max(0, self.player.rect.x - CAMERA_OFFSET_X)

    def _update_death(self):
        self.death_vel_y += GRAVITY
        self.death_y += self.death_vel_y
        self.death_angle += DEATH_ROTATION_SPEED
        # Once fallen below screen, start blackout
        if self.death_y > SCREEN_HEIGHT + 50:
            self.state = "blackout"
            self.blackout_start = pygame.time.get_ticks()

    def _check_collisions(self):
        hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
        for enemy in hits:
            # Stomp: player is falling and feet are above enemy's mid-point
            if self.player.vel_y > 0 and self.player.rect.bottom <= enemy.rect.centery + 5:
                enemy.kill()
                self.player.vel_y = STOMP_BOUNCE
            elif not self.player.invincible:
                # Knockback direction: away from enemy
                if self.player.rect.centerx < enemy.rect.centerx:
                    self.knockback_dir = -1
                else:
                    self.knockback_dir = 1
                self.knockback_remaining = KNOCKBACK_DISTANCE
                self.knockback_vel_y = KNOCKBACK_JUMP
                self.knockback_y = float(self.player.rect.y)
                # Lose a life
                self.lives -= 1
                if self.lives <= 0:
                    self._start_death()
                else:
                    self.player.start_invincible()

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
        if self.state == "dying":
            # Rotating and falling player
            rotated = pygame.transform.rotate(self.player.image, self.death_angle)
            rot_rect = rotated.get_rect(center=(
                self.player.rect.centerx - self.camera_x,
                self.death_y + self.player.rect.height // 2,
            ))
            self.screen.blit(rotated, rot_rect)
        elif self.player.visible:
            screen_x = self.player.rect.x - self.camera_x
            in_knockback = self.knockback_remaining > 0 or self.knockback_y < self.player.ground_y
            if in_knockback:
                # Draw rotated 90 degrees, using knockback_y for vertical position
                rotated = pygame.transform.rotate(self.player.image, 90)
                rot_rect = rotated.get_rect(center=(
                    screen_x + self.player.rect.width // 2,
                    self.knockback_y + self.player.rect.height // 2,
                ))
                self.screen.blit(rotated, rot_rect)
            else:
                self.screen.blit(self.player.image, (screen_x, self.player.rect.y))
        # 7. HUD (lives)
        draw_lives(self.screen, self.lives)
        # 8. Blackout screen
        if self.state == "blackout":
            self.screen.fill(BLACK)
            font = pygame.font.SysFont(None, 64)
            text = font.render("GAME OVER", True, WHITE)
            cx = SCREEN_WIDTH // 2 - text.get_width() // 2
            cy = SCREEN_HEIGHT // 2 - text.get_height() // 2
            self.screen.blit(text, (cx, cy))
        # 9. Game over overlay (restart prompt)
        if self.state == "game_over":
            draw_game_over(self.screen)

        pygame.display.flip()


if __name__ == "__main__":
    Game().run()
