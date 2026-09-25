"""Run from the repository root with: python demo.py."""

from src import TicTacToe
from src.board import Board


def show_example(title: str, board: Board) -> None:
    """Print a board and the result of each public method."""
    print(title)
    for row in board:
        display_cells = []
        for cell in row:
            if cell is None or cell == "":
                display_cells.append(".")
            else:
                display_cells.append(cell)
        print(" ".join(display_cells))

    game = TicTacToe()
    print("Winner:", game.checkWinner(board))
    print("Empty cells remain:", game.anyMovesLeft(board))
    print("Game over:", game.isGameOver(board))
    print()


def main() -> None:
    """Demonstrate an ongoing game, a mixed-case win, a draw, and an error."""
    show_example("Game in progress", [
        ["X", "O", "", None],
        [None, "x", None, None],
        [None, None, None, None],
        [None, None, None, None],
    ])

    show_example("X wins with mixed-case marks", [
        ["X", "x", "X", "x"],
        ["O", None, "o", None],
        [None, None, None, None],
        [None, None, None, None],
    ])

    show_example("Full board: draw", [
        ["X", "X", "O", "O"],
        ["O", "O", "X", "X"],
        ["X", "X", "O", "O"],
        ["O", "O", "X", "X"],
    ])

    conflicting_board = [
        ["X", "X", "X", "X"],
        ["O", "O", "O", "O"],
        [None, None, None, None],
        [None, None, None, None],
    ]
    print("Invalid position: both players win")
    try:
        TicTacToe().checkWinner(conflicting_board)
    except ValueError as error:
        print("Error:", error)


if __name__ == "__main__":
    main()
