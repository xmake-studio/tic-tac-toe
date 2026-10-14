import requests

BASE_URL = "http://localhost:8008"


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
