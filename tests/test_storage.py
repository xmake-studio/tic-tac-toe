import mongomock
import pytest

from tictactoe.board import Board
from tictactoe.game import PLAYER_WON, Game
from tictactoe.storage import MongoStorage


@pytest.fixture
def storage():
    return MongoStorage(mongomock.MongoClient().db.games)


def test_save_and_get(storage):
    game = Game()
    game.make_move(1, 1)
    storage.save(game)

    loaded = storage.get(game.id)
    assert loaded.id == game.id
    assert loaded.board.cells == game.board.cells
    assert loaded.status == game.status


def test_save_twice_updates_game(storage):
    game = Game()
    storage.save(game)
    game.make_move(0, 0)
    storage.save(game)

    assert storage.collection.count_documents({}) == 1
    assert storage.get(game.id).board.get(0, 0) == "X"


def test_status_restored(storage):
    game = Game(board=Board([["X", "X", "X"], ["O", "O", None], [None] * 3]))
    storage.save(game)
    assert storage.get(game.id).status == PLAYER_WON


def test_get_unknown(storage):
    assert storage.get("unknown") is None
