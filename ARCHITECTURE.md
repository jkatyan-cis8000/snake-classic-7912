# ARCHITECTURE.md

Written by team-lead before spawning teammates. This is the shared blueprint —
teammates read it to understand what they are building and how their module fits.

## Module Structure

- **src/types/__init__.py**: Type definitions - Direction, Position, Snake, Food, GameState, Difficulty
- **src/config/__init__.py**: Game configuration - BOARD_SIZE, DIFFICULTIES dict
- **src/service/__init__.py**: GameService class - move_snake, check_collision, eat_food, update_game_state
- **src/ui/__init__.py**: GameUI class - render, handle_input, display_score, game_over
- **src/runtime/__init__.py**: GameRunner class - main loop, initialize, run, cleanup

## Interfaces

### Types (src/types/__init__.py)
- `Direction` enum: UP, DOWN, LEFT, RIGHT
- `Position` dataclass: row, col (integers)
- `Snake` dataclass: body (list of Position), direction
- `Food` dataclass: position (Position)
- `GameState` enum: RUNNING, GAME_OVER, PAUSED
- `Difficulty` enum: EASY, MEDIUM, HARD, INSANE

### Config (src/config/__init__.py)
- `BOARD_SIZE = 20`: Grid dimensions
- `DIFFICULTIES = { ... }`: Maps difficulty to speed (lower = faster)
  - EASY: 200ms, MEDIUM: 150ms, HARD: 100ms, INSANE: 60ms

### Service (src/service/__init__.py)
- `GameService` class:
  - `__init__(difficulty: Difficulty)` - Initialize with speed setting
  - `move_snake() -> bool` - Move forward, return True if valid
  - `eat_food() -> None` - Grow snake and spawn new food
  - `check_collision() -> bool` - Check self-boundary collision
  - `spawn_food() -> None` - Generate food at random position
  - `get_snake() -> Snake` - Return current snake state
  - `get_food() -> Food` - Return current food position
  - `get_score() -> int` - Food count
  - `get_state() -> GameState` - Current game state

### UI (src/ui/__init__.py)
- `GameUI` class:
  - `render(snake: Snake, food: Food, score: int, state: GameState) -> None`
  - `handle_input() -> Direction | None` - Parse user input
  - `display_score(score: int) -> None` - Show score
  - `game_over(score: int) -> None` - Display game over screen

### Runtime (src/runtime/__init__.py)
- `GameRunner` class:
  - `__init__(difficulty: Difficulty)` - Create service + ui
  - `run() -> None` - Main game loop with timing
  - `cleanup() -> None` - Reset curses

## Shared Data Structures

All types defined in src/types are the canonical definitions. No validation happens after parsing at boundaries.

## External Dependencies

- Python standard library only (curses for UI, enum, dataclasses, time)
