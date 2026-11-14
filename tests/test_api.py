import threading

import mongomock
import pytest
import requests
from werkzeug.serving import make_server

import server as server_module
from server import create_app
from tictactoe.board import Board
from tictactoe.game import Game
from tictactoe.storage import MongoStorage

BASE_URL = None


@pytest.fixture(scope="module", autouse=True)
def storage():
    global BASE_URL
    storage = MongoStorage(mongomock.MongoClient().tictactoe.games)
    # порт 0: ОС выдаёт свободный порт, тесты не мешают запущенному серверу
    httpd = make_server("127.0.0.1", 0, create_app(storage))
    BASE_URL = f"http://127.0.0.1:{httpd.server_port}"
    thread = threading.Thread(target=httpd.serve_forever)
    thread.start()
    yield storage
    httpd.shutdown()
    thread.join()


def create_game():
    response = requests.post(f"{BASE_URL}/games")
    assert response.status_code == 201
    return response.json()


def move(game_id, row, col):
    return requests.post(
        f"{BASE_URL}/games/{game_id}/moves", json={"row": row, "col": col}
    )


def test_create_game():
    game = create_game()
    assert game["id"]
    assert game["status"] == "in_progress"
    assert game["board"] == [[None] * 3 for _ in range(3)]


def test_get_game():
    game = create_game()
    response = requests.get(f"{BASE_URL}/games/{game['id']}")
    assert response.status_code == 200
    assert response.json() == game


def test_get_unknown_game():
    response = requests.get(f"{BASE_URL}/games/unknown")
    assert response.status_code == 404
    assert "error" in response.json()


def test_make_move():
    game = create_game()
    response = move(game["id"], 1, 1)
    assert response.status_code == 200

    data = response.json()
    bot = data["bot_move"]
    assert data["board"][1][1] == "X"
    assert data["board"][bot["row"]][bot["col"]] == "O"
    assert data["status"] == "in_progress"


def test_move_is_saved():
    game = create_game()
    data = move(game["id"], 0, 0).json()
    response = requests.get(f"{BASE_URL}/games/{game['id']}")
    assert response.json()["board"] == data["board"]


def test_move_to_occupied_cell():
    game = create_game()
    move(game["id"], 1, 1)
    response = move(game["id"], 1, 1)
    assert response.status_code == 400
    assert "error" in response.json()


def test_move_out_of_board():
    game = create_game()
    assert move(game["id"], 3, 0).status_code == 400


def test_move_with_bad_body():
    game = create_game()
    url = f"{BASE_URL}/games/{game['id']}/moves"
    assert requests.post(url, json={"row": 1}).status_code == 400
    assert requests.post(url, json={"row": "a", "col": 1}).status_code == 400
    assert requests.post(url, data="not json").status_code == 400


def test_move_in_unknown_game():
    assert move("unknown", 0, 0).status_code == 404


def test_play_until_finish():
    game = create_game()
    data = game
    while data["status"] == "in_progress":
        row, col = next(
            (r, c)
            for r in range(3)
            for c in range(3)
            if data["board"][r][c] is None
        )
        data = move(game["id"], row, col).json()

    assert data["status"] in ("player_won", "bot_won", "draw")
    response = move(game["id"], 0, 0)
    assert response.status_code == 409


def test_player_wins_without_bot_move(storage):
    game = Game(board=Board([["X", "X", None], ["O", "O", None], [None] * 3]))
    storage.save(game)

    response = move(game.id, 0, 2)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "player_won"
    assert data["bot_move"] is None


def test_default_storage_is_mongo(monkeypatch):
    monkeypatch.setattr(server_module, "MongoClient", mongomock.MongoClient)
    client = create_app().test_client()

    game_id = client.post("/games").get_json()["id"]
    assert client.get(f"/games/{game_id}").status_code == 200
