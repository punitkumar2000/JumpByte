"""Polished title, HUD, pause, win, and game-over screens."""

import pygame
import math
from pathlib import Path


WHITE = (247, 250, 255)
MINT = (133, 245, 194)
GOLD = (255, 216, 105)
INK = (26, 35, 57)


class UI:
    def __init__(self):
        self.small_font = pygame.font.Font(None, 20)
        self.font = pygame.font.Font(None, 26)
        self.title_font = pygame.font.Font(None, 76)
        self.subtitle_font = pygame.font.Font(None, 30)
        asset_dir = Path(__file__).resolve().parent / "assets"

        self.menu_background = pygame.image.load(
            str(asset_dir / "menu_background.png")
        ).convert()

        self.game_over_background = pygame.image.load(
            str(asset_dir / "game_over.png")
        ).convert()

        self.win_background = pygame.image.load(
            str(asset_dir / "win_background.png")
        ).convert()

    def _panel(self, surface, rect, color=(20, 28, 48, 205), radius=18):
        panel = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        pygame.draw.rect(panel, color, panel.get_rect(), border_radius=radius)
        pygame.draw.rect(
            panel, (255, 255, 255, 45), panel.get_rect(),
            width=1, border_radius=radius,
        )
        surface.blit(panel, rect.topleft)

    def draw_hud(
        self, surface, stage_name, coin_count, lives, boost_timer=0,
        total_coins=0, progress=0.0, stage_number=1, sound_muted=False,
        score=0,
        bullet_timer=0.0,
    ):
        self._panel(surface, pygame.Rect(16, 12, surface.get_width() - 32, 68), radius=16)

        label = self.small_font.render(f"WORLD {stage_number:02d}  /  05", True, MINT)
        name = self.font.render(stage_name, True, WHITE)
        surface.blit(label, (30, 19))
        surface.blit(name, (30, 42))
        pygame.draw.line(surface, (255, 255, 255, 55), (220, 25), (220, 67), 1)

        coin_center = (247, 42)
        pygame.draw.circle(surface, GOLD, coin_center, 11)
        pygame.draw.circle(surface, (255, 246, 190), (243, 38), 3)
        coin_text = self.font.render(f"{coin_count:02d} / {total_coins:02d}", True, WHITE)
        coin_label = self.small_font.render("COINS", True, (180, 194, 218))
        surface.blit(coin_text, (266, 29))
        surface.blit(coin_label, (266, 52))

        pygame.draw.line(surface, (255, 255, 255, 55), (355, 25), (355, 67), 1)
        lives_label = self.small_font.render("LIVES", True, (180, 194, 218))
        surface.blit(lives_label, (375, 19))
        for index in range(3):
            color = (255, 112, 132) if index < lives else (89, 97, 116)
            x = 384 + index * 24
            pygame.draw.circle(surface, color, (x - 4, 48), 6)
            pygame.draw.circle(surface, color, (x + 4, 48), 6)
            pygame.draw.polygon(
                surface, color,
                [(x - 10, 49), (x + 10, 49), (x, 61)],
            )

        pygame.draw.line(surface, (255, 255, 255, 55), (472, 25), (472, 67), 1)
        progress_label = self.small_font.render("WORLD PROGRESS", True, (180, 194, 218))
        surface.blit(progress_label, (492, 19))
        bar = pygame.Rect(492, 45, 170, 9)
        pygame.draw.rect(surface, (63, 73, 94), bar, border_radius=5)
        fill = bar.copy()
        fill.width = round(bar.width * max(0.0, min(1.0, progress)))
        if fill.width:
            pygame.draw.rect(surface, (102, 225, 171), fill, border_radius=5)

        controls = self.small_font.render(
            "A/D MOVE   SPACE JUMP   P PAUSE", True, WHITE
        )
        surface.blit(controls, (680, 43))

        score_text = self.small_font.render(f"SCORE {score:06d}", True, GOLD)
        surface.blit(score_text, (680, 19))

        sound_label = "SOUND OFF" if sound_muted else "SOUND ON"
        sound_color = (255, 165, 170) if sound_muted else MINT
        sound = self.small_font.render(sound_label, True, sound_color)
        surface.blit(sound, (874, 19))

        if boost_timer > 0:
            seconds_left = (boost_timer + 59) // 60
            boost = self.small_font.render(f"BOOST {seconds_left}s", True, MINT)
            surface.blit(boost, (790, 19))

        if bullet_timer > 0:
            fire_text = self.small_font.render(
                f"FIRE POWER {bullet_timer:.0f}s",
                True,
                (120, 210, 255),
            )
            surface.blit(fire_text, (790, 62))

    def draw_banner(self, surface, text, center_y, alpha=220):
        """Draw a compact readable gameplay hint or checkpoint notice."""
        rendered = self.font.render(text, True, WHITE)
        width = min(surface.get_width() - 32, rendered.get_width() + 36)
        height = 42
        panel = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(
            panel,
            (18, 28, 48, max(0, min(230, alpha))),
            panel.get_rect(),
            border_radius=14,
        )
        pygame.draw.rect(
            panel,
            (255, 255, 255, max(0, min(75, alpha // 3))),
            panel.get_rect(),
            width=1,
            border_radius=14,
        )
        rect = panel.get_rect(center=(surface.get_width() // 2, center_y))
        surface.blit(panel, rect)
        rendered.set_alpha(max(0, min(255, alpha + 35)))
        surface.blit(rendered, rendered.get_rect(center=rect.center))

    def _overlay(self, surface):
        shade = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        shade.fill((8, 14, 29, 115))
        surface.blit(shade, (0, 0))

    def _card(self, surface, width, height):
        self._overlay(surface)
        rect = pygame.Rect(0, 0, width, height)
        rect.center = surface.get_rect().center
        shadow = pygame.Surface((width + 12, height + 12), pygame.SRCALPHA)
        pygame.draw.rect(shadow, (0, 0, 0, 70), shadow.get_rect(), border_radius=28)
        surface.blit(shadow, (rect.x - 6, rect.y + 8))
        self._panel(surface, rect, color=(22, 31, 55, 238), radius=24)
        return rect


    def _draw_animated_background(self, surface, image, phase=0):
        width, height = surface.get_size()
        image_width, image_height = image.get_size()

        # Image ko screen bharne jitna bada karo, phir halka zoom animate karo.
        zoom = 1.04 + 0.015 * math.sin(pygame.time.get_ticks() / 900 + phase)
        scale = max(width / image_width, height / image_height) * zoom
        new_size = (int(image_width * scale), int(image_height * scale))

        background = pygame.transform.smoothscale(image, new_size)
        x = (width - new_size[0]) // 2
        y = (height - new_size[1]) // 2
        surface.blit(background, (x, y))

        # Text ko background par padhna aasaan banata hai.
        shade = pygame.Surface((width, height), pygame.SRCALPHA)
        shade.fill((10, 16, 32, 15))
        surface.blit(shade, (0, 0))
    
    def draw_start(self, surface):
        self._draw_animated_background(surface, self.menu_background)
        rect = pygame.Rect(
            (surface.get_width() - 700) // 2,
            (surface.get_height() - 300) // 2,
            700,
            300,
        )
        title = self.title_font.render("JUMPBYTE", True, WHITE)
        subtitle = self.subtitle_font.render("A little adventure with a big leap.", True, MINT)
        hint = self.font.render("PRESS ENTER TO PLAY", True, GOLD)
        controls = self.small_font.render(
            "MOVE A/D or arrows  •  JUMP SPACE/W  •  PAUSE P  •  FIRE F",
            True, (209, 219, 237),
        )
        objective = self.small_font.render(
            "Collect the blue power-up to fire • Press T for Python Coach",
            True,
            (209, 219, 237),
        )
        for text, y in ((title, rect.y + 58), (subtitle, rect.y + 128),
                        (hint, rect.y + 194), (controls, rect.y + 240),
                        (objective, rect.y + 268)):
            surface.blit(text, text.get_rect(center=(surface.get_width() // 2, y)))

    def draw_python_tip(self, surface, lesson, seconds_left):
        """Show a small, temporary Python lesson near the top of the screen."""
        width = min(surface.get_width() - 32, 660)
        height = 82
        rect = pygame.Rect(0, 0, width, height)
        rect.midtop = (surface.get_width() // 2, 88)

        self._panel(
            surface,
            rect,
            color=(20, 31, 55, 238),
            radius=16,
        )
        pygame.draw.rect(
            surface,
            (133, 245, 194),
            (rect.x + 1, rect.y + 11, 4, height - 22),
            border_radius=3,
        )

        title = self.small_font.render(
            lesson["title"], True, (133, 245, 194)
        )
        surface.blit(title, (rect.x + 18, rect.y + 9))

        words = lesson["message"].split()
        lines = []
        line = ""
        max_text_width = width - 36

        for word in words:
            candidate = f"{line} {word}".strip()
            if line and self.small_font.size(candidate)[0] > max_text_width:
                lines.append(line)
                line = word
            else:
                line = candidate

        if line:
            lines.append(line)

        for index, text in enumerate(lines[:2]):
            rendered = self.small_font.render(
                text, True, (245, 247, 255)
            )
            surface.blit(
                rendered,
                (rect.x + 18, rect.y + 34 + index * 18),
            )

        bar = pygame.Rect(rect.x + 18, rect.bottom - 6, width - 36, 2)
        pygame.draw.rect(surface, (65, 75, 96), bar, border_radius=2)

        fill = bar.copy()
        fill.width = round(
            bar.width * max(0.0, min(1.0, seconds_left / 3.5))
        )
        if fill.width:
            pygame.draw.rect(
                surface, (133, 245, 194), fill, border_radius=2
            )

        

    def draw_game_over(self, surface, score=0, best_score=0):
        self._draw_animated_background(surface, self.game_over_background, 1)
        rect = pygame.Rect(
            (surface.get_width() - 500) // 2,
            (surface.get_height() - 205) // 2,
            500,
            205,
        )
        title = self.title_font.render("Out of lives", True, WHITE)
        result = self.font.render(
            f"Score {score:,}   •   Best {best_score:,}", True, MINT
        )
        hint = self.font.render("Press R to try again", True, GOLD)
        surface.blit(title, title.get_rect(center=(rect.centerx, rect.y + 77)))
        surface.blit(result, result.get_rect(center=(rect.centerx, rect.y + 119)))
        surface.blit(hint, hint.get_rect(center=(rect.centerx, rect.y + 160)))

    def draw_win(self, surface, score=0, best_score=0):
        self._draw_animated_background(surface, self.win_background, 2)
        rect = pygame.Rect(
            (surface.get_width() - 650) // 2,
            (surface.get_height() - 220) // 2,
            650,
            220,
        )
        title = self.title_font.render("Adventure complete!", True, WHITE)
        result = self.font.render(
            f"Score {score:,}   •   Best {best_score:,}", True, MINT
        )
        hint = self.font.render("You crossed all five worlds. Press R to play again.", True, GOLD)
        surface.blit(title, title.get_rect(center=(rect.centerx, rect.y + 82)))
        surface.blit(result, result.get_rect(center=(rect.centerx, rect.y + 132)))
        surface.blit(hint, hint.get_rect(center=(rect.centerx, rect.y + 174)))

    def draw_pause(self, surface):
        rect = self._card(surface, 430, 180)
        title = self.title_font.render("Paused", True, WHITE)
        hint = self.font.render("Press P to continue", True, MINT)
        surface.blit(title, title.get_rect(center=(rect.centerx, rect.y + 70)))
        surface.blit(hint, hint.get_rect(center=(rect.centerx, rect.y + 125)))

    def draw_world_intro(self, surface, world_number, world_name, timer):
        """Brief world label that fades in and out without blocking play."""
        duration = 1.8
        fade = min(1.0, timer / 0.28, (duration - timer) / 0.28)
        alpha = max(0, min(210, round(210 * fade)))
        width, height = 430, 82
        panel = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(
            panel, (18, 28, 48, alpha), panel.get_rect(), border_radius=18
        )
        pygame.draw.rect(
            panel, (255, 255, 255, round(55 * fade)),
            panel.get_rect(), width=1, border_radius=18,
        )
        center_x = surface.get_width() // 2
        surface.blit(panel, (center_x - width // 2, 102))

        label = self.small_font.render(
            f"WORLD {world_number:02d}  /  05", True, MINT
        )
        title = self.font.render(world_name, True, WHITE)
        label.set_alpha(alpha)
        title.set_alpha(alpha)
        surface.blit(label, label.get_rect(center=(center_x, 125)))
        surface.blit(title, title.get_rect(center=(center_x, 155)))
