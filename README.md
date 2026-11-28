# JumpByte

JumpByte is an original 2D platformer built with Python and Pygame. Play as a rat, explore ten themed worlds, collect coins, use speed boosts, stomp enemy cats, and defeat the final boss.

The game code, level layouts, scenery, effects, and sound effects are made for JumpByte. Rat and cat animations are loaded from the sprite assets in `assets/characters/`. The game does not use Mario characters, names, sprites, or sounds.

## Features

- Ten worlds: Green Meadow, Moonlit Cave, Sunset Castle, Frostfall Peaks, Skyforge Citadel, Ember Dunes, Coral Reef, Clockwork Factory, Cloud Kingdom, and Python Core
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
- A vertical moving platform in Green Meadow that carries the player
- Cheese bonus pickups that bounce out when cats or the boss are defeated
- A blue fire power-up in Moonlit Cave; press `F` to shoot while it is active
- Two different random Python questions at each world exit, with hints and answer explanations
- A world score recap after the quiz and a learning summary on both win and game-over screens
- Easy-to-change lives, world size, quiz length, score rewards, and enemy tuning in `settings.py`
- Named local player profiles that show each player's best score, worlds cleared, quiz result, and learned Python topics

## Worlds and objectives

1. **Green Meadow** — collect every coin and reach the exit.
2. **Moonlit Cave** — collect every coin and avoid the patrolling cats.
3. **Sunset Castle** — collect every coin and reach the exit.
4. **Frostfall Peaks** — collect every coin and reach the exit.
5. **Skyforge Citadel** — collect every coin, defeat its boss, and reach the exit.
6. **Ember Dunes** — cross desert platforms, avoid hazards, and collect every coin.
7. **Coral Reef** — travel across underwater platforms and a moving lift.
8. **Clockwork Factory** — navigate factory platforms and avoid floor hazards.
9. **Cloud Kingdom** — cross floating islands and moving platforms.
10. **Python Core** — collect every coin, defeat the final boss, and reach the exit to win.

## Controls

| Key | Action |
| --- | --- |
| Type a name, Enter | Load or create that player's local profile and open the journey map |
| Enter on the journey map | Start the adventure; also continue after quiz explanations and world recaps |
| N on the journey map | Switch to another player profile |
| A / D or Left / Right arrows | Move |
| Space, Up arrow, or W | Jump |
| P | Pause or resume |
| M | Mute or unmute sound effects |
| F | Fire while the blue power-up is active |
| E | Open the Python challenge near the exit after meeting its requirements |
| 1 / 2 / 3 | Choose an answer in a Python challenge |
| T | Turn Python Coach lessons on or off |
| R | Restart after game over or winning |
| F11 | Toggle fullscreen/windowed mode where the system sends F11 to the game |

The game opens in a resizable window. On macOS, use the green window button for fullscreen; some Mac keyboards reserve `F11` for system controls.

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
| `objects.py` | Platforms, moving platforms, coins, power-ups, cheese drops, and hazards |
| `sprites.py` | Loads, aligns, scales, and draws character animation frames |
| `effects.py` | Particle bursts for pickups, jumps, damage, and stomps |
| `levels.py` | Layouts and data for all ten worlds |
| `ui.py` | Start screen, HUD, pause, game-over, and win screens |
| `sound_effects.py` | Generated sound effects and mute control |
| `save_data.py` | Loads and saves the overall best score and named player profiles |
| `settings.py` | Shared window, movement, lives, quiz, score, and enemy settings |
| `python_challenges.py` | Python questions and answer feedback for each world |
| `python_concepts.py` | Short Python Coach explanations shown during play |
| `workload.py` | Suggested module map for viva preparation |
| `PRESENTATION_GUIDE.md` | Demo walkthrough and viva revision notes |
| `TEAM_CODE_GUIDE.md` | Five-member file split, key functions, and simple code explanations |

## Python concepts used

The project uses variables, conditionals, loops, functions, modules, lists, tuples, dictionaries, classes, objects, and inheritance. `Boss` inherits from `Enemy`; the game stores platforms, coins, enemies, and power-ups in collections.

To adjust the game without searching several files, edit the clearly marked **EASY GAME SETTINGS** section in `settings.py`. For example, change `MAX_LIVES` to change starting lives, `QUIZ_QUESTIONS_PER_WORLD` to change the number of gate questions, and the `SCORE_...` values to adjust rewards. Movement and enemy values are in the same section. `WORLD_WIDTH` changes the overall world bounds; if you change it substantially, review platform and object positions in `levels.py` too.

At the start screen, type a player name and press Enter. JumpByte saves that name's best score, furthest worlds cleared, latest quiz result, and learned topics in `high_score.json` on this computer. Enter the same name next time to see that profile. These profiles are local and do not sync between computers; the save file is ignored by Git.

## Project note

This is an educational, AI-assisted project. The viva topic map is a study guide; explain the parts you understand and describe each team member's contribution accurately.

Before submission, add the source and license/credit for any downloaded character or background artwork to the project materials.
