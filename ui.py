"""Polished title, HUD, pause, win, and game-over screens."""

import pygame
import math
from sprites import draw_frame, load_frames
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
        self.menu_rat_frames = load_frames("rat", "idle")
        self.menu_control_font = pygame.font.SysFont("Arial", 15, bold=True)
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
        if bullet_timer > 0:
            controls = self.small_font.render(
                f"FIRE: F  {bullet_timer:.0f}s", True, (150, 220, 255)
            )
        surface.blit(controls, (680, 43))

        score_text = self.small_font.render(f"SCORE {score:06d}", True, GOLD)
        surface.blit(score_text, (680, 19))

        sound_label = "SOUND OFF" if sound_muted else "SOUND ON"
        sound_color = (255, 165, 170) if sound_muted else MINT
        sound = self.small_font.render(sound_label, True, sound_color)
        surface.blit(sound, (884, 19))

        if boost_timer > 0:
            seconds_left = (boost_timer + 59) // 60
            boost = self.small_font.render(f"BOOST {seconds_left}s", True, MINT)
            surface.blit(boost, (800, 19))

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

    def draw_world_map(self, surface):
        self._draw_animated_background(surface, self.menu_background, 0.5)

        title = self.subtitle_font.render("YOUR JOURNEY", True, WHITE)
        subtitle = self.small_font.render(
            "Collect every coin to travel through the five worlds",
            True,
            MINT,
        )
        surface.blit(title, title.get_rect(center=(surface.get_width() // 2, 72)))
        surface.blit(subtitle, subtitle.get_rect(center=(surface.get_width() // 2, 108)))

        worlds = [
            ("01", "Green Meadow", "START HERE"),
            ("02", "Moonlit Cave", "UP NEXT"),
            ("03", "Sunset Castle", "UP NEXT"),
            ("04", "Frostfall Peaks", "UP NEXT"),
            ("05", "Skyforge Citadel", "FINAL WORLD"),
        ]

        card_width = 148
        card_height = 150
        gap = 24
        total_width = 5 * card_width + 4 * gap
        start_x = (surface.get_width() - total_width) // 2
        card_y = 190
        centers = []

        for index in range(5):
            x = start_x + index * (card_width + gap)
            centers.append(x + card_width // 2)

        for index in range(4):
            pygame.draw.line(
                surface,
                (133, 245, 194),
                (centers[index] + 46, card_y + 55),
                (centers[index + 1] - 46, card_y + 55),
                4,
            )

        for index, (number, name, status) in enumerate(worlds):
            x = start_x + index * (card_width + gap)
            rect = pygame.Rect(x, card_y, card_width, card_height)
            active = index == 0

            color = (22, 55, 68, 235) if active else (22, 31, 55, 220)
            self._panel(surface, rect, color=color, radius=18)

            circle_color = MINT if active else (120, 135, 160)
            pygame.draw.circle(surface, circle_color, (centers[index], card_y + 55), 28)

            number_text = self.font.render(number, True, INK)
            surface.blit(
                number_text,
                number_text.get_rect(center=(centers[index], card_y + 55)),
            )

            name_text = self.small_font.render(name, True, WHITE)
            surface.blit(
                name_text,
                name_text.get_rect(center=(centers[index], card_y + 105)),
            )

            status_color = GOLD if active else (180, 194, 218)
            status_text = self.small_font.render(status, True, status_color)
            surface.blit(
                status_text,
                status_text.get_rect(center=(centers[index], card_y + 130)),
            )

        hint = self.font.render(
            "Press ENTER to begin  •  ESC to return",
            True,
            GOLD,
        )
        surface.blit(
            hint,
            hint.get_rect(center=(surface.get_width() // 2, 430)),
        )

    def draw_start(self, surface):
        self._draw_animated_background(surface, self.menu_background)

        # Small decorative heading
        pygame.draw.line(surface, MINT, (88, 112), (140, 112), 4)
        eyebrow = self.small_font.render(
            "A PYTHON PLATFORM ADVENTURE",
            True,
            MINT,
        )
        surface.blit(eyebrow, (88, 126))

        # Main title and subtitle
        title = self.title_font.render("JUMPBYTE", True, (255, 224, 135))
        surface.blit(title, (84, 160))

        subtitle = self.subtitle_font.render(
            "Small paws. Big adventure.",
            True,
            WHITE,
        )
        surface.blit(subtitle, (90, 236))

        # Bright outline button, with no dark fill or shadow
        button_rect = pygame.Rect(88, 294, 390, 54)
        pygame.draw.rect(
            surface,
            MINT,
            button_rect,
            width=2,
            border_radius=16,
        )

        pulse = 210 + round(
            45 * (math.sin(pygame.time.get_ticks() / 320) + 1) / 2
        )
        button_text = self.font.render(
            "PRESS ENTER TO EXPLORE",
            True,
            (255, 232, 160),
        )
        button_text.set_alpha(pulse)
        surface.blit(
            button_text,
            button_text.get_rect(center=button_rect.center),
        )

        # Compact centered controls remain clear without competing with the rat.
        label_font = self.menu_control_font
        center_x = surface.get_width() // 2
        labels = [
            ("MOVE: A / D or arrows    JUMP: SPACE / W", 365),
            ("PAUSE: P    FIRE: F after blue power-up", 395),
            ("COINS • PYTHON GATES • REACH THE FLAG", 425),
        ]

        for message, y in labels:
            text = label_font.render(message, True, (255, 246, 215))
            shadow = label_font.render(message, True, (5, 12, 25))
            shadow.set_alpha(175)
            rect = text.get_rect(center=(center_x, y))
            surface.blit(shadow, rect.move(1, 2))
            surface.blit(text, rect)

        frames = self.menu_rat_frames
        frame_index = (pygame.time.get_ticks() // 350) % len(frames)
        bob = round(math.sin(pygame.time.get_ticks() / 430) * 6)

        rat_anchor = pygame.Rect(0, 0, 40, 80)
        rat_anchor.midbottom = (785, 430 + bob)
        draw_frame(surface, frames[frame_index], rat_anchor, 220, True)

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

    def draw_python_challenge(self, surface, challenge, feedback=""):
        shade = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        shade.fill((5, 10, 25, 175))
        surface.blit(shade, (0, 0))

        rect = pygame.Rect(0, 0, 700, 340)
        rect.center = surface.get_rect().center
        self._panel(surface, rect, color=(22, 31, 55, 245), radius=24)

        title = self.subtitle_font.render(
            f"PYTHON GATE  •  {challenge['topic']}",
            True,
            MINT,
        )
        surface.blit(title, (rect.x + 30, rect.y + 25))

        question = self.font.render(challenge["question"], True, WHITE)
        surface.blit(question, (rect.x + 30, rect.y + 75))

        for number, choice in enumerate(challenge["choices"], start=1):
            option = self.font.render(
                f"{number}.  {choice}",
                True,
                WHITE,
            )
            surface.blit(option, (rect.x + 40, rect.y + 125 + number * 38))

        instruction = self.small_font.render(
            "Press 1, 2, or 3 to answer",
            True,
            GOLD,
        )
        surface.blit(instruction, (rect.x + 30, rect.y + 265))

        if feedback:
            hint = self.small_font.render(feedback, True, (255, 190, 150))
            surface.blit(hint, (rect.x + 30, rect.y + 295))    

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
