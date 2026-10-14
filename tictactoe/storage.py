class MemoryStorage:
    """Хранит игры в памяти процесса."""

    def __init__(self):
        self._games = {}

    def save(self, game):
        self._games[game.id] = game

    def get(self, game_id):
        return self._games.get(game_id)
