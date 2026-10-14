from tictactoe.board import Board, InvalidMoveError
from tictactoe.game import IN_PROGRESS, Game, GameFinishedError


def demo_bot_wins():
    # у программы две "O" в ряд, она должна закрыть линию
    board = Board([
        ["X", "X", None],
        ["O", "O", None],
        ["X", None, None],
    ])
    game = Game(board=board)
    print("Ход программы:", game.make_move(2, 2))
    print(game.board)
    print("Статус:", game.status)


def demo_random_game():
    game = Game()
    print("Новая игра:", game.id)
    while game.status == IN_PROGRESS:
        row, col = game.board.empty_cells()[0]
        bot_move = game.make_move(row, col)
        print(f"Игрок: {(row, col)}, программа: {bot_move}")
    print(game.board)
    print("Итог:", game.status)

    try:
        game.make_move(0, 0)
    except GameFinishedError as e:
        print("Ошибка:", e)


def demo_errors():
    game = Game()
    game.make_move(1, 1)
    for row, col in [(1, 1), (5, 0)]:
        try:
            game.make_move(row, col)
        except InvalidMoveError as e:
            print(f"Ход {(row, col)}: {e}")


if __name__ == "__main__":
    demo_bot_wins()
    print()
    demo_random_game()
    print()
    demo_errors()
