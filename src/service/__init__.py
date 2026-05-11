from random import randint

from ..config import BOARD_SIZE, DIFFICULTIES
from ..types import Direction, Difficulty, Food, GameState, Position, Snake


class GameService:
    def __init__(self, difficulty: Difficulty):
        self.difficulty = difficulty
        self.speed = DIFFICULTIES[difficulty]
        self.snake = Snake(body=[Position(10, 10)], direction=Direction.RIGHT)
        self.food = Food(position=Position(5, 5))
        self.score = 0
        self.state = GameState.RUNNING

    def move_snake(self) -> bool:
        head = self.snake.body[0]
        new_head = Position(
            row=head.row + self._dir_delta_row(self.snake.direction),
            col=head.col + self._dir_delta_col(self.snake.direction),
        )
        if self._is_valid_position(new_head):
            self.snake.body.insert(0, new_head)
            return True
        return False

    def eat_food(self) -> None:
        self.score += 1
        self.spawn_food()

    def check_collision(self) -> bool:
        head = self.snake.body[0]
        if head.row < 0 or head.row >= BOARD_SIZE or head.col < 0 or head.col >= BOARD_SIZE:
            return True
        if head in self.snake.body[1:]:
            return True
        return False

    def spawn_food(self) -> None:
        while True:
            pos = Position(row=randint(0, BOARD_SIZE - 1), col=randint(0, BOARD_SIZE - 1))
            if pos not in self.snake.body:
                self.food.position = pos
                break

    def get_snake(self) -> Snake:
        return self.snake

    def get_food(self) -> Food:
        return self.food

    def get_score(self) -> int:
        return self.score

    def get_state(self) -> GameState:
        return self.state

    def _is_valid_position(self, pos: Position) -> bool:
        if pos.row < 0 or pos.row >= BOARD_SIZE or pos.col < 0 or pos.col >= BOARD_SIZE:
            return False
        if pos in self.snake.body[1:]:
            return False
        return True

    def _dir_delta_row(self, direction: Direction) -> int:
        if direction == Direction.UP:
            return -1
        if direction == Direction.DOWN:
            return 1
        return 0

    def _dir_delta_col(self, direction: Direction) -> int:
        if direction == Direction.LEFT:
            return -1
        if direction == Direction.RIGHT:
            return 1
        return 0
