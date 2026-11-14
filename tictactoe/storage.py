from tictactoe.board import Board
from tictactoe.game import Game


class MongoStorage:
    """Хранит игры в коллекции MongoDB. Статус считается заново по полю."""

    def __init__(self, collection):
        self.collection = collection

    def save(self, game):
        self.collection.replace_one(
            {"_id": game.id},
            {"_id": game.id, "board": game.board.cells},
            upsert=True,
        )

    def get(self, game_id):
        doc = self.collection.find_one({"_id": game_id})
        if doc is None:
            return None
        return Game(game_id=doc["_id"], board=Board(doc["board"]))
