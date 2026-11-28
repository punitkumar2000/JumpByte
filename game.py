"""Main game loop and integration for players, stages, enemies, and projectiles."""

import math
import random

import pygame

from levels import (
    build_stage_one,
    build_stage_two,
    build_stage_three,
    build_stage_four,
    build_stage_five,
    build_stage_six,
    build_stage_seven,
    build_stage_eight,
    build_stage_nine,
    build_stage_ten,
)
from objects import CheeseDrop, PlayerShot
from player import Player
from effects import ParticleSystem
from settings import (
    CHECKPOINT_X,
    EXIT_REACHED_X,
    FIRE_POWER_SECONDS,
    FPS,
    MAX_LIVES,
    PLAYER_START_POSITION,
    QUIZ_GATE_X,
    QUIZ_QUESTIONS_PER_WORLD,
    SCORE_BOSS_DEFEAT,
    SCORE_BOSS_HIT,
    SCORE_BOSS_STOMP,
    SCORE_CHECKPOINT,
    SCORE_CHEESE,
    SCORE_COIN,
    SCORE_CORRECT_ANSWER,
    SCORE_ENEMY_SHOT,
    SCORE_ENEMY_STOMP,
    SCORE_GAME_COMPLETE,
    SCORE_POWERUP,
    SCORE_WORLD_CLEAR,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SHOT_COOLDOWN_SECONDS,
    SPEED_BOOST_FRAMES,
    TOTAL_STAGES,
    WORLD_WIDTH,
    WINDOW_TITLE,
)
from ui import UI
from python_concepts import PYTHON_LESSONS
from sound_effects import SoundEffects
from save_data import (
    load_best_score,
    load_player_profile,
    save_best_score,
    save_player_profile,
)
from python_challenges import PYTHON_CHALLENGES, PYTHON_CODE_CHALLENGES


