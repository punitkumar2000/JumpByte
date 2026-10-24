"""Suggested module map for the team viva; not a record of authorship."""

TEAM_WORK = {
    "Suggested viva topic 1 - Engine and integration": [
        "game.Game", "game.Game.run", "main.Game",
    ],
    "Suggested viva topic 2 - Player and animation": [
        "player.Player", "player.Player.update", "sprites.draw_frame",
    ],
    "Suggested viva topic 3 - Enemies and boss": [
        "enemy.Enemy", "enemy.Boss", "enemy.Bullet", "game.Game.lose_life",
    ],
    "Suggested viva topic 4 - Objects and effects": [
        "objects.Platform", "objects.Coin", "objects.PowerUp",
        "objects.Hazard", "effects.ParticleSystem",
    ],
    "Suggested viva topic 5 - Worlds, interface, and saved score": [
        "levels.build_stage_one", "ui.UI", "save_data.load_best_score",
    ],
}

PHASES = {
    "Worlds 1-2": "Green Meadow and Moonlit Cave",
    "Worlds 3-4": "Sunset Castle and Frostfall Peaks",
    "World 5 and finishing systems": (
        "Skyforge Citadel, final boss, score, sound, effects, and saved best score"
    ),
}
