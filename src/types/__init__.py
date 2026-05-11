from enum import Enum
from dataclasses import dataclass


class Direction(Enum):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"


@dataclass
class Position:
    row: int
    col: int


@dataclass
class Snake:
    body: list[Position]
    direction: Direction


@dataclass
class Food:
    position: Position


class GameState(Enum):
    RUNNING = "RUNNING"
    GAME_OVER = "GAME_OVER"
    PAUSED = "PAUSED"


class Difficulty(Enum):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"
    INSANE = "INSANE"
