"""Animated cat enemies, their projectiles, and the final boss."""

import math

import pygame
from sprites import draw_frame, load_frames


class Bullet:
    """A small projectile fired horizontally toward the player's current side."""

    def __init__(self, x, y, direction):
        self.rect = pygame.Rect(x, y, 12, 6)
        self.direction = direction
        self.speed = 7

    def update(self):
        self.rect.x += self.speed * self.direction

    def draw(self, surface):
        center = self.rect.center
        flicker = (math.sin(pygame.time.get_ticks() / 45) + 1) / 2
        radius = 5 + round(flicker * 2)
        tail = (center[0] - self.direction * 13, center[1])

        # Warm streak and layered glow make the small projectile readable
        # against both bright outdoor and dark cave backgrounds.
        pygame.draw.line(surface, (255, 85, 55, 95), tail, center, 7)
        pygame.draw.circle(surface, (255, 105, 55, 100), center, radius + 5)
        pygame.draw.circle(surface, (245, 75, 55), center, radius)
        pygame.draw.circle(surface, (255, 205, 115), center, max(2, radius - 2))
        pygame.draw.circle(surface, (255, 250, 220), (center[0] - 1, center[1] - 1), 2)


class Enemy:
    """Patrols between two points, jumps now and then, and fires at the player."""

    def __init__(self, x, y, left_bound, right_bound):
        self.rect = pygame.Rect(x, y, 34, 30)
        self.left_bound = left_bound
        self.right_bound = right_bound
        self.speed = 2
        self.direction = 1

        self.ground_y = y
        self.velocity_y = 0
        self.gravity = 0.5
        self.jump_speed = -10
        self.jump_timer = 0
        self.jump_delay = 120

        self.shoot_timer = 0
        self.shoot_delay = 90
        self.attack_timer = 0

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.right >= self.right_bound:
            self.rect.right = self.right_bound
            self.direction = -1
        elif self.rect.left <= self.left_bound:
            self.rect.left = self.left_bound
            self.direction = 1

        self.jump_timer += 1
        if self.jump_timer >= self.jump_delay and self.rect.y >= self.ground_y:
            self.velocity_y = self.jump_speed
            self.jump_timer = 0

        self.velocity_y += self.gravity
        self.rect.y += int(self.velocity_y)
        if self.rect.y >= self.ground_y:
            self.rect.y = self.ground_y
            self.velocity_y = 0

        self.shoot_timer += 1
        if self.attack_timer > 0:
            self.attack_timer -= 1

    def ready_to_shoot(self):
        if self.shoot_timer >= self.shoot_delay:
            self.shoot_timer = 0
            return True
        return False

    def shoot(self, player_rect):
        self.attack_timer = 24
        direction = -1 if player_rect.centerx < self.rect.centerx else 1
        bullet_x = self.rect.left if direction == -1 else self.rect.right
        return Bullet(bullet_x, self.rect.centery, direction)

    def check_collision(self, player_rect):
        return self.rect.colliderect(player_rect)

    def draw(self, surface):
        if self.attack_timer > 0:
            animation = "attack"
            frame_index = (pygame.time.get_ticks() // 90) % 4
        else:
            animation = "walk"
            frame_index = (pygame.time.get_ticks() // 130) % 4

        frame = load_frames("cat", animation)[frame_index]
        is_boss = getattr(self, "is_boss", False)
        draw_height = 92 if is_boss else 60
        draw_frame(surface, frame, self.rect, draw_height, self.direction > 0)

        if is_boss:
            # The artwork is taller than the collision box, so anchor the
            # boss health display above the rendered sprite, not its hitbox.
            bar_width = 96
            bar_height = 8
            bar_x = self.rect.centerx - bar_width // 2
            bar_y = self.rect.bottom - draw_height - 23
            pygame.draw.rect(
                surface, (28, 24, 38),
                (bar_x - 2, bar_y - 2, bar_width + 4, bar_height + 4),
                border_radius=5,
            )
            pygame.draw.rect(
                surface, (110, 48, 65),
                (bar_x, bar_y, bar_width, bar_height),
                border_radius=4,
            )
            health_width = round(bar_width * self.health / self.max_health)
            if health_width:
                pygame.draw.rect(
                    surface, (255, 105, 120),
                    (bar_x, bar_y, health_width, bar_height),
                    border_radius=4,
                )
            if not hasattr(self, "_boss_label_font"):
                self._boss_label_font = pygame.font.Font(None, 18)
            label = self._boss_label_font.render(
                "CAT BOSS", True, (255, 240, 220)
            )
            surface.blit(label, label.get_rect(midbottom=(self.rect.centerx, bar_y - 4)))

class Boss(Enemy):
    """A larger cat enemy with health, based on the regular Enemy class."""

    def __init__(self, x, y, left_bound, right_bound):
        super().__init__(x, y, left_bound, right_bound)

        self.rect = pygame.Rect(x, y, 64, 48)
        self.ground_y = y
        self.speed = 1
        self.jump_delay = 90
        self.shoot_delay = 110

        self.max_health = 3
        self.health = self.max_health
        self.is_boss = True

    def update(self):
        if self.health == 1:
            self.speed = 2
            self.shoot_delay = 75
            self.jump_delay = 75

        super().update()

    def draw(self, surface):
        super().draw(surface)