class Game:
    def __init__(self):
        pygame.init()
        self.sounds = SoundEffects()
        self.screen = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT),
            pygame.SCALED | pygame.RESIZABLE,
        )
        self.world_surface = pygame.Surface(
            (WORLD_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA
        )
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.ui = UI()
        self.best_score = load_best_score()
        self.profile_name_input = ""
        self.profile_name = ""
        self.profile_data = load_player_profile("")
        self.profile_preview = self.profile_data
        pygame.key.start_text_input()
        self.running = True
        self.started = False
        self.show_world_map = False
        self.camera_x = 0
        self.stage_intro_timer = 0.0
        self.reset_stage()

    def reset_stage(self):
        self.stage_number = 1
        self.stage = build_stage_one()
        self.player = Player(*PLAYER_START_POSITION)
        self.respawn_position = PLAYER_START_POSITION
        self.bullets = []
        self.player_shots = []
        self.bullet_power_timer = 0.0
        self.shot_cooldown = 0.0
        self.cheese_drops = []
        self.stomp_effect_timer = 0
        self.stomp_effect_pos = (0, 0)
        self.player_lives = MAX_LIVES
        self.score = 0
        self.stage_start_score = 0
        self.stage_points = 0
        self.worlds_cleared = 0
        self.questions_asked = 0
        self.questions_correct = 0
        self.learning_concepts = set()
        self.stage_questions_asked = 0
        self.stage_questions_correct = 0
        self.stage_learning_concepts = set()
        self.challenge_history = {
            world_number: set() for world_number in PYTHON_CHALLENGES
        }
        self.challenge_questions = []
        self.challenge_question_index = 0
        self.python_coach_enabled = True
        self.python_tip = None
        self.python_tip_timer = 0.0
        self.shown_python_tips = set()
        self.hit_cooldown = 0
        self.checkpoint_message_timer = 0.0
        self.game_over = False
        self.game_won = False
        self.paused = False
        self.pause_selection = 1  # Resume is selected by default.
        self.exit_locked = False
        self.challenge_open = False
        self.stage_summary_open = False
        self.challenge_solved = False
        self.challenge_answered = False
        self.challenge_feedback = ""
        self.active_challenge = None
        self.reset_code_checkpoint()
        self.camera_x = 0
        self.particles = ParticleSystem()
        self.camera_shake_timer = 0
        self.prepare_background()

    def reset_code_checkpoint(self):
        """Choose one random code-question point for the current world."""
        self.code_checkpoint_x = random.randint(WORLD_WIDTH // 4, WORLD_WIDTH * 3 // 4)
        self.code_checkpoint_done = False
        self.code_challenge_open = False
        self.code_challenge_answered = False
        self.code_challenge_feedback = ""
        self.active_code_challenge = None

    def add_score(self, points):
        """Award points and persist a new personal best immediately."""
        self.score += points
        if self.score > self.best_score:
            self.best_score = self.score
            save_best_score(self.best_score)
        if self.profile_name:
            self.profile_data["best_score"] = self.best_score
            self.save_profile_progress()

    def save_profile_progress(self):
        """Save the selected player's score and learning progress."""
        if not self.profile_name:
            return

        saved = load_player_profile(self.profile_name)
        saved["best_score"] = max(saved["best_score"], self.best_score)
        saved["best_worlds_cleared"] = max(
            saved["best_worlds_cleared"], self.worlds_cleared
        )
        has_run_progress = (
            self.worlds_cleared > 0
            or self.questions_asked > 0
            or self.score > 0
            or self.game_over
        )
        if self.questions_asked > 0 or self.worlds_cleared > 0 or self.game_over:
            saved["last_questions_asked"] = self.questions_asked
            saved["last_questions_correct"] = self.questions_correct
        if has_run_progress:
            saved["last_score"] = self.score
        saved["concepts_learned"] = sorted(
            set(saved["concepts_learned"]) | self.learning_concepts
        )
        self.profile_data = saved
        save_player_profile(self.profile_name, saved)

    def drop_cheese(self, enemy):
        for direction in (-2, -1, 1, 2):
            drop = CheeseDrop(
                enemy.rect.centerx - 7,
                enemy.rect.top,
                direction,
            )
            self.cheese_drops.append(drop)

    def show_python_tip(self, lesson_name):
        """Show each Python lesson only once during this playthrough."""
        if (
            self.python_coach_enabled
            and lesson_name not in self.shown_python_tips
        ):
            self.shown_python_tips.add(lesson_name)
            self.learning_concepts.add(lesson_name.replace("_", " ").title())
            self.stage_learning_concepts.add(lesson_name.replace("_", " ").title())
            self.python_tip = PYTHON_LESSONS[lesson_name]
            self.python_tip_timer = 3.5
            self.save_profile_progress()

    def open_python_challenge(self):
        if self.challenge_open:
            return

        all_coins_collected = all(
            coin.collected for coin in self.stage["coins"]
        )
        boss_alive = any(
            getattr(enemy, "is_boss", False)
            for enemy in self.stage["enemies"]
        )
        near_exit = self.player.rect.right >= QUIZ_GATE_X

        if (
            near_exit
            and all_coins_collected
            and not boss_alive
            and not self.challenge_solved
        ):
            question_pool = PYTHON_CHALLENGES[self.stage_number]
            used_questions = self.challenge_history[self.stage_number]
            available_questions = [
                index
                for index in range(len(question_pool))
                if index not in used_questions
            ]

            # Pick two different questions and avoid repeats until this
            # world's question bank has been used once.
            if len(available_questions) < QUIZ_QUESTIONS_PER_WORLD:
                used_questions.clear()
                available_questions = list(range(len(question_pool)))

            selected_indices = random.sample(
                available_questions,
                min(QUIZ_QUESTIONS_PER_WORLD, len(question_pool)),
            )
            used_questions.update(selected_indices)
            self.challenge_questions = [
                question_pool[index] for index in selected_indices
            ]
            self.challenge_question_index = 0
            self.active_challenge = self.challenge_questions[0]
            self.questions_asked += len(self.challenge_questions)
            self.stage_questions_asked += len(self.challenge_questions)
            self.challenge_feedback = ""
            self.challenge_answered = False
            self.challenge_open = True
            self.save_profile_progress()

    def open_random_code_checkpoint(self):
        """Pause once in this world and ask a short game-code question."""
        if self.code_checkpoint_done:
            return

        self.code_checkpoint_done = True
        question_pool = PYTHON_CODE_CHALLENGES[self.stage_number]
        challenge = dict(random.choice(question_pool))
        choices = challenge["choices"][:]
        correct_choice = choices[challenge["answer"] - 1]
        random.shuffle(choices)
        challenge["choices"] = choices
        challenge["answer"] = choices.index(correct_choice) + 1
        self.active_code_challenge = challenge
        self.code_challenge_open = True
        self.code_challenge_answered = False
        self.code_challenge_feedback = ""
        self.questions_asked += 1
        self.stage_questions_asked += 1
        self.save_profile_progress()

    def answer_code_challenge(self, choice_number):
        """Give a hint on a wrong choice and reward a correct answer."""
        challenge = self.active_code_challenge
        if challenge is None or self.code_challenge_answered:
            return

        if choice_number == challenge["answer"]:
            self.code_challenge_answered = True
            self.questions_correct += 1
            self.stage_questions_correct += 1
            topic = challenge["topic"].title()
            self.learning_concepts.add(topic)
            self.stage_learning_concepts.add(topic)
            self.add_score(SCORE_CORRECT_ANSWER)
            self.sounds.play_powerup()
        else:
            self.code_challenge_feedback = f"Hint: {challenge['hint']}"
            self.save_profile_progress()

    def answer_python_challenge(self, choice_number):
        challenge = self.active_challenge
        if challenge is None:
            return

        if choice_number == challenge["answer"]:
            self.challenge_answered = True
            self.questions_correct += 1
            self.stage_questions_correct += 1
            self.learning_concepts.add(challenge["topic"].title())
            self.stage_learning_concepts.add(challenge["topic"].title())
            self.add_score(SCORE_CORRECT_ANSWER)
            self.sounds.play_powerup()
        else:
            self.challenge_feedback = f"Wrong answer! {challenge['hint']}"
            self.save_profile_progress()

    def return_home(self):
        """End this run and return to the name-entry home screen."""
        self.reset_stage()
        self.started = False
        self.show_world_map = False
        self.profile_name_input = self.profile_name
        self.profile_preview = self.profile_data
        pygame.key.start_text_input()

    def handle_pause_choice(self):
        """Apply the selected Home or Resume option."""
        if self.pause_selection == 0:
            self.return_home()
        else:
            self.paused = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif (
                self.paused
                and event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
            ):
                for index, button in enumerate(self.ui.pause_button_rects(self.screen)):
                    if button.collidepoint(event.pos):
                        self.pause_selection = index
                        self.handle_pause_choice()
                        break
            elif (
                event.type == pygame.TEXTINPUT
                and not self.started
                and not self.show_world_map
            ):
                self.profile_name_input = (
                    self.profile_name_input + event.text
                )[:18]
                self.profile_preview = load_player_profile(
                    self.profile_name_input.strip()
                )
            elif event.type == pygame.KEYDOWN:
                if self.code_challenge_open:
                    if self.code_challenge_answered:
                        if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                            self.code_challenge_open = False
                            self.code_challenge_answered = False
                            self.code_challenge_feedback = ""
                            self.active_code_challenge = None
                    elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                        self.answer_code_challenge(event.key - pygame.K_0)
                    continue

                if self.paused:
                    if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_w, pygame.K_s):
                        self.pause_selection = 1 - self.pause_selection
                    elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        self.handle_pause_choice()
                    elif event.key in (pygame.K_p, pygame.K_ESCAPE):
                        self.paused = False
                    continue

                if self.stage_summary_open:
                    if event.key == pygame.K_RETURN:
                        self.continue_after_stage_summary()
                    continue

                if self.challenge_open and self.challenge_answered:
                    if event.key == pygame.K_RETURN:
                        self.challenge_answered = False
                        self.challenge_feedback = ""
                        self.challenge_question_index += 1

                        if self.challenge_question_index < len(self.challenge_questions):
                            self.active_challenge = self.challenge_questions[
                                self.challenge_question_index
                            ]
                        else:
                            self.challenge_open = False
                            self.challenge_solved = True
                            self.active_challenge = None
                            self.check_stage_exit()
                    continue

                if not self.started and not self.show_world_map:
                    if event.key == pygame.K_F11:
                        pygame.display.toggle_fullscreen()
                    elif event.key == pygame.K_BACKSPACE:
                        self.profile_name_input = self.profile_name_input[:-1]
                        self.profile_preview = load_player_profile(
                            self.profile_name_input.strip()
                        )
                    elif event.key == pygame.K_RETURN:
                        name = " ".join(self.profile_name_input.strip().split())
                        if name:
                            self.profile_name = name
                            self.profile_data = load_player_profile(name)
                            self.profile_preview = self.profile_data
                            self.best_score = self.profile_data["best_score"]
                            self.reset_stage()
                            self.show_world_map = True
                            pygame.key.stop_text_input()
                    continue

                if event.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()
                elif event.key == pygame.K_RETURN:
                    if self.show_world_map:
                        self.show_world_map = False
                        self.started = True
                        self.stage_intro_timer = 1.8
                        self.show_python_tip("strings")
                elif event.key == pygame.K_n and self.show_world_map:
                    self.show_world_map = False
                    self.profile_name = ""
                    self.profile_name_input = ""
                    self.profile_data = load_player_profile("")
                    self.profile_preview = self.profile_data
                    pygame.key.start_text_input()
                elif event.key == pygame.K_ESCAPE and self.show_world_map:
                    self.show_world_map = False
                elif (
                    event.key == pygame.K_p
                    and self.started
                    and not self.game_over
                    and not self.game_won
                    and not self.challenge_open
                    and not self.code_challenge_open
                    and not self.stage_summary_open
                ):
                    self.paused = not self.paused
                elif event.key == pygame.K_m and self.started:
                    self.sounds.toggle_mute()
                elif event.key == pygame.K_t and self.started:
                    self.python_coach_enabled = not self.python_coach_enabled
                    if self.python_coach_enabled:
                        self.show_python_tip("strings")
                    else:
                        self.python_tip = None
                        self.python_tip_timer = 0.0
                elif (
                    event.key == pygame.K_f
                    and self.started
                    and not self.paused
                    and not self.game_over
                    and not self.game_won
                    and self.bullet_power_timer > 0
                    and self.shot_cooldown <= 0
                ):
                    direction = 1 if self.player.facing_right else -1
                    shot_x = (
                        self.player.rect.right
                        if direction > 0
                        else self.player.rect.left - 18
                    )
                    self.player_shots.append(
                        PlayerShot(shot_x, self.player.rect.centery, direction)
                    )
                    self.sounds.play_shoot()
                    self.shot_cooldown = SHOT_COOLDOWN_SECONDS
                elif event.key == pygame.K_e and self.started:
                    self.open_python_challenge()
                elif self.challenge_open and event.key in (
                    pygame.K_1,
                    pygame.K_2,
                    pygame.K_3,
                ):
                    choice_number = event.key - pygame.K_0
                    self.answer_python_challenge(choice_number)
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
            self.save_profile_progress()

    def check_stage_exit(self):
        all_coins_collected = all(
            coin.collected for coin in self.stage["coins"]
        )
        boss_alive = any(
            getattr(enemy, "is_boss", False)
            for enemy in self.stage["enemies"]
        )
        reached_exit = self.player.rect.right >= EXIT_REACHED_X

        self.exit_locked = reached_exit and (
            not all_coins_collected
            or boss_alive
            or not self.challenge_solved
        )

        if (
            not reached_exit
            or not all_coins_collected
            or boss_alive
            or not self.challenge_solved
            or self.stage_summary_open
        ):
            return

        self.add_score(SCORE_WORLD_CLEAR)
        if self.stage_number == TOTAL_STAGES:
            self.add_score(SCORE_GAME_COMPLETE)
        self.worlds_cleared += 1
        self.stage_points = self.score - self.stage_start_score
        self.stage_summary_open = True
        self.save_profile_progress()

    def continue_after_stage_summary(self):
        """Load the next world after the player has read the score card."""
        self.stage_summary_open = False

        if self.stage_number >= TOTAL_STAGES:
            self.game_won = True
            return

        stage_builders = (
            build_stage_one,
            build_stage_two,
            build_stage_three,
            build_stage_four,
            build_stage_five,
            build_stage_six,
            build_stage_seven,
            build_stage_eight,
            build_stage_nine,
            build_stage_ten,
        )
        self.stage_number += 1
        self.stage = stage_builders[self.stage_number - 1]()
        # Each new world starts with its own full set of lives.
        self.player_lives = MAX_LIVES

        self.stage_intro_timer = 1.8
        self.prepare_background()
        self.player = Player(*PLAYER_START_POSITION)
        self.respawn_position = PLAYER_START_POSITION
        self.checkpoint_message_timer = 0.0
        self.bullets.clear()
        self.player_shots.clear()
        self.cheese_drops.clear()
        self.bullet_power_timer = 0.0
        self.shot_cooldown = 0.0
        self.hit_cooldown = 0
        self.stomp_effect_timer = 0
        self.camera_shake_timer = 0
        self.particles = ParticleSystem()
        self.exit_locked = False
        self.challenge_open = False
        self.challenge_solved = False
        self.challenge_answered = False
        self.challenge_feedback = ""
        self.active_challenge = None
        self.reset_code_checkpoint()
        self.challenge_questions = []
        self.challenge_question_index = 0
        self.stage_questions_asked = 0
        self.stage_questions_correct = 0
        self.stage_learning_concepts = set()
        self.stage_start_score = self.score
        self.show_python_tip("dictionaries")
        self.camera_x = 0

    def update(self, dt=1 / FPS):
        if (
            not self.started
            or self.game_over
            or self.game_won
            or self.paused
            or self.challenge_open
            or self.code_challenge_open
            or self.stage_summary_open
        ):
            return

        self.stage_intro_timer = max(0.0, self.stage_intro_timer - dt)
        self.bullet_power_timer = max(0.0, self.bullet_power_timer - dt)
        self.shot_cooldown = max(0.0, self.shot_cooldown - dt)
        self.checkpoint_message_timer = max(
            0.0, self.checkpoint_message_timer - dt
        )
        self.python_tip_timer = max(0.0, self.python_tip_timer - dt)
        if self.python_tip_timer == 0:
            self.python_tip = None

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
        moving_platforms = self.stage.get("moving_platforms", [])

        # Lift par khade player ko lift ke saath le jao.
        for platform in moving_platforms:
            standing_on_lift = (
                self.player.rect.bottom == platform.rect.top
                and self.player.rect.right > platform.rect.left
                and self.player.rect.left < platform.rect.right
            )

            old_y = platform.rect.y
            platform.update()

            if standing_on_lift:
                self.player.rect.y += platform.rect.y - old_y

        all_platforms = self.stage["platforms"] + moving_platforms
        self.player.update(keys, all_platforms)
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
            self.player.rect.centerx >= CHECKPOINT_X
            and self.respawn_position == PLAYER_START_POSITION
        ):
            self.respawn_position = (
                CHECKPOINT_X - 40,
                490 - self.player.rect.height,
            )
            self.checkpoint_message_timer = 1.8
            self.add_score(SCORE_CHECKPOINT)
            self.particles.burst(CHECKPOINT_X, 350, (115, 255, 160), 22, 150)
            self.sounds.play_checkpoint()
            self.show_python_tip("tuples")

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
                        self.add_score(SCORE_BOSS_STOMP)
                        self.show_python_tip("inheritance")
                        enemy.health -= 1
                        if enemy.health <= 0:
                            self.add_score(SCORE_BOSS_DEFEAT)
                            self.drop_cheese(enemy)
                            self.stage["enemies"].remove(enemy)
                    else:
                        self.add_score(SCORE_ENEMY_STOMP)
                        self.show_python_tip("classes")
                        self.drop_cheese(enemy)
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
            if bullet.rect.right > 0 and bullet.rect.left < WORLD_WIDTH
        ]

        for shot in self.player_shots[:]:
            shot.update()
            hit_enemy = None

            for enemy in self.stage["enemies"][:]:
                if shot.rect.colliderect(enemy.rect):
                    hit_enemy = enemy
                    break

            if hit_enemy is not None:
                self.player_shots.remove(shot)

                if getattr(hit_enemy, "is_boss", False):
                    hit_enemy.health -= 1
                    self.add_score(SCORE_BOSS_HIT)
                    if hit_enemy.health <= 0:
                        self.add_score(SCORE_BOSS_DEFEAT)
                        self.drop_cheese(hit_enemy)
                        self.stage["enemies"].remove(hit_enemy)
                else:
                    self.add_score(SCORE_ENEMY_SHOT)
                    self.drop_cheese(hit_enemy)
                    self.stage["enemies"].remove(hit_enemy)

            elif shot.rect.right < 0 or shot.rect.left > WORLD_WIDTH:
                self.player_shots.remove(shot)

        for drop in self.cheese_drops[:]:
            drop.update()

            if self.player.rect.colliderect(drop.rect):
                self.cheese_drops.remove(drop)
                self.add_score(SCORE_CHEESE)
                continue

            if drop.lifetime <= 0:
                self.cheese_drops.remove(drop)

        for coin in self.stage["coins"]:
            if not coin.collected and self.player.rect.colliderect(coin.rect):
                coin.collected = True
                self.show_python_tip("lists")
                self.add_score(SCORE_COIN)
                self.sounds.play_coin()
                self.particles.burst(*coin.rect.center, (255, 220, 85), 14, 165)

        for powerup in self.stage.get("powerups", []):
            if not powerup.collected and self.player.rect.colliderect(powerup.rect):
                powerup.collected = True
                self.show_python_tip("conditionals")
                if powerup.kind == "bullet":
                    self.bullet_power_timer = FIRE_POWER_SECONDS
                else:
                    self.player.speed_boost_timer = SPEED_BOOST_FRAMES
                self.add_score(SCORE_POWERUP)
                self.sounds.play_powerup()
                self.particles.burst(
                    *powerup.rect.center, (120, 235, 255), 20, 185
                )

        if (
            not self.code_checkpoint_done
            and not self.game_over
            and self.player.rect.centerx >= self.code_checkpoint_x
        ):
            self.open_random_code_checkpoint()

        self.check_stage_exit()

        self.camera_x = max(
            0,
            min(
                self.player.rect.centerx - SCREEN_WIDTH // 2,
                WORLD_WIDTH - SCREEN_WIDTH,
            ),
        )

    def draw_exit_gate(self, world, locked=True):
        pole_x = WORLD_WIDTH - 70
        # Gate pole and base
        pygame.draw.rect(world, (90, 70, 55), (pole_x, 405, 8, 85))
        pygame.draw.rect(world, (145, 115, 80), (pole_x - 3, 480, 14, 10))
        pygame.draw.circle(world, (255, 220, 120), (pole_x + 4, 402), 5)

        # Gently waving flag
        wave = (pygame.time.get_ticks() // 250) % 2
        tip_x = WORLD_WIDTH - (20 if wave == 0 else 27)
        middle_y = 421 if wave == 0 else 424

        flag_color = (155, 165, 185) if locked else (245, 190, 65)
        pygame.draw.polygon(
            world,
            flag_color,
            [(pole_x + 8, 405), (tip_x, middle_y), (pole_x + 8, 438)],
        )
        pygame.draw.line(
            world,
            (215, 220, 235) if locked else (255, 230, 145),
            (pole_x + 11, 411),
            (tip_x - 8, middle_y),
            2,
        )
        if locked:
            pygame.draw.arc(
                world, (220, 220, 230), (pole_x + 12, 447, 12, 13),
                math.pi, 2 * math.pi, 2,
            )
            pygame.draw.rect(
                world, (220, 220, 230), (pole_x + 11, 453, 14, 11),
                border_radius=2,
            )
        else:
            pulse = (math.sin(pygame.time.get_ticks() / 160) + 1) / 2
            pygame.draw.circle(
                world, (255, 225, 125, 90 + round(pulse * 90)),
                (pole_x + 8, 421), 18 + round(pulse * 3), 2,
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

        elif self.stage_number == 5:
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

        elif self.stage_number == 6:
            # Ember Dunes: layered orange dunes and desert cacti.
            pygame.draw.circle(world, (255, 220, 135), (1320, 150), 54)
            pygame.draw.ellipse(world, (205, 125, 90), (-160, 350, 750, 220))
            pygame.draw.ellipse(world, (220, 145, 95), (380, 370, 780, 220))
            pygame.draw.ellipse(world, (190, 105, 85), (980, 345, 800, 240))
            for x, y in ((250, 405), (740, 420), (1250, 400)):
                pygame.draw.rect(world, (55, 125, 90), (x, y, 14, 80), border_radius=7)
                pygame.draw.rect(world, (55, 125, 90), (x - 17, y + 20, 18, 12), border_radius=6)
                pygame.draw.rect(world, (55, 125, 90), (x + 12, y + 38, 18, 12), border_radius=6)

        elif self.stage_number == 7:
            # Coral Reef: ocean floor, sea plants, and distant coral.
            pygame.draw.ellipse(world, (40, 135, 165), (-120, 385, 800, 200))
            pygame.draw.ellipse(world, (35, 115, 155), (650, 390, 900, 190))
            for x, y, color in ((170, 470, (255, 115, 155)), (500, 465, (245, 165, 95)), (980, 470, (225, 110, 190)), (1430, 465, (255, 145, 125))):
                pygame.draw.line(world, color, (x, y), (x, y - 48), 7)
                pygame.draw.line(world, color, (x, y - 25), (x - 20, y - 42), 6)
                pygame.draw.line(world, color, (x, y - 32), (x + 18, y - 50), 6)
            for x, y in ((280, 180), (690, 255), (1170, 145), (1500, 280)):
                pygame.draw.circle(world, (135, 230, 245), (x, y), 8, 2)

        elif self.stage_number == 8:
            # Clockwork Factory: chimneys, windows, and gear-like wheels.
            for x, y, width, height in ((180, 285, 180, 205), (410, 235, 230, 255), (710, 310, 190, 180), (1010, 260, 240, 230)):
                pygame.draw.rect(world, (65, 80, 105), (x, y, width, height))
            for x, top in ((220, 200), (490, 150), (790, 235), (1080, 175)):
                pygame.draw.rect(world, (80, 95, 120), (x, top, 48, 490 - top))
                pygame.draw.rect(world, (105, 120, 145), (x - 6, top - 12, 60, 14))
            for x, y in ((320, 390), (570, 390), (820, 400), (1160, 390)):
                pygame.draw.circle(world, (225, 180, 90), (x, y), 27, 5)
                pygame.draw.circle(world, (225, 180, 90), (x, y), 7)
            for x, y in ((455, 290), (525, 290), (1080, 315), (1150, 315)):
                pygame.draw.rect(world, (255, 215, 120), (x, y, 22, 32), border_radius=4)

        elif self.stage_number == 9:
            # Cloud Kingdom: floating islands and soft cloud banks.
            for x, y, width in ((40, 335, 360), (520, 385, 420), (1100, 340, 430)):
                pygame.draw.ellipse(world, (225, 245, 255), (x, y, width, 90))
                pygame.draw.ellipse(world, (205, 232, 250), (x + width // 3, y - 28, width // 2, 90))
            for x, y in ((300, 250), (790, 220), (1280, 255)):
                pygame.draw.ellipse(world, (105, 150, 190), (x, y, 180, 32))
                pygame.draw.polygon(world, (95, 135, 180), ((x + 25, y + 18), (x + 155, y + 18), (x + 110, y + 88), (x + 70, y + 88)))
                pygame.draw.ellipse(world, (100, 185, 125), (x + 16, y - 9, 148, 20))

        else:
            # Python Core: a glowing final gate surrounded by code-like runes.
            for index in range(18):
                x = 70 + index * 88
                y = 85 + (index * 53) % 190
                color = (120, 175, 235) if index % 2 else (185, 135, 245)
                pygame.draw.line(world, color, (x, y), (x + 24, y), 3)
                pygame.draw.line(world, color, (x + 12, y - 8), (x + 12, y + 8), 2)
            pygame.draw.circle(world, (255, 210, 105), (1260, 230), 100, 5)
            pygame.draw.circle(world, (130, 210, 255), (1260, 230), 74, 3)
            pygame.draw.rect(world, (85, 70, 145), (1210, 330, 100, 160))
            pygame.draw.polygon(world, (115, 95, 180), ((1190, 330), (1330, 330), (1260, 265)))

    def prepare_background(self):
        """Cache the detailed scenery so it scrolls behind the gameplay layer."""
        self.background_surface = pygame.Surface((WORLD_WIDTH, SCREEN_HEIGHT))
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

        elif self.stage_number in (2, 5, 10):
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

        elif self.stage_number in (7, 9):
            for index in range(12):
                x = (index * 89 + int(time * 18)) % SCREEN_WIDTH
                y = 120 + (index * 37) % 300
                pygame.draw.circle(surface, (155, 235, 245), (x, y), 3 + index % 3, 1)

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

            for platform in self.stage.get("moving_platforms", []):
                platform.draw(world)

            for hazard in self.stage.get("hazards", []):
                hazard.draw(world)

            # Gray checkpoint becomes green after activation.
            flag_color = (
                (65, 210, 130)
                if self.respawn_position != PLAYER_START_POSITION
                else (185, 185, 195)
            )

            pygame.draw.rect(
                world, (90, 70, 55), (CHECKPOINT_X - 4, 350, 6, 55)
            )
            pygame.draw.polygon(
                world,
                flag_color,
                [
                    (CHECKPOINT_X + 2, 351),
                    (CHECKPOINT_X + 36, 361),
                    (CHECKPOINT_X + 2, 373),
                ],
            )
            pygame.draw.circle(
                world, (255, 245, 190), (CHECKPOINT_X - 1, 348), 4
            )

            for coin in self.stage["coins"]:
                coin.draw(world)

            for drop in self.cheese_drops:
                drop.draw(world)

            for powerup in self.stage.get("powerups", []):
                powerup.draw(world)

            for enemy in self.stage["enemies"]:
                enemy.draw(world)

            if self.stage_intro_timer > 0 and not self.python_tip:
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

            for shot in self.player_shots:
                shot.draw(world)

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
                progress=self.player.rect.centerx / WORLD_WIDTH,
                stage_number=self.stage_number,
                sound_muted=self.sounds.muted,
                score=self.score,
                bullet_timer=self.bullet_power_timer,
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
                elif coins_missing:
                    message_text = "Collect all coins to unlock the exit!"
                else:
                    message_text = "Press E at the flag for the Python challenge!"

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
            if (
                self.started
                and self.python_tip
                and self.python_tip_timer > 0
                and not self.game_over
                and not self.game_won
                and not self.paused
            ):
                self.ui.draw_python_tip(
                    self.screen,
                    self.python_tip,
                    self.python_tip_timer,
                )

        if not self.started:
            if self.show_world_map:
                self.ui.draw_world_map(
                    self.screen, self.profile_name, self.profile_data
                )
            else:
                preview_name = self.profile_name_input.strip()
                self.ui.draw_start(
                    self.screen,
                    preview_name,
                    self.profile_preview,
                )
        elif self.game_over:
            self.ui.draw_game_over(
                self.screen,
                self.score,
                self.best_score,
                self.worlds_cleared,
                self.questions_correct,
                self.questions_asked,
                sorted(self.learning_concepts),
            )
        elif self.game_won:
            self.ui.draw_win(
                self.screen,
                self.score,
                self.best_score,
                self.worlds_cleared,
                self.questions_correct,
                self.questions_asked,
                sorted(self.learning_concepts),
            )
        elif self.stage_summary_open:
            self.ui.draw_stage_summary(
                self.screen,
                self.stage_number,
                self.stage["info"]["name"],
                self.stage_points,
                self.score,
                self.stage_questions_correct,
                self.stage_questions_asked,
                sorted(self.stage_learning_concepts),
                is_final=self.stage_number == TOTAL_STAGES,
            )
        elif self.paused:
            self.ui.draw_pause(
                self.screen,
                selected_index=self.pause_selection,
                mouse_pos=pygame.mouse.get_pos(),
            )


        if self.challenge_open and self.active_challenge is not None:
            self.ui.draw_python_challenge(
                self.screen,
                self.active_challenge,
                self.challenge_feedback,
                answered=self.challenge_answered,
                question_number=self.challenge_question_index + 1,
                question_total=len(self.challenge_questions),
            )
        if self.code_challenge_open and self.active_code_challenge is not None:
            self.ui.draw_code_checkpoint(
                self.screen,
                self.active_code_challenge,
                feedback=self.code_challenge_feedback,
                answered=self.code_challenge_answered,
            )
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            dt = min(self.clock.tick(FPS) / 1000.0, 0.05)
            self.update(dt)
            self.draw()

        pygame.quit()
