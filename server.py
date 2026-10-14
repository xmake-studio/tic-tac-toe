from flask import Flask, jsonify, request

from tictactoe.board import InvalidMoveError
from tictactoe.game import Game, GameFinishedError
from tictactoe.storage import MemoryStorage

PORT = 8008


def error(message, code):
    return jsonify({"error": message}), code


def create_app(storage=None):
    app = Flask(__name__)
    app.json.ensure_ascii = False
    storage = storage or MemoryStorage()

    @app.post("/games")
    def create_game():
        game = Game()
        storage.save(game)
        return jsonify(game.to_dict()), 201

    @app.get("/games/<game_id>")
    def get_game(game_id):
        game = storage.get(game_id)
        if game is None:
            return error("Игра не найдена", 404)
        return jsonify(game.to_dict())

    @app.post("/games/<game_id>/moves")
    def make_move(game_id):
        game = storage.get(game_id)
        if game is None:
            return error("Игра не найдена", 404)

        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return error("Тело запроса должно быть JSON-объектом", 400)
        row, col = data.get("row"), data.get("col")
        if type(row) is not int or type(col) is not int:
            return error("Нужно передать целые row и col", 400)

        try:
            bot_move = game.make_move(row, col)
        except InvalidMoveError as e:
            return error(str(e), 400)
        except GameFinishedError as e:
            return error(str(e), 409)
        storage.save(game)

        result = game.to_dict()
        result["bot_move"] = None
        if bot_move:
            result["bot_move"] = {"row": bot_move[0], "col": bot_move[1]}
        return jsonify(result)

    return app


if __name__ == "__main__":
    create_app().run(port=PORT)
