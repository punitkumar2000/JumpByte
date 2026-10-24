"""The player character, movement, jumping, and platform collisions."""

import math

import pygame
from sprites import draw_frame, load_frames

from settings import (
    GRAVITY,
    JUMP_SPEED,
    PLAYER_COLOR,
    PLAYER_SPEED,
    SCREEN_HEIGHT,
)


class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 34, 46)
        self.velocity_y = 0
        self.on_ground = False
        self.speed_boost_timer = 0
        self.is_moving = False
        self.facing_right = True

    def update(self, keys, platforms):
        # Save the old position so we can tell which side hit a platform.
        previous_rect = self.rect.copy()

        if self.speed_boost_timer > 0:
            self.speed_boost_timer -= 1

        move_speed = PLAYER_SPEED * 2 if self.speed_boost_timer > 0 else PLAYER_SPEED
        # Move left or right.
        move_x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            move_x -= move_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            move_x += move_speed

        if move_x:
            self.facing_right = move_x > 0

        self.rect.x += move_x

        # Stop the player at the sides of platforms.
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if move_x > 0:
                    self.rect.right = platform.rect.left
                elif move_x < 0:
                    self.rect.left = platform.rect.right
        self.is_moving = move_x != 0 and self.rect.x != previous_rect.x
        # Keep the player inside the level.
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(1600, self.rect.right)

        # Jump only when standing on a platform.
        jump_pressed = (
            keys[pygame.K_SPACE]
            or keys[pygame.K_UP]
            or keys[pygame.K_w]
        )
        if jump_pressed and self.on_ground:
            self.velocity_y = JUMP_SPEED
            self.on_ground = False

        # Apply gravity and move vertically.
        self.velocity_y += GRAVITY
        move_y = int(self.velocity_y)
        self.rect.y += move_y
        self.on_ground = False

        # Land on platforms, or bump the underside when jumping.
        for platform in platforms:
            if not self.rect.colliderect(platform.rect):
                continue

            if move_y >= 0 and previous_rect.bottom <= platform.rect.top:
                self.rect.bottom = platform.rect.top
                self.velocity_y = 0
                self.on_ground = True
            elif move_y < 0 and previous_rect.top >= platform.rect.bottom:
                self.rect.top = platform.rect.bottom
                self.velocity_y = 0

        # Gravity is fractional, so int(0.5) is zero every other frame.
        # Check for a platform directly under the feet as well as overlap;
        # this keeps on_ground stable while standing still.
        if move_y >= 0:
            for platform in platforms:
                supported = (
                    self.rect.bottom == platform.rect.top
                    and self.rect.right > platform.rect.left
                    and self.rect.left < platform.rect.right
                )
                if supported:
                    self.velocity_y = 0
                    self.on_ground = True
                    break

        # If the player falls off the level, return them to the start.
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.topleft = (60, 400)
            self.velocity_y = 0
            self.on_ground = False

    def draw(self, surface, hit_cooldown=0):
        if not self.on_ground:
            animation = "jump"
            frame_index = 2
        elif self.is_moving:
            animation = "run"
            # Slower frame changes plus a shared frame pivot prevent the
            # generated poses from looking like they are vibrating.
            frame_index = (pygame.time.get_ticks() // 165) % 4
        else:
            animation = "idle"
            frame_index = 0

        frame = load_frames("rat", animation)[frame_index]

        if hit_cooldown > 0:
            flash = (math.sin(pygame.time.get_ticks() / 55) + 1) / 2
            hurt_glow = pygame.Rect(0, 0, 74, 70)
            hurt_glow.midbottom = self.rect.midbottom
            pygame.draw.ellipse(
                surface,
                (255, 85, 105, 85 + round(flash * 80)),
                hurt_glow,
                3,
            )

        # A pulsing cyan ring makes the temporary speed power-up visible
        # while keeping the character art itself clear.
        if self.speed_boost_timer > 0:
            pulse = (math.sin(pygame.time.get_ticks() / 90) + 1) / 2
            aura = pygame.Rect(0, 0, 70 + round(pulse * 8), 68 + round(pulse * 6))
            aura.midbottom = self.rect.midbottom
            pygame.draw.ellipse(surface, (100, 225, 255, 125), aura, 2)

        draw_frame(surface, frame, self.rect, 64, self.facing_right)
