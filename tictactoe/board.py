SIZE = 3

# все выигрышные линии: строки, столбцы и две диагонали
LINES = [[(r, c) for c in range(SIZE)] for r in range(SIZE)]
LINES += [[(r, c) for r in range(SIZE)] for c in range(SIZE)]
LINES.append([(i, i) for i in range(SIZE)])
LINES.append([(i, SIZE - 1 - i) for i in range(SIZE)])


class InvalidMoveError(Exception):
    pass


class Board:
    """Игровое поле 3x3. Пустая клетка хранится как None."""

    def __init__(self, cells=None):
        if cells is None:
            cells = [[None] * SIZE for _ in range(SIZE)]
        self.cells = [list(row) for row in cells]

    def get(self, row, col):
        return self.cells[row][col]

    def place(self, row, col, symbol):
        if not (0 <= row < SIZE and 0 <= col < SIZE):
            raise InvalidMoveError("Координаты вне поля")
        if self.cells[row][col] is not None:
            raise InvalidMoveError("Клетка уже занята")
        self.cells[row][col] = symbol

    def empty_cells(self):
        return [
            (r, c)
            for r in range(SIZE)
            for c in range(SIZE)
            if self.cells[r][c] is None
        ]

    def is_full(self):
        return not self.empty_cells()

    def winner(self):
        for line in LINES:
            symbols = {self.cells[r][c] for r, c in line}
            if len(symbols) == 1 and None not in symbols:
                return symbols.pop()
        return None

    def copy(self):
        return Board(self.cells)

    def __str__(self):
        rows = []
        for row in self.cells:
            rows.append(" | ".join(cell or " " for cell in row))
        return "\n---------\n".join(rows)
