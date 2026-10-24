"""Small helpers for loading and drawing the game's original sprite art."""

from functools import lru_cache
from pathlib import Path

import pygame


FRAME_DIRECTORY = Path(__file__).parent / "assets" / "characters" / "frames"
_SCALED_FRAMES = {}


@lru_cache(maxsize=None)
def load_frames(character, animation):
    """Load frames on one shared canvas so their feet/pivot stay still."""
    images = []
    for index in range(4):
        path = FRAME_DIRECTORY / f"{character}_{animation}_{index}.png"
        images.append(pygame.image.load(str(path)).convert_alpha())

    canvas_width = max(frame.get_width() for frame in images)
    canvas_height = max(frame.get_height() for frame in images)
    frames = []
    for image in images:
        # Center horizontally and align every pose to the same floor baseline.
        canvas = pygame.Surface((canvas_width, canvas_height), pygame.SRCALPHA)
        x = (canvas_width - image.get_width()) // 2
        y = canvas_height - image.get_height()
        canvas.blit(image, (x, y))
        frames.append(canvas)
    return tuple(frames)


def draw_frame(surface, frame, anchor_rect, height, facing_right=True):
    """Draw a proportional sprite centered over its existing collision box."""
    key = (id(frame), height, facing_right)
    scaled = _SCALED_FRAMES.get(key)
    if scaled is None:
        scale = height / frame.get_height()
        width = max(1, round(frame.get_width() * scale))
        scaled = pygame.transform.smoothscale(frame, (width, height))
        if not facing_right:
            scaled = pygame.transform.flip(scaled, True, False)
        _SCALED_FRAMES[key] = scaled

    destination = scaled.get_rect(midbottom=(anchor_rect.centerx, anchor_rect.bottom))
    surface.blit(scaled, destination)
