"""Polished title, HUD, pause, win, and game-over screens."""

import pygame
import math
from sprites import draw_frame, load_frames
from pathlib import Path
from settings import MAX_LIVES, TOTAL_STAGES


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

        label = self.small_font.render(f"WORLD {stage_number:02d}  /  {TOTAL_STAGES:02d}", True, MINT)
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
        lives_label = self.small_font.render("STAGE LIVES", True, (180, 194, 218))
        lives_value = self.font.render(f"{lives}/{MAX_LIVES}", True, WHITE)
        surface.blit(lives_label, (375, 19))
        surface.blit(lives_value, (375, 39))

        pygame.draw.line(surface, (255, 255, 255, 55), (490, 25), (490, 67), 1)
        progress_label = self.small_font.render("WORLD PROGRESS", True, (180, 194, 218))
        surface.blit(progress_label, (510, 19))
        bar = pygame.Rect(510, 45, 160, 9)
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

    def draw_world_map(self, surface, player_name="", profile=None):
        self._draw_animated_background(surface, self.menu_background, 0.5)
        profile = profile or {}

        title = self.subtitle_font.render("YOUR JOURNEY", True, WHITE)
        subtitle = self.small_font.render(
            f"Collect every coin to travel through {TOTAL_STAGES} worlds",
            True,
            MINT,
        )
        surface.blit(title, title.get_rect(center=(surface.get_width() // 2, 68)))
        surface.blit(subtitle, subtitle.get_rect(center=(surface.get_width() // 2, 101)))

        saved_progress = self.small_font.render(
            f"Welcome, {player_name}   •   Best score: {profile.get('best_score', 0):,}"
            f"   •   Worlds cleared: {profile.get('best_worlds_cleared', 0)}/{TOTAL_STAGES}",
            True,
            GOLD,
        )
        surface.blit(
            saved_progress,
            saved_progress.get_rect(center=(surface.get_width() // 2, 135)),
        )

        world_names = [
            "Green Meadow", "Moonlit Cave", "Sunset Castle", "Frostfall Peaks",
            "Skyforge Citadel", "Ember Dunes", "Coral Reef", "Clockwork Factory",
            "Cloud Kingdom", "Python Core",
        ]
        worlds = [
            (f"{number:02d}", name,
             "START HERE" if number == 1 else
             "FINAL WORLD" if number == TOTAL_STAGES else "UP NEXT")
            for number, name in enumerate(world_names, start=1)
        ]

        card_width, card_height, gap = 145, 102, 14
        total_width = 5 * card_width + 4 * gap
        start_x = (surface.get_width() - total_width) // 2
        first_row_y, row_gap = 166, 15
        centers = [start_x + index * (card_width + gap) + card_width // 2 for index in range(5)]

        for row in range(2):
            row_y = first_row_y + row * (card_height + row_gap)
            for index in range(4):
                pygame.draw.line(
                    surface, (133, 245, 194),
                    (centers[index] + 42, row_y + 36),
                    (centers[index + 1] - 42, row_y + 36), 3,
                )

        for index, (number, name, status) in enumerate(worlds):
            row, column = divmod(index, 5)
            x = start_x + column * (card_width + gap)
            card_y = first_row_y + row * (card_height + row_gap)
            rect = pygame.Rect(x, card_y, card_width, card_height)
            active = index == 0
            color = (22, 55, 68, 235) if active else (22, 31, 55, 220)
            self._panel(surface, rect, color=color, radius=16)

            center = (centers[column], card_y + 34)
            pygame.draw.circle(surface, MINT if active else (120, 135, 160), center, 21)
            number_text = self.font.render(number, True, INK)
            surface.blit(number_text, number_text.get_rect(center=center))

            name_text = self.small_font.render(name, True, WHITE)
            surface.blit(name_text, name_text.get_rect(center=(centers[column], card_y + 68)))
            status_color = GOLD if active else (180, 194, 218)
            status_text = self.small_font.render(status, True, status_color)
            surface.blit(status_text, status_text.get_rect(center=(centers[column], card_y + 89)))

        hint = self.font.render(
            "ENTER: begin adventure  •  N: switch player  •  ESC: back",
            True,
            GOLD,
        )
        surface.blit(hint, hint.get_rect(center=(surface.get_width() // 2, 424)))

    def draw_start(self, surface, player_name="", profile=None):
        self._draw_animated_background(surface, self.menu_background)
        profile = profile or {}

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

        # Player name field uses a bright outline so it stays readable on the art.
        button_rect = pygame.Rect(88, 294, 390, 54)
        pygame.draw.rect(
            surface,
            MINT,
            button_rect,
            width=2,
            border_radius=16,
        )

        field_text = (
            f"PLAYER: {player_name}  |"
            if player_name
            else "TYPE YOUR NAME, THEN PRESS ENTER"
        )
        button_text = self.font.render(field_text, True, (255, 232, 160))
        surface.blit(
            button_text,
            button_text.get_rect(center=button_rect.center),
        )

        if player_name:
            topics = profile.get("concepts_learned", [])
            topic_names = ", ".join(topics[:4]) if topics else "none yet"
            if len(topics) > 4:
                topic_names += ", and more"
            progress_text = (
                f"BEST SCORE: {profile.get('best_score', 0):,}"
                f"    WORLDS CLEARED: {profile.get('best_worlds_cleared', 0)}/{TOTAL_STAGES}"
            )
            quiz_text = (
                f"LAST QUIZ: {profile.get('last_questions_correct', 0)}/"
                f"{profile.get('last_questions_asked', 0)}"
                f"    TOPICS: {topic_names}"
            )
        else:
            progress_text = "Your score and learning progress will be saved under this name."
            quiz_text = "Use the same name next time to view your saved progress."

        for message, y in ((progress_text, 357), (quiz_text, 378)):
            line = self.small_font.render(message, True, WHITE)
            shadow = self.small_font.render(message, True, (5, 12, 25))
            shadow.set_alpha(190)
            rect = line.get_rect(topleft=(90, y))
            surface.blit(shadow, rect.move(1, 2))
            surface.blit(line, rect)

        # Compact centered controls remain clear without competing with the rat.
        label_font = self.menu_control_font
        center_x = surface.get_width() // 2
        labels = [
            ("MOVE: A / D or arrows    JUMP: SPACE / W", 414),
            ("PAUSE: P    FIRE: F after blue power-up", 438),
            ("COINS • PYTHON GATES • REACH THE FLAG", 462),
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

    def draw_python_challenge(
        self, surface, challenge, feedback="", answered=False,
        question_number=1, question_total=1,
    ):
        shade = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        shade.fill((5, 10, 25, 175))
        surface.blit(shade, (0, 0))

        rect = pygame.Rect(0, 0, 700, 340)
        rect.center = surface.get_rect().center
        self._panel(surface, rect, color=(22, 31, 55, 245), radius=24)

        title = self.subtitle_font.render(
            f"PYTHON GATE  •  {challenge['topic']}  •  {question_number}/{question_total}",
            True,
            MINT,
        )
        surface.blit(title, (rect.x + 30, rect.y + 25))

        question = self.font.render(challenge["question"], True, WHITE)
        surface.blit(question, (rect.x + 30, rect.y + 75))

        if answered:
            result = self.font.render("Correct!", True, MINT)
            surface.blit(result, (rect.x + 30, rect.y + 125))

            words = challenge["explanation"].split()
            lines = []
            line = ""
            max_width = rect.width - 60
            for word in words:
                candidate = f"{line} {word}".strip()
                if line and self.small_font.size(candidate)[0] > max_width:
                    lines.append(line)
                    line = word
                else:
                    line = candidate
            if line:
                lines.append(line)

            for index, explanation_line in enumerate(lines[:3]):
                rendered_line = self.small_font.render(
                    explanation_line, True, WHITE
                )
                surface.blit(
                    rendered_line,
                    (rect.x + 30, rect.y + 165 + index * 24),
                )

            instruction = self.small_font.render(
                "Press ENTER to continue",
                True,
                GOLD,
            )
            surface.blit(instruction, (rect.x + 30, rect.y + 280))
        else:
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

    def draw_code_checkpoint(self, surface, challenge, feedback="", answered=False):
        """Pause play and show a short multiple-choice code blank."""
        shade = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        shade.fill((5, 10, 25, 190))
        surface.blit(shade, (0, 0))

        rect = pygame.Rect(0, 0, 740, 410)
        rect.center = surface.get_rect().center
        self._panel(surface, rect, color=(22, 31, 55, 250), radius=24)
        title = self.subtitle_font.render(
            f"CODE CHECKPOINT  |  {challenge['topic']}", True, MINT
        )
        surface.blit(title, title.get_rect(center=(rect.centerx, rect.y + 31)))

        question = self.small_font.render(challenge["question"], True, WHITE)
        surface.blit(question, (rect.x + 32, rect.y + 68))

        code_rect = pygame.Rect(rect.x + 28, rect.y + 99, rect.width - 56, 68)
        pygame.draw.rect(surface, (9, 17, 34), code_rect, border_radius=12)
        pygame.draw.rect(surface, (85, 125, 160), code_rect, width=1, border_radius=12)
        code_lines = challenge["code"].splitlines()
        code_size = 23
        code_font = pygame.font.SysFont("monospace", code_size, bold=True)
        while max(code_font.size(line)[0] for line in code_lines) > code_rect.width - 28:
            code_size -= 1
            code_font = pygame.font.SysFont("monospace", code_size, bold=True)
        line_height = max(23, code_font.get_linesize())
        code_y = code_rect.centery - len(code_lines) * line_height // 2
        for line in code_lines:
            rendered = code_font.render(line, True, GOLD)
            surface.blit(rendered, rendered.get_rect(center=(code_rect.centerx, code_y)))
            code_y += line_height

        if answered:
            result = self.font.render("Correct! The gate is open.", True, MINT)
            surface.blit(result, (rect.x + 32, rect.y + 187))
            lines = self._wrap_lines(
                challenge["explanation"], self.small_font, rect.width - 64
            )
            for index, line in enumerate(lines[:3]):
                text = self.small_font.render(line, True, WHITE)
                surface.blit(text, (rect.x + 32, rect.y + 226 + index * 24))
            instruction = self.small_font.render(
                "Press ENTER to continue playing", True, GOLD
            )
            surface.blit(instruction, (rect.x + 32, rect.bottom - 32))
            return

        for number, choice in enumerate(challenge["choices"], start=1):
            option = self.font.render(f"{number}.  {choice}", True, WHITE)
            surface.blit(option, (rect.x + 42, rect.y + 183 + (number - 1) * 39))

        instruction = self.small_font.render(
            "Choose 1, 2, or 3. A wrong answer gives you a hint.",
            True,
            GOLD,
        )
        surface.blit(instruction, (rect.x + 32, rect.bottom - 66))
        if feedback:
            for index, line in enumerate(self._wrap_lines(feedback, self.small_font, rect.width - 64)[:2]):
                hint = self.small_font.render(line, True, (255, 190, 150))
                surface.blit(hint, (rect.x + 32, rect.bottom - 42 + index * 18))

    def _wrap_lines(self, text, font, max_width):
        lines = []
        line = ""
        for word in text.split():
            candidate = f"{line} {word}".strip()
            if line and font.size(candidate)[0] > max_width:
                lines.append(line)
                line = word
            else:
                line = candidate
        if line:
            lines.append(line)
        return lines

    def draw_stage_summary(
        self, surface, world_number, world_name, stage_score, total_score,
        questions_correct, questions_asked, concepts, is_final=False,
    ):
        """Show the world result and the learning collected in that world."""
        rect = self._card(surface, 740, 350)
        title = self.subtitle_font.render(
            f"WORLD {world_number} COMPLETE", True, MINT
        )
        name = self.font.render(world_name, True, WHITE)
        score = self.font.render(
            f"World points: +{stage_score:,}     Total score: {total_score:,}",
            True,
            GOLD,
        )
        quiz = self.font.render(
            f"Python questions: {questions_correct}/{questions_asked} correct",
            True,
            WHITE,
        )
        learned = self.small_font.render("WHAT YOU PRACTISED", True, MINT)
        topics_text = ", ".join(concepts) if concepts else "Keep playing to discover more Python ideas."
        topic_lines = self._wrap_lines(topics_text, self.small_font, rect.width - 70)

        surface.blit(title, title.get_rect(center=(rect.centerx, rect.y + 48)))
        surface.blit(name, name.get_rect(center=(rect.centerx, rect.y + 92)))
        surface.blit(score, score.get_rect(center=(rect.centerx, rect.y + 140)))
        surface.blit(quiz, quiz.get_rect(center=(rect.centerx, rect.y + 180)))
        surface.blit(learned, learned.get_rect(center=(rect.centerx, rect.y + 222)))
        for index, line in enumerate(topic_lines[:3]):
            rendered = self.small_font.render(line, True, WHITE)
            surface.blit(
                rendered,
                rendered.get_rect(center=(rect.centerx, rect.y + 247 + index * 19)),
            )
        hint_text = "Press ENTER to finish your adventure" if is_final else "Press ENTER for the next world"
        hint = self.small_font.render(hint_text, True, GOLD)
        surface.blit(hint, hint.get_rect(center=(rect.centerx, rect.bottom - 24)))

    def _draw_end_screen(
        self, surface, background, phase, title_text, score, best_score,
        worlds_cleared, questions_correct, questions_asked, concepts, hint_text,
    ):
        self._draw_animated_background(surface, background, phase)
        rect = self._card(surface, 790, 360)
        title = self.subtitle_font.render(title_text, True, WHITE)
        result = self.font.render(
            f"Score {score:,}   •   Best {best_score:,}", True, GOLD
        )
        reflection_title = self.small_font.render(
            "YOUR LEARNING JOURNEY", True, MINT
        )
        progress = self.font.render(
            f"Worlds cleared: {worlds_cleared}/{TOTAL_STAGES}    •    Python answers: {questions_correct}/{questions_asked}",
            True,
            WHITE,
        )
        topics = ", ".join(concepts) if concepts else "Play more worlds to discover Python concepts."
        topic_lines = self._wrap_lines(topics, self.small_font, rect.width - 70)
        surface.blit(title, title.get_rect(center=(rect.centerx, rect.y + 48)))
        surface.blit(result, result.get_rect(center=(rect.centerx, rect.y + 94)))
        surface.blit(
            reflection_title,
            reflection_title.get_rect(center=(rect.centerx, rect.y + 143)),
        )
        surface.blit(progress, progress.get_rect(center=(rect.centerx, rect.y + 180)))
        for index, line in enumerate(topic_lines[:3]):
            rendered = self.small_font.render(line, True, WHITE)
            surface.blit(
                rendered,
                rendered.get_rect(center=(rect.centerx, rect.y + 215 + index * 20)),
            )
        hint = self.small_font.render(hint_text, True, GOLD)
        surface.blit(hint, hint.get_rect(center=(rect.centerx, rect.bottom - 24)))

    def draw_game_over(
        self, surface, score=0, best_score=0, worlds_cleared=0,
        questions_correct=0, questions_asked=0, concepts=(),
    ):
        self._draw_end_screen(
            surface, self.game_over_background, 1, "Out of lives",
            score, best_score, worlds_cleared, questions_correct,
            questions_asked, concepts, "Press R to try again",
        )

    def draw_win(
        self, surface, score=0, best_score=0, worlds_cleared=5,
        questions_correct=0, questions_asked=0, concepts=(),
    ):
        self._draw_end_screen(
            surface, self.win_background, 2, "Adventure complete!",
            score, best_score, worlds_cleared, questions_correct,
            questions_asked, concepts, "Press R to play again",
        )

    def pause_button_rects(self, surface):
        """Return the Home and Resume button positions for drawing and clicks."""
        width, height = 360, 48
        left = (surface.get_width() - width) // 2
        top = (surface.get_height() - 276) // 2 + 112
        return [
            pygame.Rect(left, top, width, height),
            pygame.Rect(left, top + 60, width, height),
        ]

    def draw_pause(self, surface, selected_index=1, mouse_pos=None):
        rect = self._card(surface, 500, 276)
        title = self.subtitle_font.render("GAME PAUSED", True, WHITE)
        surface.blit(title, title.get_rect(center=(rect.centerx, rect.y + 48)))

        labels = ("HOME  •  Restart from the beginning", "RESUME  •  Continue this run")
        for index, (button, label) in enumerate(zip(self.pause_button_rects(surface), labels)):
            hovered = mouse_pos is not None and button.collidepoint(mouse_pos)
            active = index == selected_index or hovered
            fill = (48, 104, 120, 245) if active else (35, 47, 72, 235)
            border = MINT if active else (105, 128, 158)
            self._panel(surface, button, color=fill, radius=14)
            pygame.draw.rect(surface, border, button, width=2, border_radius=14)
            text = self.font.render(label, True, GOLD if index == 0 else WHITE)
            surface.blit(text, text.get_rect(center=button.center))

        hint = self.small_font.render("W/S or Up/Down   •   ENTER Choose   •   P/ESC Resume", True, MINT)
        surface.blit(hint, hint.get_rect(center=(rect.centerx, rect.bottom - 22)))

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
            f"WORLD {world_number:02d}  /  {TOTAL_STAGES:02d}", True, MINT
        )
        title = self.font.render(world_name, True, WHITE)
        label.set_alpha(alpha)
        title.set_alpha(alpha)
        surface.blit(label, label.get_rect(center=(center_x, 125)))
        surface.blit(title, title.get_rect(center=(center_x, 155)))
