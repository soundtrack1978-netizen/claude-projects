import sys
import pygame
import random
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS,
    SKY_BLUE, GROUND_GREEN, GROUND_HEIGHT, CAMERA_OFFSET_X,
    STOMP_BOUNCE, PLAYER_LIVES, GRAVITY, BLACK, WHITE,
    DEATH_BOUNCE, DEATH_ROTATION_SPEED, BLACKOUT_DURATION,
    KNOCKBACK_DISTANCE, KNOCKBACK_SPEED, KNOCKBACK_JUMP,
    HEART_DROP_CHANCE, POOP_WIDTH, PLAYER_WIDTH,
    WALL1_X, WALL2_X, WALL_HEIGHT, WALL2_HEIGHT, WALL3_X,
    PITS, PIT_WIDTH,
)
from player import Player
from background import Background
from enemy import create_enemies
from goal import Goal
from item import HeartItem, PoopItem
from wall import Wall
from effect import SparkleEffect, GasEffect
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
        self.goal = Goal()
        self.goal_group = pygame.sprite.GroupSingle(self.goal)
        self.wall_group = pygame.sprite.Group(
            Wall(WALL1_X),
            Wall(WALL2_X, WALL2_HEIGHT),
            Wall(WALL3_X),
        )
        self.items = pygame.sprite.Group()
        self.poops = pygame.sprite.Group()
        self.effects = []
        self.dying_enemies = []
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
                if self.state in ("game_over", "clear") and event.key == pygame.K_r:
                    self._restart()

    def _restart(self):
        self.player = Player()
        self.player_group = pygame.sprite.GroupSingle(self.player)
        self.enemies = create_enemies()
        self.goal = Goal()
        self.goal_group = pygame.sprite.GroupSingle(self.goal)
        self.wall_group = pygame.sprite.Group(
            Wall(WALL1_X),
            Wall(WALL2_X, WALL2_HEIGHT),
            Wall(WALL3_X),
        )
        self.items = pygame.sprite.Group()
        self.poops = pygame.sprite.Group()
        self.effects = []
        self.dying_enemies = []
        self.background = Background()
        self.camera_x = 0
        self.lives = PLAYER_LIVES
        self.state = "playing"
        self.knockback_remaining = 0
        self.knockback_dir = 0
        self.knockback_vel_y = 0
        self.knockback_y = 0.0

    def _kill_enemy(self, enemy):
        """Kill enemy with rotation + fall animation."""
        self.dying_enemies.append({
            "image": enemy.image.copy(),
            "x": enemy.rect.centerx,
            "y": float(enemy.rect.y),
            "vel_y": DEATH_BOUNCE,
            "angle": 0,
        })
        if random.random() < HEART_DROP_CHANCE:
            self.items.add(HeartItem(enemy.rect.centerx, enemy.rect.top))
        enemy.kill()

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
        self.player.update(self.wall_group)
        # Fell into pit
        if self.player.rect.top > SCREEN_HEIGHT:
            self._start_death()
            return
        self.enemies.update()
        self.items.update()
        self.poops.update()
        self._check_collisions()
        # Poop attack (2s hold)
        if self.player.pooping:
            self.player.pooping = False
            poop = PoopItem(self.player.rect.left - POOP_WIDTH, self.player.rect.bottom)
            self.poops.add(poop)
        # Poop vs enemies (stationary or flying)
        for poop in self.poops:
            for enemy in pygame.sprite.spritecollide(poop, self.enemies, False):
                self._kill_enemy(enemy)
        # Fart attack
        if self.player.attacking:
            self.player.attacking = False
            gas = GasEffect(self.player.rect.left, self.player.rect.centery)
            self.effects.append(gas)
            # Fart hits poop → launch it (only if right behind player)
            for poop in self.poops:
                if not poop.flying:
                    dist = self.player.rect.left - poop.rect.right
                    if 0 <= dist <= PLAYER_WIDTH:
                        poop.launch()
            # Hit enemies in gas range
            for enemy in list(self.enemies):
                if gas.hit_rect.colliderect(enemy.rect):
                    self._kill_enemy(enemy)
        # Item pickup
        for item in pygame.sprite.spritecollide(self.player, self.items, False):
            if not item.collected and item.pickable:
                item.collect()
                self.lives += 1
                self.effects.append(SparkleEffect(
                    self.player.rect.centerx, self.player.rect.centery,
                ))
        # Update dying enemies
        for de in self.dying_enemies:
            de["vel_y"] += GRAVITY
            de["y"] += de["vel_y"]
            de["angle"] += DEATH_ROTATION_SPEED
        self.dying_enemies = [de for de in self.dying_enemies if de["y"] < SCREEN_HEIGHT + 50]
        # Update effects
        for effect in self.effects:
            effect.update()
        self.effects = [e for e in self.effects if e.alive]
        # Check goal
        if pygame.sprite.spritecollide(self.player, self.goal_group, False):
            self.state = "clear"
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
                self._kill_enemy(enemy)
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
        # 4. Ground (with pit gaps)
        ground_y = SCREEN_HEIGHT - GROUND_HEIGHT
        # Build sorted list of pit screen positions
        pit_edges = []
        for px in sorted(PITS):
            pit_edges.append((px - self.camera_x, px - self.camera_x + PIT_WIDTH))
        # Draw ground segments between pits
        seg_start = 0
        for pit_left, pit_right in pit_edges:
            if pit_left > seg_start:
                pygame.draw.rect(self.screen, GROUND_GREEN,
                                 (seg_start, ground_y, pit_left - seg_start, GROUND_HEIGHT))
            seg_start = pit_right
        if seg_start < SCREEN_WIDTH:
            pygame.draw.rect(self.screen, GROUND_GREEN,
                             (seg_start, ground_y, SCREEN_WIDTH - seg_start, GROUND_HEIGHT))
        # 5. Walls
        for wall in self.wall_group:
            wx = wall.rect.x - self.camera_x
            if -wall.rect.width < wx < SCREEN_WIDTH + wall.rect.width:
                self.screen.blit(wall.image, (wx, wall.rect.y))
        # 6. Goal
        gx = self.goal.rect.x - self.camera_x
        if -self.goal.rect.width < gx < SCREEN_WIDTH + self.goal.rect.width:
            self.screen.blit(self.goal.image, (gx, self.goal.rect.y))
        # 6. Items
        for item in self.items:
            if item.visible:
                ix = item.rect.x - self.camera_x
                if -item.rect.width < ix < SCREEN_WIDTH + item.rect.width:
                    self.screen.blit(item.image, (ix, item.rect.y))
        # 7. Poops
        for poop in self.poops:
            px = poop.rect.x - self.camera_x
            if -poop.rect.width < px < SCREEN_WIDTH + poop.rect.width:
                self.screen.blit(poop.image, (px, poop.rect.y))
        # 8. Enemies
        for enemy in self.enemies:
            ex = enemy.rect.x - self.camera_x
            if -enemy.rect.width < ex < SCREEN_WIDTH + enemy.rect.width:
                self.screen.blit(enemy.image, (ex, enemy.rect.y))
        # 8b. Dying enemies (rotating + falling)
        for de in self.dying_enemies:
            rotated = pygame.transform.rotate(de["image"], de["angle"])
            rx = de["x"] - self.camera_x
            rot_rect = rotated.get_rect(center=(rx, de["y"] + de["image"].get_height() // 2))
            self.screen.blit(rotated, rot_rect)
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
        # 7. Effects (sparkles)
        for effect in self.effects:
            effect.draw(self.screen, self.camera_x)
        # 8. HUD (lives)
        draw_lives(self.screen, self.lives)
        # 8. Blackout screen
        if self.state == "blackout":
            self.screen.fill(BLACK)
            font = pygame.font.SysFont(None, 64)
            text = font.render("GAME OVER", True, WHITE)
            cx = SCREEN_WIDTH // 2 - text.get_width() // 2
            cy = SCREEN_HEIGHT // 2 - text.get_height() // 2
            self.screen.blit(text, (cx, cy))
        # 9. Stage clear
        if self.state == "clear":
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            self.screen.blit(overlay, (0, 0))
            font_big = pygame.font.SysFont(None, 64)
            font_small = pygame.font.SysFont(None, 28)
            clear_text = font_big.render("STAGE CLEAR!", True, (255, 215, 0))
            prompt = font_small.render("Press R to Restart", True, WHITE)
            cx = SCREEN_WIDTH // 2
            self.screen.blit(clear_text, (cx - clear_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
            self.screen.blit(prompt, (cx - prompt.get_width() // 2, SCREEN_HEIGHT // 2 + 20))
        # 10. Game over overlay (restart prompt)
        if self.state == "game_over":
            draw_game_over(self.screen)

        pygame.display.flip()


if __name__ == "__main__":
    Game().run()
