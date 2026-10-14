import uuid

from tictactoe.board import Board
from tictactoe.bot import Bot

PLAYER = "X"
BOT = "O"

IN_PROGRESS = "in_progress"
PLAYER_WON = "player_won"
BOT_WON = "bot_won"
DRAW = "draw"


class GameFinishedError(Exception):
    pass


class Game:
    """Партия пользователя против программы. Пользователь ходит первым."""

    def __init__(self, game_id=None, board=None, bot=None):
        self.id = game_id or uuid.uuid4().hex
        self.board = board or Board()
        self.bot = bot or Bot(BOT)
        self.status = self._calc_status()

    def make_move(self, row, col):
        """Ход пользователя. Возвращает ответный ход программы или None."""
        if self.status != IN_PROGRESS:
            raise GameFinishedError("Игра уже закончена")

        self.board.place(row, col, PLAYER)
        self.status = self._calc_status()
        if self.status != IN_PROGRESS:
            return None

        bot_move = self.bot.choose_move(self.board)
        self.board.place(*bot_move, BOT)
        self.status = self._calc_status()
        return bot_move

    def _calc_status(self):
        winner = self.board.winner()
        if winner == PLAYER:
            return PLAYER_WON
        if winner == BOT:
            return BOT_WON
        if self.board.is_full():
            return DRAW
        return IN_PROGRESS
