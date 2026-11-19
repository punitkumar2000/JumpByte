# JumpByte: Team Code Guide

This guide divides the project into five viva topics. It explains the real files and function names in simple language. Use it to study the code, and describe only the work your team actually did.

## How the whole game works

```text
main.py starts Game.run()
        ↓
handle_events() reads keyboard and window events
        ↓
update() changes the game state
        ↓
draw() draws the world, characters, and interface
        ↺ repeats until the player quits
```

The game loop runs many times each second. The game logic and saved values live in Python objects and files; `ui.py` displays them on screen. This is a desktop Pygame game, so it has no separate web backend.

## Team member 1 — Game flow and integration

**Main files:** `main.py`, `game.py`, `save_data.py`

### What these files do

- `main.py` is the small launch file. `if __name__ == "__main__":` makes the game start when this file is run. `Game().run()` creates the game and starts its loop.
- `game.py` connects the player, levels, enemies, objects, questions, sounds, and UI. The `Game` class keeps the current score, lives, stage, and screen state.
- `save_data.py` remembers the best score locally in `high_score.json`.

### Main functions to explain

- `Game.__init__()` starts Pygame and prepares the window, clock, sound, and game state.
- `Game.reset_stage()` sets up a fresh run: score, lives, first stage, questions, and other counters.
- `Game.run()` repeats the game loop: handle input, update the game, draw the screen, and keep the frame rate steady.
- `Game.handle_events()` reacts to keys such as Enter, arrows, Space, P, E, and R.
- `Game.update()` moves characters and objects and checks what they touch. It pauses updates during menus, quizzes, and score cards.
- `Game.draw()` draws the current world and chooses which screen or overlay should be visible.
- `Game.add_score(points)` adds points and updates the saved best score if the current score beats it.
- `Game.lose_life()` removes a life after damage and starts game over when no lives remain.
- `Game.check_stage_exit()` checks whether the player has met the conditions to finish a world.
- `Game.continue_after_stage_summary()` moves to the next world after the player reads the recap.
- `load_best_score()` reads the saved score; `save_best_score(score)` writes it.

### Simple viva explanation

“`main.py` starts the game. The `Game` class coordinates the other modules. Its loop handles input, updates the game, and draws each frame. The save module stores the best score in a local JSON file.”

## Team member 2 — Player and animation

**Main files:** `player.py`, `sprites.py`

### What these files do

- `player.py` controls the mouse character's position, movement, jumping, gravity, collision, and drawing.
- `sprites.py` loads the character animation images and draws them at the right size and direction.

### Main functions to explain

- `Player.__init__(x, y)` creates the player's collision rectangle and movement state.
- `Player.update(keys, platforms)` reads movement keys, moves the player, applies gravity, handles jumping, and checks platform collisions.
- `Player.draw(surface, hit_cooldown=0)` draws the player sprite on the game surface.
- `load_frames(character, animation)` loads the images for an animation, such as idle or walk. A cache avoids loading the same frames repeatedly.
- `draw_frame(surface, frame, anchor_rect, height, facing_right=True)` scales and draws one frame while keeping the character's feet aligned.

### Simple viva explanation

“The player has a rectangle used for collision and a sprite used for appearance. `update()` changes the rectangle; `draw()` displays the animation. Gravity changes vertical speed, and the platform checks decide when the player lands.”

## Team member 3 — Enemies, bullets, and boss

**Main file:** `enemy.py`  
**Connection to the main game:** enemy and bullet collisions are handled in `game.py`.

### What this file does

It defines bullets, regular enemies, and the boss. Enemies patrol within their limits, can jump or shoot, and can collide with the player. The boss reuses enemy behavior and adds health and stronger behavior.

### Main classes and functions to explain

- `Bullet.__init__()`, `Bullet.update()`, and `Bullet.draw()` create, move, and display an enemy projectile.
- `Enemy.__init__()` sets up an enemy's position and movement limits.
- `Enemy.update()` moves the enemy and updates its movement timers.
- `Enemy.ready_to_shoot()` checks whether its shooting timer has finished.
- `Enemy.shoot(player_rect)` creates a bullet aimed toward the player.
- `Enemy.check_collision(player_rect)` checks whether the enemy touches the player.
- `Enemy.draw(surface)` displays the enemy sprite.
- `Boss(Enemy)` means the boss inherits useful behavior from `Enemy`.
- `Boss.update()` changes boss behavior, including its stronger behavior when its health is low.
- `Boss.draw(surface)` displays the boss and its health information.

### Simple viva explanation

“`Enemy` is a reusable blueprint for cats. `Boss` inherits from it, so it can reuse movement and drawing while adding health and stronger attacks. The main `Game` code checks hits and updates score or lives.”

## Team member 4 — Game objects and visual effects

