"""Polished title, HUD, pause, win, and game-over screens."""

import pygame


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

    def draw_start(self, surface):
        rect = self._card(surface, 700, 300)
        title = self.title_font.render("JUMPBYTE", True, WHITE)
        subtitle = self.subtitle_font.render("A little adventure with a big leap.", True, MINT)
        hint = self.font.render("PRESS ENTER TO PLAY", True, GOLD)
        controls = self.small_font.render(
            "MOVE  A / D or arrows     •     JUMP  SPACE / W / ↑     •     PAUSE  P",
            True, (209, 219, 237),
        )
        objective = self.small_font.render(
            "Explore five worlds • collect every coin • outsmart the cat",
            True, (209, 219, 237),
        )
        for text, y in ((title, rect.y + 58), (subtitle, rect.y + 128),
                        (hint, rect.y + 194), (controls, rect.y + 240),
                        (objective, rect.y + 268)):
            surface.blit(text, text.get_rect(center=(surface.get_width() // 2, y)))

    def draw_game_over(self, surface, score=0, best_score=0):
        rect = self._card(surface, 500, 205)
        title = self.title_font.render("Out of lives", True, WHITE)
        result = self.font.render(
            f"Score {score:,}   •   Best {best_score:,}", True, MINT
        )
        hint = self.font.render("Press R to try again", True, GOLD)
        surface.blit(title, title.get_rect(center=(rect.centerx, rect.y + 77)))
        surface.blit(result, result.get_rect(center=(rect.centerx, rect.y + 119)))
        surface.blit(hint, hint.get_rect(center=(rect.centerx, rect.y + 160)))

    def draw_win(self, surface, score=0, best_score=0):
        rect = self._card(surface, 650, 220)
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
