import random

from tictactoe.board import Board
from tictactoe.bot import Bot


def test_bot_takes_winning_move():
    board = Board([
        ["O", "O", None],
        ["X", "X", None],
        ["X", None, None],
    ])
    assert Bot("O").choose_move(board) == (0, 2)


def test_bot_does_not_change_board_while_thinking():
    board = Board([["O", "O", None], ["X", "X", None], [None] * 3])
    Bot("O").choose_move(board)
    assert board.get(0, 2) is None


def test_bot_random_move_when_cannot_win():
    board = Board()
    board.place(1, 1, "X")
    move = Bot("O", rng=random.Random(1)).choose_move(board)
    assert move in board.empty_cells()


def test_bot_uses_rng():
    class FakeRng:
        def choice(self, cells):
            return cells[-1]

    board = Board()
    assert Bot("O", rng=FakeRng()).choose_move(board) == (2, 2)
