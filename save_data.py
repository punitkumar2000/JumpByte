"""Save the overall best score and local player profiles."""

import json
from pathlib import Path

from settings import TOTAL_STAGES


SAVE_FILE = Path(__file__).parent / "high_score.json"
EMPTY_PROFILE = {
    "player_name": "",
    "best_score": 0,
    "best_worlds_cleared": 0,
    "last_questions_asked": 0,
    "last_questions_correct": 0,
    "last_score": 0,
    "resume_stage": 1,
    "resume_score": 0,
    "resume_worlds_cleared": 0,
    "resume_questions_asked": 0,
    "resume_questions_correct": 0,
    "concepts_learned": [],
}


def _read_save_data():
    """Read saved data safely, including older score-only save files."""
    try:
        data = json.loads(SAVE_FILE.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError, TypeError, json.JSONDecodeError):
        return {}


def _profile_key(player_name):
    return " ".join(str(player_name).strip().split()).casefold()


def load_best_score():
    """Return the saved record, or zero if this is a fresh/invalid save."""
    try:
        return max(0, int(_read_save_data().get("best_score", 0)))
    except (ValueError, TypeError):
        return 0


def save_best_score(score):
    """Keep the overall best score without removing player profiles."""
    try:
        data = _read_save_data()
        data["best_score"] = max(int(data.get("best_score", 0)), int(score))
        SAVE_FILE.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    except (OSError, ValueError, TypeError):
        # A read-only install should still let the game run normally.
        pass


def load_player_profile(player_name):
    """Load one case-insensitive player profile, or return a fresh profile."""
    key = _profile_key(player_name)
    profile = dict(EMPTY_PROFILE)
    if not key:
        return profile

    players = _read_save_data().get("players", {})
    saved_profile = players.get(key, {}) if isinstance(players, dict) else {}
    if not isinstance(saved_profile, dict):
        saved_profile = {}
    profile.update(saved_profile)
    profile["player_name"] = str(player_name).strip()
    try:
        for field in (
            "best_score", "best_worlds_cleared", "last_questions_asked",
            "last_questions_correct", "last_score", "resume_stage",
            "resume_score", "resume_worlds_cleared",
            "resume_questions_asked", "resume_questions_correct",
        ):
            profile[field] = max(0, int(profile.get(field, 0)))
    except (ValueError, TypeError):
        return dict(EMPTY_PROFILE, player_name=str(player_name).strip())
    if not isinstance(profile.get("concepts_learned"), list):
        profile["concepts_learned"] = []
    if "resume_stage" not in saved_profile:
        cleared = min(TOTAL_STAGES, profile["best_worlds_cleared"])
        if cleared >= TOTAL_STAGES:
            profile["resume_stage"] = 1
        else:
            profile["resume_stage"] = cleared + 1
            profile["resume_worlds_cleared"] = cleared
            if cleared:
                profile["resume_score"] = profile["last_score"]
                profile["resume_questions_asked"] = profile["last_questions_asked"]
                profile["resume_questions_correct"] = profile["last_questions_correct"]
    profile["resume_stage"] = min(TOTAL_STAGES, max(1, profile["resume_stage"]))
    return profile


def save_player_profile(player_name, profile):
    """Save a profile by name while keeping the shared best-score field."""
    key = _profile_key(player_name)
    if not key:
        return
    try:
        data = _read_save_data()
        players = data.get("players", {})
        if not isinstance(players, dict):
            players = {}
        safe_profile = dict(EMPTY_PROFILE)
        safe_profile.update(profile)
        safe_profile["player_name"] = str(player_name).strip()
        safe_profile["concepts_learned"] = sorted(
            {str(topic) for topic in safe_profile.get("concepts_learned", [])}
        )
        players[key] = safe_profile
        data["players"] = players
        data["best_score"] = max(
            int(data.get("best_score", 0)), int(safe_profile["best_score"])
        )
        SAVE_FILE.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    except (OSError, ValueError, TypeError):
        # A read-only install should still let the game run normally.
        pass
