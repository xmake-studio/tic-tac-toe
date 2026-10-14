from tictactoe.game import Game
from tictactoe.storage import MemoryStorage


def test_save_and_get():
    storage = MemoryStorage()
    game = Game()
    storage.save(game)
    assert storage.get(game.id) is game


def test_get_unknown():
    assert MemoryStorage().get("unknown") is None
