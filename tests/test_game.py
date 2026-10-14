import pytest

from tictactoe.board import Board, InvalidMoveError
from tictactoe.bot import Bot
from tictactoe.game import (
    BOT_WON, DRAW, IN_PROGRESS, PLAYER_WON, Game, GameFinishedError,
)


class FirstCellRng:
    def choice(self, cells):
        return cells[0]


def make_game(cells=None):
    return Game(board=Board(cells), bot=Bot("O", rng=FirstCellRng()))


def test_new_game():
    game = Game()
    assert game.status == IN_PROGRESS
    assert game.id
    assert len(game.board.empty_cells()) == 9


def test_game_ids_are_unique():
    assert Game().id != Game().id


def test_move_returns_bot_move():
    game = make_game()
    bot_move = game.make_move(1, 1)
    assert bot_move == (0, 0)
    assert game.board.get(1, 1) == "X"
    assert game.board.get(0, 0) == "O"
    assert game.status == IN_PROGRESS


def test_player_wins():
    game = make_game([
        ["X", "X", None],
        ["O", "O", None],
        [None, None, None],
    ])
    assert game.make_move(0, 2) is None
    assert game.status == PLAYER_WON


def test_bot_wins():
    game = make_game([
        ["X", "X", None],
        ["O", "O", None],
        ["X", None, None],
    ])
    assert game.make_move(2, 2) == (1, 2)
    assert game.status == BOT_WON


def test_draw_after_player_move():
    game = make_game([
        ["X", "O", "X"],
        ["X", "O", "O"],
        ["O", "X", None],
    ])
    assert game.make_move(2, 2) is None
    assert game.status == DRAW


def test_draw_after_bot_move():
    game = make_game([
        ["X", "O", "X"],
        ["X", "O", None],
        ["O", "X", None],
    ])
    assert game.make_move(1, 2) == (2, 2)
    assert game.status == DRAW


def test_move_after_finish():
    game = make_game([["X", "X", "X"], ["O", "O", None], [None] * 3])
    assert game.status == PLAYER_WON
    with pytest.raises(GameFinishedError):
        game.make_move(2, 2)


def test_to_dict():
    game = make_game()
    game.make_move(1, 1)
    data = game.to_dict()
    assert data["id"] == game.id
    assert data["status"] == IN_PROGRESS
    assert data["board"][1][1] == "X"
    assert data["board"][0][0] == "O"


def test_invalid_move_does_not_change_status():
    game = make_game()
    game.make_move(1, 1)
    with pytest.raises(InvalidMoveError):
        game.make_move(1, 1)
    assert game.status == IN_PROGRESS
