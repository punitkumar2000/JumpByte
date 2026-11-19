# JumpByte: Demo and Viva Guide

## Short demo walkthrough

1. Start the game. Press **Enter** to open the journey map, then press **Enter** again to begin Green Meadow.
2. Show movement and jumping with **A/D** or the arrow keys, and **Space/W/Up**. Collect a coin to show the score and Python Coach message.
3. Show a power-up. The yellow power-up boosts speed; the blue power-up enables **F** to fire. **P** pauses the game and **M** mutes sound effects.
4. Collect every coin in the world. At the exit, press **E** to open the Python gate. Answer two questions with **1**, **2**, or **3**. A wrong answer gives a hint; a correct answer shows an explanation. Press **Enter** after each explanation.
5. Show the world recap: score earned in that world, total score, and quiz result. Press **Enter** to continue. Repeat for the five worlds; in Skyforge Citadel, collect all coins, defeat the boss, and pass the quiz to reach the final recap.
6. After the final recap, the win screen shows worlds cleared, Python answers correct, and concepts learned. The game-over screen shows the same learning progress if lives run out.

If the demo time is short, demonstrate one coin, one Python Coach message, both questions in one gate, the world score recap, and the final boss using prepared screenshots or a saved demo run.

## Python concepts to explain

| Concept | Where it appears |
| --- | --- |
| Variables and conditionals | Score, lives, timers, and checks for collected items or collisions |
| Lists and loops | Stage lists of coins, enemies, platforms, hazards, and the loops that update/draw them |
| Tuples | Positions such as the checkpoint respawn coordinate `(x, y)` |
| Dictionaries | Stage data and Python lesson/challenge data stored under named keys |
| Classes and objects | `Player`, `Enemy`, `Coin`, `Platform`, and individual game objects |
| Inheritance | `Boss` extends `Enemy` and adds boss health/behavior |
| Modules and imports | Separate files keep game logic, levels, UI, effects, and sound organized |
| Game loop | `Game.run()` handles input, updates the world, draws frames, and limits frame rate |
| Collision detection | Pygame rectangles detect contact with platforms, coins, enemies, and hazards |
| File storage | `save_data.py` loads and saves the best score as JSON |

## Common viva questions

**Why use classes?**  
Classes group an object's data and behavior. For example, each `Coin` has a position and collected state, plus a method to draw it.

**How does the boss reuse enemy code?**  
`Boss` inherits from `Enemy`, so it can reuse movement and drawing behavior while adding health and stronger behavior.

**How does the player jump?**  
When a jump key is pressed while grounded, the player gets upward velocity. Gravity changes that velocity each frame, producing the jump arc.

**How does a Python challenge work?**  
Each world has a question bank in `python_challenges.py`. The game randomly selects two different questions for the gate. A wrong answer shows a hint; a correct answer shows its explanation before the next question. The game records how many questions were answered and which concepts appeared.

**How does the learning recap work?**
`game.py` tracks questions, concepts, worlds cleared, and score. `ui.py` displays those values after each world and on the final win/game-over screen. JumpByte is a local Pygame game, so this is game-state logic plus an on-screen UI, not a separate web backend.

**Where do we change the number of lives?**
Change `MAX_LIVES` in the **EASY GAME SETTINGS** section in `settings.py`. The game start and HUD both use that same value.

**Where is the best score saved?**  
`save_data.py` writes it to the local `high_score.json` file. That file is ignored by Git so each computer can keep its own score.

## Before presenting

- Run the game from the project folder and confirm it opens in a window.
- Keep this guide and the source code available for the viva.
- Credit downloaded or generated artwork according to its source and license; do not describe an asset as hand-drawn unless the team created it that way.
- Describe the team's real contributions accurately. The project README identifies the work as AI-assisted.
