"""Check winners and game status without changing the caller's board."""

from .board import Board, normalize_board
from .rules import WIN_GROUPS


class TicTacToe:
    """Evaluate a 4x4 board using the three methods from the exercise prompt.

    Marks may be uppercase or lowercase. None and "" represent empty cells.
    Each call examines the supplied board; no board is stored on the object.
    Turn order, move counts, gravity, and previous moves are not checked.
    """

    def checkWinner(self, board: Board) -> str | None:
        """Return uppercase "X" or "O" for a winner, or None for no winner.

        Check winning pattern to see if same player occupies each spo. One player
        may complete several groups. Raise ValueError if both players win,
        or if the board has invalid dimensions or cell values.
        """
        normalized_board = normalize_board(board)
        winner = None

        for winning_group in WIN_GROUPS:
            reference_row, reference_column = winning_group[0]
            candidate_player = normalized_board[reference_row][reference_column]

            # if first index of winning group is None, game can not be won this way
            if candidate_player is None:
                continue

            all_cells_match = True
            for row_index, column_index in winning_group:
                cell = normalized_board[row_index][column_index]
                if cell != candidate_player:
                    all_cells_match = False
                    break

            # if all cells do not belong to the same player, not winning match
            if not all_cells_match:
                continue

            if winner is not None and winner != candidate_player:
                raise ValueError("Board contains winning groups for both players.")

            winner = candidate_player
            # Keep checking: another group might give the other player a win.

        return winner

    def anyMovesLeft(self, board: Board) -> bool:
        """Return True if any cell is empty, otherwise return False.

        Empty cells still count after a win. This method does not check for
        winners; use isGameOver to determine whether play has ended.
        Raise ValueError for invalid dimensions or cell values.
        """
        normalized_board = normalize_board(board)

        for row in normalized_board:
            for cell in row:
                if cell is None:
                    return True

        return False

    def isGameOver(self, board: Board) -> bool:
        """Return True when a player has won or the board is full.

        A full board without a winner is a draw. Raise ValueError for invalid
        dimensions, invalid cell values, or wins by both players.
        """
        winner = self.checkWinner(board)
        if winner is not None:
            return True

        if self.anyMovesLeft(board):
            return False

        return True
