"""Simple original sound effects generated with Python and Pygame."""

import math
from array import array

import pygame


class SoundEffects:
    def __init__(self):
        self.enabled = False
        self.muted = False

        try:
            pygame.mixer.quit()
            pygame.mixer.init(
                frequency=22050,
                size=-16,
                channels=1,
                buffer=512,
            )
            self.sample_rate = 22050

            self.coin_sound = self._make_tone(
                start_frequency=900,
                end_frequency=1300,
                duration=0.12,
                volume=0.35,
            )
            self.stomp_sound = self._make_tone(
                start_frequency=260,
                end_frequency=90,
                duration=0.16,
                volume=0.45,
            )
            self.jump_sound = self._make_tone(
                start_frequency=420,
                end_frequency=760,
                duration=0.10,
                volume=0.25,
            )
            self.powerup_sound = self._make_tone(
                start_frequency=620,
                end_frequency=1480,
                duration=0.24,
                volume=0.32,
            )
            self.checkpoint_sound = self._make_tone(
                start_frequency=780,
                end_frequency=1180,
                duration=0.18,
                volume=0.28,
            )
            self.damage_sound = self._make_tone(
                start_frequency=520,
                end_frequency=140,
                duration=0.22,
                volume=0.35,
            )
            self.enabled = True
        except pygame.error:
            # The game can still run if the computer has no audio device.
            self.enabled = False

    def _make_tone(self, start_frequency, end_frequency, duration, volume):
        sample_count = int(self.sample_rate * duration)
        samples = array("h")

        for index in range(sample_count):
            progress = index / sample_count
            frequency = start_frequency + (
                end_frequency - start_frequency
            ) * progress
            envelope = (1 - progress) ** 2
            wave_value = math.sin(
                2 * math.pi * frequency * index / self.sample_rate
            )
            samples.append(int(32767 * volume * envelope * wave_value))

        return pygame.mixer.Sound(buffer=samples.tobytes())

    def play_coin(self):
        if self.enabled and not self.muted:
            self.coin_sound.play()

    def play_stomp(self):
        if self.enabled and not self.muted:
            self.stomp_sound.play()

    def play_jump(self):
        if self.enabled and not self.muted:
            self.jump_sound.play()

    def play_powerup(self):
        if self.enabled and not self.muted:
            self.powerup_sound.play()

    def play_checkpoint(self):
        if self.enabled and not self.muted:
            self.checkpoint_sound.play()

    def play_damage(self):
        if self.enabled and not self.muted:
            self.damage_sound.play()

    def toggle_mute(self):
        self.muted = not self.muted
        return self.muted
