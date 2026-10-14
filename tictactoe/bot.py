import random


class Bot:
    """Ход программы: выигрывает, если может, иначе ходит случайно."""

    def __init__(self, symbol, rng=None):
        self.symbol = symbol
        self.rng = rng or random.Random()

    def choose_move(self, board):
        empty = board.empty_cells()
        for row, col in empty:
            test_board = board.copy()
            test_board.place(row, col, self.symbol)
            if test_board.winner() == self.symbol:
                return row, col
        return self.rng.choice(empty)
