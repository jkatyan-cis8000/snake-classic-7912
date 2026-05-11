import curses
import time

from ..config import DIFFICULTIES
from ..service import GameService
from ..types import Difficulty, Direction, Food, GameState, Snake


class GameRunner:
    def __init__(self, difficulty: Difficulty):
        self.service = GameService(difficulty)
        self.stdscr = None
        self.difficulty = difficulty

    def run(self) -> None:
        curses.wrapper(self._main_loop)

    def cleanup(self) -> None:
        if self.stdscr:
            curses.nocbreak()
            self.stdscr.keypad(False)
            curses.echo()
            curses.endwin()

    def _main_loop(self, stdscr) -> None:
        self.stdscr = stdscr
        self._setup_curses()
        self.service.spawn_food()
        self.service.spawn_food()

        while self.service.get_state() == GameState.RUNNING:
            self._process_input()
            self._update_game()
            self._render()
            time.sleep(self.service.speed / 1000.0)

    def _setup_curses(self) -> None:
        curses.curs_set(0)
        self.stdscr.nodelay(True)
        self.stdscr.timeout(100)

    def _process_input(self) -> None:
        key = self.stdscr.getch()
        direction_map = {
            ord('w'): Direction.UP,
            ord('s'): Direction.DOWN,
            ord('a'): Direction.LEFT,
            ord('d'): Direction.RIGHT,
            curses.KEY_UP: Direction.UP,
            curses.KEY_DOWN: Direction.DOWN,
            curses.KEY_LEFT: Direction.LEFT,
            curses.KEY_RIGHT: Direction.RIGHT,
        }
        if key in direction_map:
            self.service.snake.direction = direction_map[key]

    def _update_game(self) -> None:
        if not self.service.move_snake():
            self.service.state = GameState.GAME_OVER
            return
        if self.service.check_collision():
            self.service.state = GameState.GAME_OVER
            return
        head = self.service.snake.body[0]
        if head.row == self.service.food.position.row and head.col == self.service.food.position.col:
            self.service.eat_food()

    def _render(self) -> None:
        self.stdscr.clear()
        self._draw_board()
        self._draw_snake()
        self._draw_food()
        self._draw_score()
        self.stdscr.refresh()

    def _draw_board(self) -> None:
        for i in range(-1, 21):
            self.stdscr.addch(0, i + 1, '-')
            self.stdscr.addch(21, i + 1, '-')
        for i in range(22):
            self.stdscr.addch(i, 0, '|')
            self.stdscr.addch(i, 22, '|')

    def _draw_snake(self) -> None:
        for i, pos in enumerate(self.service.snake.body):
            self.stdscr.addch(pos.row + 1, pos.col + 1, 'O' if i == 0 else 'o')

    def _draw_food(self) -> None:
        pos = self.service.food.position
        self.stdscr.addch(pos.row + 1, pos.col + 1, '*')

    def _draw_score(self) -> None:
        self.stdscr.addstr(23, 2, f'Score: {self.service.score}')
