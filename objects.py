"""Platforms, collectibles, power-ups, and themed floor hazards."""

import math

import pygame

from settings import COIN_COLOR, DIRT, GRASS, PLAYER_SHOT_SPEED


class Platform:
    def __init__(self, x, y, width, height=24):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, surface, theme=None):
        """Draw a softly shaded platform using the current world's colors."""
        theme = theme or {}
        top_color = theme.get("top", GRASS)
        highlight = theme.get("highlight", (145, 225, 125))
        soil_color = theme.get("soil", DIRT)
        shadow_color = theme.get("shadow", (83, 50, 38))
        detail_color = theme.get("detail", (115, 75, 48))

        pygame.draw.ellipse(
            surface, (18, 22, 34, 55),
            (self.rect.x + 3, self.rect.bottom - 3, max(1, self.rect.width - 6), 9),
        )
        pygame.draw.rect(surface, shadow_color, self.rect, border_radius=7)
        pygame.draw.rect(
            surface,
            soil_color,
            (
                self.rect.x + 1,
                self.rect.y + 6,
                max(1, self.rect.width - 2),
                max(1, self.rect.height - 7),
            ),
            border_radius=6,
        )

        # Small pebble marks give the front face a little texture.
        for x in range(self.rect.left + 12, self.rect.right - 5, 32):
            y = self.rect.top + 15 + ((x // 32) % 2) * 5
            pygame.draw.ellipse(surface, detail_color, (x, y, 6, 3))

        pygame.draw.rect(
            surface,
            top_color,
            (self.rect.x, self.rect.y, self.rect.width, min(11, self.rect.height)),
            border_radius=6,
        )
        pygame.draw.line(
            surface,
            highlight,
            (self.rect.left + 6, self.rect.top + 2),
            (self.rect.right - 6, self.rect.top + 2),
            2,
        )
        for x in range(self.rect.left + 13, self.rect.right - 7, 38):
            sway = int(math.sin(pygame.time.get_ticks() / 650 + x) * 1.2)
            pygame.draw.line(
                surface, highlight,
                (x, self.rect.top + 8), (x + 3, self.rect.top + 4 + sway), 1,
            )


class Coin:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 18, 18)
        self.collected = False

    def draw(self, surface):
        if not self.collected:
            time = pygame.time.get_ticks() / 1000
            pulse = 1 + math.sin(time * 5 + self.rect.x * 0.03) * 1.5
            bob = round(math.sin(time * 3.2 + self.rect.x * 0.02) * 3)
            center = (self.rect.centerx, self.rect.centery + bob)
            radius = round(9 + pulse)

            pygame.draw.circle(surface, (255, 238, 130), center, radius + 4, 1)
            pygame.draw.circle(surface, COIN_COLOR, center, radius)
            pygame.draw.circle(surface, (255, 242, 170), (center[0] - 2, center[1] - 3), 3)
            pygame.draw.circle(
                surface,
                (235, 160, 40),
                (center[0] + 3, center[1] + 2),
                2,
            )
class PowerUp:
    def __init__(self, x, y, kind="speed"):
        self.rect = pygame.Rect(x, y, 24, 24)
        self.collected = False
        self.kind = kind

    def draw(self, surface):
        if self.collected:
            return

        time = pygame.time.get_ticks() / 1000
        bob = round(math.sin(time * 3.5 + self.rect.x) * 4)
        center = (self.rect.centerx, self.rect.centery + bob)
        radius = 14 + round((math.sin(time * 4) + 1) * 1.5)

        if self.kind == "bullet":
            pygame.draw.circle(
                surface, (100, 205, 255), center, radius + 6, 2
            )
            pygame.draw.circle(surface, (65, 155, 235), center, radius)
            pygame.draw.circle(
                surface, (240, 250, 255), center, 5
            )
            return

        pygame.draw.circle(
            surface, (255, 240, 115), center, radius + 6, 2
        )
        pygame.draw.circle(surface, (250, 210, 55), center, radius)
        pygame.draw.polygon(
            surface,
            (85, 65, 35),
            [
                (center[0] + 3, center[1] - 10),
                (center[0] - 4, center[1] + 1),
                (center[0] + 1, center[1] + 1),
                (center[0] - 2, center[1] + 10),
                (center[0] + 6, center[1] - 2),
                (center[0] + 1, center[1] - 2),
            ],
        )


class Hazard:
    """A small themed floor trap the player must jump over."""

    def __init__(self, x, floor_y, width=58, color=(220, 90, 85)):
        self.rect = pygame.Rect(x, floor_y - 20, width, 20)
        self.color = color

    def draw(self, surface):
        # A dim base shadow and three sharp points make the danger readable.
        pygame.draw.ellipse(
            surface, (25, 28, 40, 85),
            (self.rect.x - 3, self.rect.bottom - 4, self.rect.width + 6, 9),
        )
        spike_count = max(2, self.rect.width // 18)
        for index in range(spike_count):
            left = self.rect.left + index * self.rect.width // spike_count
            right = self.rect.left + (index + 1) * self.rect.width // spike_count
            tip_x = (left + right) // 2
            pygame.draw.polygon(
                surface,
                self.color,
                [(left, self.rect.bottom), (tip_x, self.rect.top), (right, self.rect.bottom)],
            )
            pygame.draw.line(
                surface,
                (255, 225, 205),
                (tip_x, self.rect.top + 2),
                (tip_x - 3, self.rect.top + 9),
                1,
            )
class MovingPlatform:
    """Moves vertically between two points and carries the player."""

    def __init__(self, x, y, width, height, top_y, bottom_y, speed=1):
        self.rect = pygame.Rect(x, y, width, height)
        self.top_y = top_y
        self.bottom_y = bottom_y
        self.speed = speed
        self.direction = 1
        self.previous_y = y

    def update(self):
        self.previous_y = self.rect.y
        self.rect.y += self.speed * self.direction

        if self.rect.top <= self.top_y:
            self.rect.top = self.top_y
            self.direction = 1
        elif self.rect.bottom >= self.bottom_y:
            self.rect.bottom = self.bottom_y
            self.direction = -1

    def draw(self, surface, theme=None):
        theme = theme or {}
        moving_color = theme.get("moving", (95, 190, 210))
        highlight = theme.get("highlight", (205, 245, 245))
        accent = theme.get("accent", (120, 220, 235))
        pygame.draw.rect(surface, (28, 35, 56), self.rect.inflate(4, 4), border_radius=9)
        pygame.draw.rect(surface, moving_color, self.rect, border_radius=8)
        pygame.draw.rect(
            surface, highlight,
            (self.rect.x, self.rect.y, self.rect.width, 6),
            border_radius=4,
        )
        for x in (self.rect.left + 10, self.rect.right - 10):
            pygame.draw.circle(surface, accent, (x, self.rect.centery + 2), 3)

class CheeseDrop:
    """A small bonus pickup that bounces out when an enemy is defeated."""

    def __init__(self, x, y, direction):
        self.rect = pygame.Rect(x, y, 14, 12)
        self.velocity_x = direction * 2.5
        self.velocity_y = -4
        self.gravity = 0.3
        self.floor_y = 490
        self.lifetime = 600
        self.collected = False

    def update(self):
        self.lifetime -= 1
        self.rect.x += int(self.velocity_x)
        self.velocity_y += self.gravity
        self.rect.y += int(self.velocity_y)

        if self.rect.bottom >= self.floor_y:
            self.rect.bottom = self.floor_y
            self.velocity_y = 0
            self.velocity_x *= 0.85

    def draw(self, surface):
        if self.collected:
            return

        points = [
            (self.rect.centerx, self.rect.top),
            (self.rect.right, self.rect.centery),
            (self.rect.centerx, self.rect.bottom),
            (self.rect.left, self.rect.centery),
        ]
        pygame.draw.polygon(surface, (255, 220, 100), points)
        pygame.draw.circle(
            surface, (255, 245, 190),
            (self.rect.centerx - 2, self.rect.centery - 2), 2,
        )

class PlayerShot:
    def __init__(self, x, y, direction):
        self.rect = pygame.Rect(x, y, 18, 10)
        self.direction = direction
        self.speed = PLAYER_SHOT_SPEED

    def update(self):
        self.rect.x += self.speed * self.direction

    def draw(self, surface):
        pygame.draw.line(
            surface, (100, 205, 255),
            (self.rect.centerx - self.direction * 12, self.rect.centery),
            self.rect.center, 5,
        )
        pygame.draw.ellipse(surface, (225, 250, 255), self.rect)
