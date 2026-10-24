# JumpByte

JumpByte is an original 2D platformer built with Python and Pygame. Play as a rat, explore five themed worlds, collect coins, use speed boosts, stomp enemy cats, and defeat the final boss.

The game code, level layouts, scenery, effects, and sound effects are made for JumpByte. Rat and cat animations are loaded from the sprite assets in `assets/characters/`. The game does not use Mario characters, names, sprites, or sounds.

## Features

- Five worlds: Green Meadow, Moonlit Cave, Sunset Castle, Frostfall Peaks, and Skyforge Citadel
- Rat character with movement, jumping, gravity, and platform collisions
- Cat enemies that patrol and fire projectiles
- Stomping attacks, including a health-based final boss with an enraged phase
- Coins required to unlock each world’s exit
- Points for coins, enemies, checkpoints, and completing worlds; best score saves locally
- Themed floor hazards that must be jumped over
- Speed-boost power-ups
- Mid-world checkpoints, lives, respawn, game-over, and restart
- Original scenery, platform details, animated characters, and visual effects
- Generated sound effects for coins, jumps, power-ups, checkpoints, stomps, and damage
- `M` key to mute or unmute sound effects
- Start, pause, game-over, and victory screens

## Worlds and objectives

1. **Green Meadow** — collect every coin and reach the exit.
2. **Moonlit Cave** — collect every coin and avoid the patrolling cats.
3. **Sunset Castle** — collect every coin and reach the exit.
4. **Frostfall Peaks** — collect every coin and reach the exit.
5. **Skyforge Citadel** — collect every coin, defeat the final boss, and reach the exit to win.

## Controls

| Key | Action |
| --- | --- |
| Enter | Start the game |
| A / D or Left / Right arrows | Move |
| Space, Up arrow, or W | Jump |
| P | Pause or resume |
| M | Mute or unmute sound effects |
| R | Restart after game over or winning |

## Setup and run

### macOS

From the project folder, open Terminal and run:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
```

### Windows PowerShell

From the project folder, open PowerShell and run:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

## Project files

| File | Purpose |
| --- | --- |
| `main.py` | Starts the game |
| `game.py` | Game loop, events, stages, collisions, and drawing |
| `player.py` | Player movement, jumping, and animation |
| `enemy.py` | Cat enemies, projectiles, and boss |
| `objects.py` | Platforms, coins, and power-ups |
| `sprites.py` | Loads, aligns, scales, and draws character animation frames |
| `effects.py` | Particle bursts for pickups, jumps, damage, and stomps |
| `levels.py` | Layouts and data for the five worlds |
| `ui.py` | Start screen, HUD, pause, game-over, and win screens |
| `sound_effects.py` | Generated sound effects and mute control |
| `save_data.py` | Loads and saves the local best score |
| `settings.py` | Shared game settings |
| `workload.py` | Suggested module map for viva preparation |

## Python concepts used

The project uses variables, conditionals, loops, functions, modules, lists, tuples, dictionaries, classes, objects, and inheritance. `Boss` inherits from `Enemy`; the game stores platforms, coins, enemies, and power-ups in collections.

## Project note

This is an educational, AI-assisted project. This is an educational, AI-assisted project. The viva topic map is a study guide, not a record of authorship; describe actual contributions honestly and explain the modules you understand.
