"""Platforms, collectibles, power-ups, and themed floor hazards."""

import math

import pygame

from settings import COIN_COLOR, DIRT, GRASS


class Platform:
    def __init__(self, x, y, width, height=24):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, surface):
        pygame.draw.rect(surface, (83, 50, 38), self.rect, border_radius=4)
        pygame.draw.rect(
            surface, DIRT,
            (self.rect.x, self.rect.y + 5, self.rect.width, self.rect.height - 5),
            border_radius=3,
        )

        # Small marks on the dirt
        for x in range(self.rect.left + 8, self.rect.right - 4, 28):
            y = self.rect.top + 16 + ((x // 28) % 2) * 7
            pygame.draw.circle(surface, (115, 75, 48), (x, y), 2)

        # Grass strip and blades
        pygame.draw.rect(
            surface, GRASS,
            (self.rect.x, self.rect.y, self.rect.width, 8),
            border_radius=3,
        )
        pygame.draw.line(
            surface, (145, 225, 125),
            (self.rect.left + 4, self.rect.top + 1),
            (self.rect.right - 4, self.rect.top + 1), 2,
        )
        for x in range(self.rect.left + 9, self.rect.right - 5, 28):
            blade_y = self.rect.y + 7 + int(math.sin(pygame.time.get_ticks() / 500 + x) * 1.5)
            pygame.draw.line(surface, (95, 205, 105), (x, blade_y), (x + 3, blade_y - 5), 1)


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
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 24, 24)
        self.collected = False

    def draw(self, surface):
        if not self.collected:
            time = pygame.time.get_ticks() / 1000
            bob = round(math.sin(time * 3.5 + self.rect.x) * 4)
            center = (self.rect.centerx, self.rect.centery + bob)
            radius = 14 + round((math.sin(time * 4) + 1) * 1.5)
            pygame.draw.circle(surface, (255, 240, 115), center, radius + 6, 2)
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
