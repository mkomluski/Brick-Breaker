# Brick Breaker

A classic Brick Breaker / Arkanoid-style arcade game built from scratch in Python using tkinter. Features procedurally generated levels, four brick types, a power-up system, and persistent save/high score data.

![Status](https://img.shields.io/badge/status-in%20development-yellow)
![Python](https://img.shields.io/badge/python-3.12-blue)

---

## Table of Contents

- [Features](#features)
- [Screenshots](#screenshots)
- [Download & Play](#download--play)
- [Running from Source](#running-from-source)
- [How to Play](#how-to-play)
- [Project Structure](#project-structure)
- [Technical Overview](#technical-overview)
- [Roadmap](#roadmap)
- [Building the Executable](#building-the-executable)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **Mouse-controlled paddle** with directional ball control — where the ball hits the paddle determines its new trajectory
- **Four brick types:**
  - Normal — destroyed in one hit
  - Multi-hit — takes 2–3 hits, shows progressive crack damage
  - Indestructible — permanent obstacle, never destroyed
  - Exploding — destroys all adjacent bricks in a chain reaction on destruction
- **Procedurally generated levels** — infinite progression, with brick variety and density scaling by level number
- **Power-up system** — power-ups drop from destroyed bricks, fall down the screen, and are caught with the paddle
- **Lives and scoring system**, with a persistent local high score
- **Save & resume** — exit mid-run and continue later from the same level and score
- **Full screen flow** — start screen, level transition screen, and game over screen

## Download & Play

No Python installation required.

1. Go to the [Releases](../../releases) page
2. Download `BrickBreaker.exe` from the latest release
3. Run it — that's it

## Running from Source

If you'd rather run it from source (e.g. to modify the code):

**Requirements:**

- Python 3.12+ (tkinter is included with standard Python installs on Windows)

**Steps:**

```
git clone https://github.com/mkomluski/Brick-Breaker.git
cd Brick-Breaker
python main.py
```

No external dependencies are required to run the game — it uses only the Python standard library (`tkinter`, `random`, `os`, `collections`, `time`).

## How to Play

- Move your **mouse** to control the paddle
- Keep the ball in play by bouncing it off the paddle
- Destroy bricks to score points and clear the level
- Catch falling power-ups with the paddle for temporary or permanent effects
- You have a limited number of lives — losing all of them ends the run
- Clear all destructible bricks to advance to the next level

## Project Structure

```
brick_breaker/
├── main.py                # Entry point — creates Game and calls run()
├── game.py                # Core game loop, state management, collision handling
├── entities/
│   ├── paddle.py          # Paddle class
│   ├── ball.py             # Ball class
│   ├── brick.py            # Brick class
│   └── powerup.py          # PowerUp class
├── levels/
│   ├── level_data.py       # LevelData — layout container + procedural generation
│   └── level_manager.py    # LevelManager — tracks and advances levels
├── assets/
│   ├── images/              # Power-up icons and other sprites
│   └── sounds/               # (planned) sound effects
├── data/
│   └── highscore.txt        # Persisted local high score
└── utils/
    ├── collisions.py        # Pure collision-detection geometry functions
    ├── constants.py          # All game constants (sizes, speeds, colors)
    ├── enums.py               # BrickType, BrickState, GameState, PowerUpType
    ├── screens.py             # Start/transition/game-over screen drawing
    └── storage.py             # High score and save-file read/write
```

## Technical Overview

Built with an object-oriented architecture that separates game logic, entity behavior, and presentation:

- **`Game`** owns the game loop (`tkinter.after()`-driven), current state, and all cross-entity logic like collision detection and explosion chains
- **Entity classes** (`Paddle`, `Ball`, `Brick`, `PowerUp`) each manage only their own state and drawing — they don't know about each other
- **`utils/`** holds pure, state-free functions: geometry, file I/O, and screen drawing — kept separate from anything that touches live game state
- **Enums** (`BrickType`, `BrickState`, `GameState`, `PowerUpType`) are used throughout instead of raw strings/booleans, to keep state transitions explicit and prevent contradictory flag combinations
- **Levels are procedurally generated** rather than hardcoded, with brick variety gated by level number and constraints (like a cap on indestructible bricks per row) to keep every generated layout playable
- **Collision detection** is written from scratch — AABB overlap checks plus normalized center-offset calculations to determine bounce direction

Full design rationale and decision history is documented in `DECISIONS.md` in the repo.

## Roadmap

**Currently implemented (Phase 6 — Power-ups, in progress):**

- ✅ Extra Life
- ✅ Wide Paddle

**Planned:**

- ⬜ Hammer Ball — one-time destruction of an indestructible brick
- ⬜ Fireball — ball passes through bricks without bouncing
- ⬜ Multi-ball — splits into multiple simultaneous balls
- ⬜ Sound effects
- ⬜ Brick shatter / particle animations
- ⬜ Visual polish pass (colors, paddle/ball styling)
- ⬜ Per-power-up icon art (currently using shared placeholder art)
- ⬜ Difficulty scaling refinements across levels

## Building the Executable

This project uses [PyInstaller](https://pyinstaller.org/) to build a standalone Windows executable.

```
pip install pyinstaller
pyinstaller --onefile --windowed --add-data "assets;assets" main.py
```

The built `.exe` will be in the `dist/` folder. The `--add-data` flag is required to bundle the `assets/` folder into the executable; without it, power-up icons will fail to load at runtime.

## Contributing

Suggestions and bug reports are welcome via [Issues](../../issues).

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
