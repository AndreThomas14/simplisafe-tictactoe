"""Validate a 4x4 board and make a copy with uppercase player marks."""

# Each cell contains an X or O (either case), or None or "" for an empty cell.
Board = list[list[str | None]]


def normalize_board(board: Board) -> Board:
    """Return a validated copy so callers' cells are never changed.

    Accept X, x, O, o, None, and empty strings. Convert lowercase marks to
    uppercase and empty strings to None in the copy. Raise ValueError for
    any other cell or incorrect dimensions. Whitespace is not an empty cell.
    Turn order and the number of marks per player are not checked.
    """
    if not isinstance(board, list):
        raise ValueError("Board must be a list of exactly 4 rows.")
    if len(board) != 4:
        raise ValueError("Board must contain exactly 4 rows.")

    normalized_board: Board = []

    for row_index, row in enumerate(board):
        if not isinstance(row, list):
            raise ValueError(f"Row {row_index} must be a list of exactly 4 cells.")
        if len(row) != 4:
            raise ValueError(f"Row {row_index} must contain exactly 4 cells.")

        normalized_row: list[str | None] = []

        for column_index, cell in enumerate(row):
            if cell is None:
                normalized_row.append(None)
                continue

            if not isinstance(cell, str):
                raise ValueError(
                    f"Cell ({row_index}, {column_index}) must be X, x, O, o, None, or an empty string."
                )

            if cell == "":
                normalized_row.append(None)
                continue

            if cell not in ("X", "x", "O", "o"):
                raise ValueError(
                    f"Cell ({row_index}, {column_index}) must be X, x, O, o, None, or an empty string."
                )

            normalized_row.append(cell.upper())

        normalized_board.append(normalized_row)

    return normalized_board
