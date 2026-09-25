"""List the 20 ways to win on a 4x4 board.

A winning group contains four (row, column) coordinates. Indices start at zero.
For example, ((3, 0), (3, 1), (3, 2), (3, 3)) identifies the bottom row.
These coordinates describe where matching marks would form a win; they do not
describe the order in which players must place their marks.

WIN_GROUPS is built once when this module is imported and reused for every board.
The groups are tuples so they cannot be accidentally changed during evaluation.
"""

# Each pair identifies one cell; each group identifies four cells to match.
WinningGroup = tuple[tuple[int, int], ...]


def _horizontal_groups() -> list[WinningGroup]:
    """Build one group for each of the four complete rows."""
    winning_groups: list[WinningGroup] = []

    for row_index in range(4):
        row_coordinates = []
        for column_index in range(4):
            row_coordinates.append((row_index, column_index))
        winning_groups.append(tuple(row_coordinates))

    return winning_groups


def _vertical_groups() -> list[WinningGroup]:
    """Build one group for each of the four complete columns."""
    winning_groups: list[WinningGroup] = []

    for column_index in range(4):
        column_coordinates = []
        for row_index in range(4):
            column_coordinates.append((row_index, column_index))
        winning_groups.append(tuple(column_coordinates))

    return winning_groups


def _diagonal_groups() -> list[WinningGroup]:
    """Return the two diagonals that cross all four rows and columns."""
    return [
        ((0, 0), (1, 1), (2, 2), (3, 3)),
        ((0, 3), (1, 2), (2, 1), (3, 0)),
    ]


def _corner_groups() -> list[WinningGroup]:
    """Return the single group containing all four outer corners."""
    return [
        ((0, 0), (0, 3), (3, 0), (3, 3)),
    ]


def _box_groups() -> list[WinningGroup]:
    """Build the nine adjacent 2x2 boxes, including overlapping boxes."""
    winning_groups: list[WinningGroup] = []

    # A box's top-left cell cannot be in the last row or last column.
    for top_row in range(3):
        for left_column in range(3):
            box_coordinates = (
                (top_row, left_column),
                (top_row, left_column + 1),
                (top_row + 1, left_column),
                (top_row + 1, left_column + 1),
            )
            winning_groups.append(box_coordinates)

    return winning_groups


def _build_winning_groups() -> tuple[WinningGroup, ...]:
    """Combine the five rule families into one immutable collection."""
    winning_groups: list[WinningGroup] = []
    winning_groups.extend(_horizontal_groups())
    winning_groups.extend(_vertical_groups())
    winning_groups.extend(_diagonal_groups())
    winning_groups.extend(_corner_groups())
    winning_groups.extend(_box_groups())
    return tuple(winning_groups)


# Build once when this module is imported; reuse for every board.
WIN_GROUPS = _build_winning_groups()
