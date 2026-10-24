"""Small local save file for the player's best JumpByte score."""

import json
from pathlib import Path


SAVE_FILE = Path(__file__).parent / "high_score.json"


def load_best_score():
    """Return the saved record, or zero if this is a fresh/invalid save."""
    try:
        data = json.loads(SAVE_FILE.read_text(encoding="utf-8"))
        return max(0, int(data.get("best_score", 0)))
    except (OSError, ValueError, TypeError, json.JSONDecodeError):
        return 0


def save_best_score(score):
    """Write a small JSON record; create the file only after a new record."""
    try:
        SAVE_FILE.write_text(
            json.dumps({"best_score": int(score)}, indent=2) + "\n",
            encoding="utf-8",
        )
    except OSError:
        # A read-only install should still let the game run normally.
        pass
