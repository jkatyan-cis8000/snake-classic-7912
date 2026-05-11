import curses

from ..types import Direction, Snake, Food, GameState


class GameUI:
    def __init__(self) -> None:
        self._stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self._stdscr.nodelay(True)
        self._stdscr.keypad(True)

    def render(self, snake: Snake, food: Food, score: int, state: GameState) -> None:
        self._stdscr.clear()

        for pos in snake.body:
            self._stdscr.addch(pos.row, pos.col, "O")

        self._stdscr.addch(food.position.row, food.position.col, "F")

        self._stdscr.addstr(0, 0, f"Score: {score}")

        if state == GameState.GAME_OVER:
            self._stdscr.addstr(snake.body[0].row, snake.body[0].col - 5, "GAME OVER")

        self._stdscr.refresh()

    def handle_input(self) -> Direction | None:
        key = self._stdscr.getch()
        if key == curses.KEY_UP:
            return Direction.UP
        elif key == curses.KEY_DOWN:
            return Direction.DOWN
        elif key == curses.KEY_LEFT:
            return Direction.LEFT
        elif key == curses.KEY_RIGHT:
            return Direction.RIGHT
        return None

    def display_score(self, score: int) -> None:
        self._stdscr.addstr(0, 0, f"Score: {score}")
        self._stdscr.refresh()

    def game_over(self, score: int) -> None:
        self._stdscr.addstr(10, 10, f"GAME OVER")
        self._stdscr.addstr(11, 10, f"Final Score: {score}")
        self._stdscr.refresh()
        self._stdscr.nodelay(False)
        self._stdscr.getch()

    def cleanup(self) -> None:
        curses.nocbreak()
        self._stdscr.keypad(False)
        curses.echo()
        curses.endwin()