**Main files:** `objects.py`, `effects.py`

### What these files do

- `objects.py` defines the things placed in a level: platforms, coins, power-ups, hazards, moving platforms, bonus cheese, and player shots.
- `effects.py` creates small particles for visual feedback, such as a burst when something happens.

### Main classes and functions to explain

- `Platform` stores a platform rectangle and draws it.
- `Coin` stores whether it has been collected and draws the coin.
- `PowerUp` stores its type and collected state, then draws the matching item.
- `Hazard` represents a dangerous object in the level.
- `MovingPlatform.update()` changes the platform's position; `draw()` displays it.
- `CheeseDrop.update()` moves bonus cheese after an enemy is defeated; `draw()` displays it.
- `PlayerShot.update()` moves a shot; `draw()` displays it.
- `Particle.update(dt)` updates one particle's position and lifetime; `draw(surface)` draws it.
- `ParticleSystem.burst(...)` creates a group of particles; `update(dt)` and `draw(surface)` manage the group.

### Simple viva explanation

“Each object class keeps the data and drawing behavior for one kind of game item. The game checks collisions with these objects. `ParticleSystem` adds short visual effects without changing the main character sprites.”

## Team member 5 — Stages, Python learning, interface, and settings

**Main files:** `levels.py`, `ui.py`, `settings.py`, `python_challenges.py`, `python_concepts.py`, `sound_effects.py`

### What these files do

- `levels.py` has one `build_stage_...()` function for each of the five worlds. Each function returns that world's platforms, coins, enemies, and other objects.
- `ui.py` draws the start screen, world map, HUD, Python lessons and quizzes, stage recap, pause screen, and win/game-over screens.
- `settings.py` keeps values that the team may want to tune, such as lives, quiz length, world width, score rewards, and enemy speed.
- `python_challenges.py` stores the question banks, choices, correct answers, hints, and explanations for the worlds.
- `python_concepts.py` stores short lessons shown by Python Coach.
- `sound_effects.py` creates and plays game sounds and handles mute.

### Main functions to explain

- `build_stage_one()` through `build_stage_five()` create the five world layouts.
- `UI.draw_hud()` displays score, lives, and current game information.
- `UI.draw_python_challenge()` displays a question and its choices.
- `UI.draw_stage_summary()` displays the score and learning recap after a world.
- `UI.draw_game_over()` and `UI.draw_win()` display the final result and learning summary.
- Values such as `MAX_LIVES` and `QUIZ_QUESTIONS_PER_WORLD` in `settings.py` let the team change game tuning in one place.
- `PYTHON_CHALLENGES` and `PYTHON_LESSONS` are dictionaries: named keys connect each world or topic to its questions or lesson text.
- `SoundEffects.toggle_mute()` switches sound on or off; methods such as `play_coin()` play a particular effect.

### Simple viva explanation

“The level builders create the world data, the UI draws that data for the player, and the question and lesson files provide the Python learning content. Shared settings make common game values easier to change.”

## Python ideas used in the project

| Python idea | Easy example from JumpByte |
| --- | --- |
| Variable | `score` remembers the current points. |
| Condition (`if`) | The game checks whether a coin is collected or lives reached zero. |
| Loop | The game loop keeps updating and drawing; `for` loops check lists of coins or enemies. |
| List | A stage stores many coins, enemies, and platforms in lists. |
| Tuple | A player start or respawn position can be stored as `(x, y)`. |
| Dictionary | A stage or quiz question uses named keys such as `"coins"` or `"answer"`. |
| Function | `load_best_score()` performs a specific task. |
| Class and object | `Player` is a class; the player in a running game is an object. |
| Inheritance | `Boss` inherits behavior from `Enemy`. |
| Module | Importing `Player` from `player.py` lets another file use that code. |

## Quick viva questions

**Why split the game into files?**  
Each file has a related job, so the team can find and explain parts more easily.

**What is the difference between `update()` and `draw()`?**  
`update()` changes game data, such as position or score. `draw()` paints the current data on the screen.

**How do two quiz questions get selected?**  
`game.py` selects questions from that world's bank in `python_challenges.py` and avoids selecting the same question twice in one gate.

**How does a correct answer affect the game?**  
The game records the correct answer and topic, adds score, and displays the explanation. After both explanations, it can show the stage recap when the exit conditions are met.

**Where can we change the starting lives?**  
Change `MAX_LIVES` in the easy settings section of `settings.py`.

**What does “backend” mean in this project?**  
There is no separate server backend. The game's Python state stores score, lives, quiz results, and learned topics; `ui.py` displays that information.

## Before the viva

Each member should open their assigned file, point to the functions listed here, and explain them in their own words. Be honest about which parts were shared or AI-assisted, and do not claim code that you did not work on or understand.
