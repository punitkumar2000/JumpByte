"""Main game loop and integration for players, stages, enemies, and projectiles."""

import math

import pygame

from levels import (
    build_stage_one,
    build_stage_two,
    build_stage_three,
    build_stage_four,
    build_stage_five,
)
from player import Player
from effects import ParticleSystem
from settings import FPS, SCREEN_HEIGHT, SCREEN_WIDTH, WINDOW_TITLE
from ui import UI
from sound_effects import SoundEffects
from save_data import load_best_score, save_best_score


class Game:
    def __init__(self):
        pygame.init()
        self.sounds = SoundEffects()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.world_surface = pygame.Surface(
            (1600, SCREEN_HEIGHT), pygame.SRCALPHA
        )
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.ui = UI()
        self.best_score = load_best_score()
        self.running = True
        self.started = False
        self.camera_x = 0
        self.stage_intro_timer = 0.0
        self.reset_stage()

    def reset_stage(self):
        self.stage_number = 1
        self.stage = build_stage_one()
        self.player = Player(60, 400)
        self.respawn_position = (60, 400)
        self.bullets = []
        self.stomp_effect_timer = 0
        self.stomp_effect_pos = (0, 0)
        self.player_lives = 3
        self.score = 0
        self.hit_cooldown = 0
        self.checkpoint_message_timer = 0.0
        self.game_over = False
        self.game_won = False
        self.paused = False
        self.exit_locked = False
        self.camera_x = 0
        self.particles = ParticleSystem()
        self.camera_shake_timer = 0
        self.prepare_background()

    def add_score(self, points):
        """Award points and persist a new personal best immediately."""
        self.score += points
        if self.score > self.best_score:
            self.best_score = self.score
            save_best_score(self.best_score)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.started = True
                    self.stage_intro_timer = 1.8
                elif (
                    event.key == pygame.K_p
                    and self.started
                    and not self.game_over
                    and not self.game_won
                ):
                    self.paused = not self.paused
                elif event.key == pygame.K_m and self.started:
                    self.sounds.toggle_mute()
                elif event.key == pygame.K_r and (
                    self.game_over or self.game_won
                ):
                    self.reset_stage()
                    self.started = True
                    self.stage_intro_timer = 1.8

    def lose_life(self):
        if self.hit_cooldown > 0 or self.game_over:
            return

        self.player_lives -= 1
        self.sounds.play_damage()
        self.particles.burst(*self.player.rect.center, (255, 105, 115), 16, 190)
        self.camera_shake_timer = 18
        self.hit_cooldown = 75
        self.player.rect.topleft = self.respawn_position
        self.player.velocity_y = 0
        self.player.on_ground = False

        if self.player_lives <= 0:
            self.game_over = True

    def check_stage_exit(self):
        all_coins_collected = all(
            coin.collected for coin in self.stage["coins"]
        )
        boss_alive = any(
            getattr(enemy, "is_boss", False)
            for enemy in self.stage["enemies"]
        )
        reached_exit = self.player.rect.right >= 1540

        self.exit_locked = reached_exit and (
            not all_coins_collected or boss_alive
        )

        if not reached_exit or not all_coins_collected or boss_alive:
            return

        self.add_score(500)

        if self.stage_number == 1:
            self.stage_number = 2
            self.stage = build_stage_two()
        elif self.stage_number == 2:
            self.stage_number = 3
            self.stage = build_stage_three()
        elif self.stage_number == 3:
            self.stage_number = 4
            self.stage = build_stage_four()
        elif self.stage_number == 4:
            self.stage_number = 5
            self.stage = build_stage_five()
        else:
            self.add_score(1000)
            self.game_won = True
            return

        self.stage_intro_timer = 1.8
        self.prepare_background()
        self.player = Player(60, 400)
        self.respawn_position = (60, 400)
        self.checkpoint_message_timer = 0.0
        self.bullets.clear()
        self.stomp_effect_timer = 0
        self.exit_locked = False
        self.camera_x = 0

    def update(self, dt=1 / FPS):
        if (
            not self.started
            or self.game_over
            or self.game_won
            or self.paused
        ):
            return

        self.stage_intro_timer = max(0.0, self.stage_intro_timer - dt)
        self.checkpoint_message_timer = max(
            0.0, self.checkpoint_message_timer - dt
        )

        if self.stomp_effect_timer > 0:
            self.stomp_effect_timer -= 1
        if self.camera_shake_timer > 0:
            self.camera_shake_timer -= 1
        self.particles.update(dt)

        keys = pygame.key.get_pressed()
        jump_pressed = (
            keys[pygame.K_SPACE]
            or keys[pygame.K_UP]
            or keys[pygame.K_w]
        )

        if jump_pressed and self.player.on_ground:
            self.sounds.play_jump()
            self.particles.burst(
                self.player.rect.centerx, self.player.rect.bottom,
                (205, 190, 155), 8, 75,
            )

        was_airborne = not self.player.on_ground
        previous_vertical_speed = self.player.velocity_y
        self.player.update(keys, self.stage["platforms"])
        if was_airborne and self.player.on_ground and previous_vertical_speed > 0:
            landing_color = (225, 245, 255) if self.stage_number == 4 else (205, 190, 155)
            self.particles.burst(
                self.player.rect.centerx, self.player.rect.bottom,
                landing_color, 8, 80,
            )

        for hazard in self.stage.get("hazards", []):
            if hazard.rect.colliderect(self.player.rect):
                self.lose_life()
                break

        # First time crossing the midpoint activates a properly floor-aligned
        # checkpoint and gives clear visual/audio feedback.
        if (
            self.player.rect.centerx >= 800
            and self.respawn_position == (60, 400)
        ):
            self.respawn_position = (
                760,
                490 - self.player.rect.height,
            )
            self.checkpoint_message_timer = 1.8
            self.add_score(200)
            self.particles.burst(800, 350, (115, 255, 160), 22, 150)
            self.sounds.play_checkpoint()

        if self.hit_cooldown > 0:
            self.hit_cooldown -= 1

        for enemy in self.stage["enemies"][:]:
            enemy.update()

            if enemy.ready_to_shoot():
                self.bullets.append(enemy.shoot(self.player.rect))

            if enemy.check_collision(self.player.rect) and self.hit_cooldown == 0:
                # Neeche girte hue enemy ke upar land kiya toh stomp hoga
                if (
                    self.player.velocity_y > 0
                    and self.player.rect.bottom < enemy.rect.centery
                ):
                    self.stomp_effect_pos = enemy.rect.center
                    self.stomp_effect_timer = 18
                    self.particles.burst(
                        *enemy.rect.center, (255, 190, 95), 18, 210
                    )
                    self.sounds.play_stomp()
                    self.player.velocity_y = -10
                    self.hit_cooldown = 18

                    if getattr(enemy, "is_boss", False):
                        self.add_score(250)
                        enemy.health -= 1
                        if enemy.health <= 0:
                            self.add_score(500)
                            self.stage["enemies"].remove(enemy)
                    else:
                        self.add_score(200)
                        self.stage["enemies"].remove(enemy)
                else:
                    self.lose_life()

        for bullet in self.bullets:
            bullet.update()
            if bullet.rect.colliderect(self.player.rect):
                self.lose_life()
                bullet.rect.x = -100

        self.bullets = [
            bullet for bullet in self.bullets
            if bullet.rect.right > 0 and bullet.rect.left < 1600
        ]

        for coin in self.stage["coins"]:
            if not coin.collected and self.player.rect.colliderect(coin.rect):
                coin.collected = True
                self.add_score(100)
                self.sounds.play_coin()
                self.particles.burst(*coin.rect.center, (255, 220, 85), 14, 165)

        for powerup in self.stage.get("powerups", []):
            if not powerup.collected and self.player.rect.colliderect(powerup.rect):
                powerup.collected = True
                self.player.speed_boost_timer = 300
                self.add_score(50)
                self.sounds.play_powerup()
                self.particles.burst(
                    *powerup.rect.center, (120, 235, 255), 20, 185
                )

        self.check_stage_exit()

        self.camera_x = max(
            0,
            min(
                self.player.rect.centerx - SCREEN_WIDTH // 2,
                1600 - SCREEN_WIDTH,
            ),
        )

    def draw_exit_gate(self, world, locked=True):
        # Gate pole and base
        pygame.draw.rect(world, (90, 70, 55), (1530, 405, 8, 85))
        pygame.draw.rect(world, (145, 115, 80), (1527, 480, 14, 10))
        pygame.draw.circle(world, (255, 220, 120), (1534, 402), 5)

        # Gently waving flag
        wave = (pygame.time.get_ticks() // 250) % 2
        tip_x = 1580 if wave == 0 else 1573
        middle_y = 421 if wave == 0 else 424

        flag_color = (155, 165, 185) if locked else (245, 190, 65)
        pygame.draw.polygon(
            world,
            flag_color,
            [(1538, 405), (tip_x, middle_y), (1538, 438)],
        )
        pygame.draw.line(
            world,
            (215, 220, 235) if locked else (255, 230, 145),
            (1541, 411),
            (tip_x - 8, middle_y),
            2,
        )
        if locked:
            pygame.draw.arc(
                world, (220, 220, 230), (1542, 447, 12, 13),
                math.pi, 2 * math.pi, 2,
            )
            pygame.draw.rect(
                world, (220, 220, 230), (1541, 453, 14, 11),
                border_radius=2,
            )
        else:
            pulse = (math.sin(pygame.time.get_ticks() / 160) + 1) / 2
            pygame.draw.circle(
                world, (255, 225, 125, 90 + round(pulse * 90)),
                (1538, 421), 18 + round(pulse * 3), 2,
            )

    def draw_scenery(self, world):
        if self.stage_number == 1:
            # Green Meadow hills
            pygame.draw.ellipse(world, (125, 190, 120), (-100, 365, 650, 260))
            pygame.draw.ellipse(world, (105, 175, 105), (400, 390, 750, 250))
            pygame.draw.ellipse(world, (85, 155, 95), (950, 360, 750, 280))

            # Small flowers in the meadow
            for x, y, color in [
                (70, 460, (255, 220, 90)),
                (385, 465, (250, 130, 160)),
                (610, 450, (255, 220, 90)),
                (920, 465, (250, 130, 160)),
                (1170, 455, (255, 220, 90)),
                (1510, 465, (250, 130, 160)),
            ]:
                pygame.draw.line(
                    world, (45, 125, 65), (x, y), (x, y + 14), 2
                )
                pygame.draw.circle(world, color, (x, y), 4)
                pygame.draw.circle(
                    world, (255, 245, 220), (x - 4, y), 3
                )
                pygame.draw.circle(
                    world, (255, 245, 220), (x + 4, y), 3
                )

        elif self.stage_number == 2:
            # Hanging cave rocks
            for x, width, height in [
                (80, 100, 75),
                (340, 130, 95),
                (700, 110, 65),
                (1050, 140, 100),
                (1390, 120, 80),
            ]:
                pygame.draw.polygon(
                    world,
                    (70, 58, 95),
                    [
                        (x, 0),
                        (x + width, 0),
                        (x + width // 2, height),
                    ],
                )

            # Glowing cave crystals
            for x, y, color in [
                (180, 455, (90, 235, 245)),
                (560, 450, (175, 125, 255)),
                (900, 460, (90, 235, 245)),
                (1280, 450, (175, 125, 255)),
            ]:
                pygame.draw.polygon(
                    world,
                    color,
                    [
                        (x, y + 22),
                        (x - 10, y),
                        (x - 4, y + 3),
                        (x, y - 14),
                        (x + 5, y + 2),
                        (x + 11, y + 22),
                    ],
                )
                pygame.draw.line(
                    world, (235, 250, 255), (x, y - 8), (x - 3, y + 10), 2
                )

        elif self.stage_number == 3:
            # Sunset Castle in the distance
            pygame.draw.ellipse(world, (135, 83, 110), (-80, 405, 700, 180))
            pygame.draw.ellipse(world, (120, 70, 100), (700, 390, 950, 200))

            # Castle walls and towers
            pygame.draw.rect(world, (75, 53, 88), (260, 300, 280, 190))
            pygame.draw.rect(world, (65, 46, 80), (300, 250, 65, 240))
            pygame.draw.rect(world, (65, 46, 80), (435, 250, 65, 240))

            # Tower roofs
            pygame.draw.polygon(
                world, (55, 42, 72), [(285, 250), (380, 250), (332, 195)]
            )
            pygame.draw.polygon(
                world, (55, 42, 72), [(420, 250), (515, 250), (468, 195)]
            )

            # Glowing windows
            pygame.draw.rect(world, (245, 190, 100), (325, 330, 28, 45))
            pygame.draw.rect(world, (245, 190, 100), (445, 330, 28, 45))
            pygame.draw.rect(world, (245, 190, 100), (380, 400, 40, 90))

            # Setting sun and castle flags
            pygame.draw.circle(world, (255, 175, 105), (1350, 190), 58)
            pygame.draw.circle(world, (255, 205, 125), (1350, 190), 43)

            pygame.draw.line(
                world, (225, 205, 175), (332, 178), (332, 205), 3
            )
            pygame.draw.polygon(
                world,
                (235, 95, 110),
                [(334, 180), (365, 188), (334, 197)],
            )

            pygame.draw.line(
                world, (225, 205, 175), (468, 178), (468, 205), 3
            )
            pygame.draw.polygon(
                world,
                (100, 190, 220),
                [(470, 180), (500, 188), (470, 197)],
            )

        elif self.stage_number == 4:
            # Frostfall Peaks: icy mountains and snow
            pygame.draw.circle(world, (225, 245, 255), (1320, 115), 48)

            pygame.draw.polygon(
                world, (80, 145, 190),
                [(0, 450), (210, 190), (420, 450)],
            )
            pygame.draw.polygon(
                world, (110, 175, 210),
                [(260, 450), (560, 150), (850, 450)],
            )
            pygame.draw.polygon(
                world, (75, 135, 185),
                [(690, 450), (1010, 205), (1300, 450)],
            )
            pygame.draw.polygon(
                world, (105, 165, 205),
                [(1110, 450), (1390, 170), (1650, 450)],
            )

            # Snow caps
            pygame.draw.polygon(
                world, (240, 250, 255),
                [(210, 190), (165, 245), (205, 232), (235, 250)],
            )
            pygame.draw.polygon(
                world, (245, 252, 255),
                [(560, 150), (500, 230), (555, 210), (600, 240)],
            )
            pygame.draw.polygon(
                world, (240, 250, 255),
                [(1010, 205), (955, 255), (1005, 240), (1040, 260)],
            )
            pygame.draw.polygon(
                world, (245, 252, 255),
                [(1390, 170), (1335, 235), (1385, 218), (1420, 245)],
            )

        else:
            # Skyforge Citadel: starry sky and floating towers
            pygame.draw.circle(world, (245, 205, 130), (1320, 175), 52)
            pygame.draw.circle(world, (255, 225, 165), (1320, 175), 38)

            # Distant floating islands
            pygame.draw.ellipse(world, (75, 95, 145), (90, 340, 300, 55))
            pygame.draw.polygon(
                world, (65, 80, 125),
                [(140, 365), (340, 365), (290, 435), (190, 435)],
            )
            pygame.draw.ellipse(world, (85, 100, 155), (1030, 355, 350, 55))
            pygame.draw.polygon(
                world, (65, 80, 125),
                [(1090, 378), (1320, 378), (1265, 445), (1145, 445)],
            )

            # Citadel towers in the distance
            pygame.draw.rect(world, (70, 68, 125), (470, 265, 95, 225))
            pygame.draw.polygon(
                world, (95, 88, 155),
                [(455, 265), (580, 265), (518, 195)],
            )
            pygame.draw.rect(world, (70, 68, 125), (620, 320, 70, 170))
            pygame.draw.polygon(
                world, (95, 88, 155),
                [(608, 320), (702, 320), (655, 260)],
            )

            # Glowing windows
            pygame.draw.rect(world, (255, 215, 115), (500, 315, 22, 35))
            pygame.draw.rect(world, (255, 215, 115), (535, 315, 22, 35))
            pygame.draw.rect(world, (130, 225, 255), (643, 365, 18, 30))

    def prepare_background(self):
        """Cache the detailed scenery so it scrolls behind the gameplay layer."""
        self.background_surface = pygame.Surface((1600, SCREEN_HEIGHT))
        self.background_surface.fill(self.stage["info"]["background"])
        self.draw_scenery(self.background_surface)

    def draw_ambient(self, surface):
        """Add lightweight animated weather and sky details for each world."""
        time = pygame.time.get_ticks() / 1000

        if self.stage_number == 1:
            cloud_y = (88, 145, 72, 118, 60)
            for index, base_x in enumerate((80, 420, 790, 1160, 1530)):
                x = int((base_x - time * 11) % 1780 - self.camera_x * 0.16)
                y = cloud_y[index]
                if -90 < x < SCREEN_WIDTH + 70:
                    cloud = (240, 250, 255)
                    pygame.draw.ellipse(surface, cloud, (x, y + 9, 62, 25))
                    pygame.draw.circle(surface, cloud, (x + 20, y + 9), 18)
                    pygame.draw.circle(surface, cloud, (x + 43, y + 7), 22)

        elif self.stage_number in (2, 5):
            stars = [
                (70, 82), (190, 145), (310, 66), (455, 115), (585, 58),
                (730, 136), (860, 78), (1010, 125), (1180, 60),
                (1340, 142), (1510, 90),
            ]
            for index, (x, y) in enumerate(stars):
                screen_x = int(x - self.camera_x * 0.22)
                if 0 <= screen_x < SCREEN_WIDTH:
                    brightness = 170 + int((math.sin(time * 2.4 + index) + 1) * 42)
                    color = (brightness, brightness, 255) if self.stage_number == 2 else (255, 235, brightness)
                    pygame.draw.circle(
                        surface, color, (screen_x, y),
                        1 + int(index % 3 == 0),
                    )
                    if index % 4 == 0 and brightness > 245:
                        pygame.draw.line(surface, color, (screen_x - 4, y), (screen_x + 4, y), 1)
                        pygame.draw.line(surface, color, (screen_x, y - 4), (screen_x, y + 4), 1)

        elif self.stage_number == 4:
            for index in range(30):
                speed = 22 + (index % 5) * 8
                x = int((index * 97 + math.sin(time + index) * 18 - time * speed) % SCREEN_WIDTH)
                y = int((index * 61 + time * speed * 1.35) % SCREEN_HEIGHT)
                pygame.draw.line(surface, (238, 250, 255), (x, y), (x - 2, y + 6), 2)

    def draw(self):
        self.screen.fill(self.stage["info"]["background"])
        self.screen.blit(
            self.background_surface,
            (-int(self.camera_x * 0.28), 0),
        )
        self.draw_ambient(self.screen)

        # Keep the last gameplay frame visible behind pause, win, and
        # game-over panels. The simulation is already stopped in update().
        if self.started:
            world = self.world_surface
            world.fill((0, 0, 0, 0))

            for platform in self.stage["platforms"]:
                platform.draw(world)

            for hazard in self.stage.get("hazards", []):
                hazard.draw(world)

            # Gray checkpoint becomes green after activation.
            flag_color = (
                (65, 210, 130)
                if self.respawn_position != (60, 400)
                else (185, 185, 195)
            )

            pygame.draw.rect(world, (90, 70, 55), (796, 350, 6, 55))
            pygame.draw.polygon(
                world,
                flag_color,
                [(802, 351), (836, 361), (802, 373)],
            )
            pygame.draw.circle(world, (255, 245, 190), (799, 348), 4)

            for coin in self.stage["coins"]:
                coin.draw(world)

            for powerup in self.stage.get("powerups", []):
                powerup.draw(world)

            for enemy in self.stage["enemies"]:
                enemy.draw(world)

            if self.stomp_effect_timer > 0:
                effect_age = 18 - self.stomp_effect_timer
                radius = 8 + effect_age * 2
                pygame.draw.circle(
                    world,
                    (255, 230, 120),
                    self.stomp_effect_pos,
                    radius,
                    3,
                )

            for bullet in self.bullets:
                bullet.draw(world)

            boss_alive = any(
                getattr(enemy, "is_boss", False)
                for enemy in self.stage["enemies"]
            )
            coins_missing = any(
                not coin.collected for coin in self.stage["coins"]
            )
            self.draw_exit_gate(world, locked=coins_missing or boss_alive)
            self.player.draw(world, self.hit_cooldown)
            self.particles.draw(world)

            shake = self.camera_shake_timer / 18
            shake_x = round(math.sin(pygame.time.get_ticks() * 0.09) * 4 * shake)
            shake_y = round(math.cos(pygame.time.get_ticks() * 0.12) * 2 * shake)
            self.screen.blit(world, (-self.camera_x + shake_x, shake_y))

            coin_count = sum(
                1 for coin in self.stage["coins"] if coin.collected
            )
            self.ui.draw_hud(
                self.screen,
                self.stage["info"]["name"],
                coin_count,
                self.player_lives,
                self.player.speed_boost_timer,
                total_coins=len(self.stage["coins"]),
                progress=self.player.rect.centerx / 1600,
                stage_number=self.stage_number,
                sound_muted=self.sounds.muted,
                score=self.score,
            )

            # Exit par coins baaki hon toh player ko reason dikhega.
            if self.exit_locked:
                boss_alive = any(
                    getattr(enemy, "is_boss", False)
                    for enemy in self.stage["enemies"]
                )
                coins_missing = coin_count < len(self.stage["coins"])

                if boss_alive and coins_missing:
                    message_text = "Collect all coins and defeat the boss!"
                elif boss_alive:
                    message_text = "Defeat the boss to unlock the exit!"
                else:
                    message_text = "Collect all coins to unlock the exit!"

                self.ui.draw_banner(
                    self.screen, message_text, SCREEN_HEIGHT - 44
                )

            if self.checkpoint_message_timer > 0:
                alpha = (
                    220 if self.checkpoint_message_timer > 0.3
                    else round(220 * self.checkpoint_message_timer / 0.3)
                )
                self.ui.draw_banner(
                    self.screen,
                    "Checkpoint reached! You will respawn here.",
                    SCREEN_HEIGHT - 92,
                    alpha,
                )

            if self.stage_intro_timer > 0:
                self.ui.draw_world_intro(
                    self.screen,
                    self.stage_number,
                    self.stage["info"]["name"],
                    self.stage_intro_timer,
                )

        if not self.started:
            self.ui.draw_start(self.screen)
        elif self.game_over:
            self.ui.draw_game_over(self.screen, self.score, self.best_score)
        elif self.game_won:
            self.ui.draw_win(self.screen, self.score, self.best_score)
        elif self.paused:
            self.ui.draw_pause(self.screen)

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            dt = min(self.clock.tick(FPS) / 1000.0, 0.05)
            self.update(dt)
            self.draw()

        pygame.quit()
