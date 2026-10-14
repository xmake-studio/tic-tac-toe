import pytest

from tictactoe.board import Board, InvalidMoveError


def test_new_board_is_empty():
    board = Board()
    assert len(board.empty_cells()) == 9
    assert not board.is_full()
    assert board.winner() is None


def test_place_and_get():
    board = Board()
    board.place(0, 2, "X")
    assert board.get(0, 2) == "X"
    assert (0, 2) not in board.empty_cells()


@pytest.mark.parametrize("row, col", [(-1, 0), (0, -1), (3, 0), (0, 3)])
def test_place_out_of_range(row, col):
    with pytest.raises(InvalidMoveError):
        Board().place(row, col, "X")


def test_place_on_occupied_cell():
    board = Board()
    board.place(1, 1, "X")
    with pytest.raises(InvalidMoveError):
        board.place(1, 1, "O")


@pytest.mark.parametrize("cells", [
    [["X", "X", "X"], [None] * 3, [None] * 3],
    [["O", None, None], ["O", None, None], ["O", None, None]],
    [["X", None, None], [None, "X", None], [None, None, "X"]],
    [[None, None, "O"], [None, "O", None], ["O", None, None]],
])
def test_winner(cells):
    symbol = next(c for row in cells for c in row if c)
    assert Board(cells).winner() == symbol


def test_full_board_without_winner():
    board = Board([
        ["X", "O", "X"],
        ["X", "O", "O"],
        ["O", "X", "X"],
    ])
    assert board.is_full()
    assert board.winner() is None


def test_copy_is_independent():
    board = Board()
    copy = board.copy()
    copy.place(0, 0, "X")
    assert board.get(0, 0) is None


def test_str():
    board = Board([["X", None, None], [None, "O", None], [None] * 3])
    lines = str(board).split("\n")
    assert lines[0] == "X |   |  "
    assert lines[2] == "  | O |  "
