# 4x4 Tic-Tac-Toe solver

Python 3.10+ is required. No external dependencies or installation are needed.
Run the following commands from this repository's root directory. On Windows,
you can substitute `py` for `python`.

## Run the demo

```powershell
python demo.py
```

The demo prints an ongoing game, a mixed-case X win, a full-board draw, and a
handled error for two winners. Dots represent empty cells in the printed output.

## Run the tests

```powershell
python -m unittest discover -s test -v
```

The tests use Python's built-in `unittest`. They cover all 20 winning groups for
both players and both cases, missing or opposing marks within each group,
mixed-case wins, draws, remaining moves, conflicting winners, malformed input,
input preservation, and repeated calls after a board changes. Winning examples
are specified independently of the implementation's rule generators.

## Solution

The idea for the chosen solution is that since we have a predefined 4x4 board with
rules, we can:

1. Generate all possible winning coordinate groups once when `rules.py` is imported
2. Normalize and validate the supplied board each time it is checked
3. Iterate through win groupings to see if the same player occupies each coordinate
4. If they do, that is how they won the game

Groupings for 4x4 come out to: four rows, four columns, two diagonals, all four outer corners,
and nine adjacent 2x2 boxes. We keep checking after a win to reject a board where
both players win. Multiple winning groups for the same player are allowed.

### Adding a new win condition

The matching logic in `checkWinner` is separate from the shapes defined in
`src/rules.py`. To add a shape, write a helper that returns its coordinate groups,
then include those groups in `_build_winning_groups()`. For example, an L-shaped
win could include `((0, 0), (1, 0), (2, 0), (2, 1))`. Its helper would also need to
include every position and rotation allowed by the new rule.

`checkWinner` already walks every coordinate in each group, so its matching loop
does not need to change for another shape or a different number of matching
cells. Each group must be nonempty and contain distinct, valid board coordinates.
Add independent tests for the new shape, its boundaries, near misses, and wins
that conflict with another player's win. Rules based on move history or mixed
player patterns would require additional evaluation logic.

### Supporting a larger board

The current implementation deliberately supports only 4x4. Extending it would
require changes to validation and group generation:

1. Define the board size and line length separately. On a 5x5 board, does a line
   require five matching marks, or any four consecutive marks?
2. Update `normalize_board` to validate the supported dimensions instead of
   requiring four rows and four cells per row.
3. Pass those dimensions and the required line length to the rule generators.
   Replace fixed ranges and coordinates. Four-in-a-row on a larger board needs
   every horizontal, vertical, and diagonal segment of four cells, including
   diagonals that do not start at a corner. Full-length lines on a square board
   need complete rows, columns, and the two full diagonals.
4. Define how the other rules scale: corners could remain the four outermost
   cells, and boxes could remain adjacent 2x2 squares at every valid position.
5. Build groups for the selected configuration instead of using the single
   fixed `WIN_GROUPS` collection. Have the checker use those groups, and add tests
   for each supported size and its boundary cases.

The cell-matching loop and empty-cell scan can be reused. The work is in describing
the rules for the new size and supplying the correct groups, rather than adding
size-specific branches to the winner check. Larger boards also increase group
storage and checking time; the current O(1) claim applies only to fixed 4x4 boards.

### Input and API

Input must be a list of four lists, each containing four cells. Use `None` or `""`
for an empty cell and `X`, `x`, `O`, or `o` for player marks. Empty strings become
`None` in a normalized copy; the original board is unchanged. Whitespace remains
invalid. Other values and malformed
dimensions raise `ValueError`.

```python
from src import TicTacToe

board = [
    ["x", "X", "x", "X"],
    ["O", None, None, None],
    [None, None, None, None],
    [None, None, None, None],
]

game = TicTacToe()
print(game.checkWinner(board))   # X
print(game.anyMovesLeft(board))  # True
print(game.isGameOver(board))    # True
```

| Original API | Result |
| --- | --- |
| `checkWinner(board)` | `"X"`, `"O"`, or `None`; raises for two winners |
| `anyMovesLeft(board)` | Whether any cell is empty, even after a win |
| `isGameOver(board)` | Whether a winner exists or the board is full; raises for two winners |

All three methods validate input. The solver does not enforce turn order, move
counts, gravity, or whether play continued after a win. It supports only 4x4
boards. Runtime and storage are O(1) for this fixed size.

Explicit loops keep the checks readable. Separating rule definitions makes them
easier to review, at the cost of ensuring no winning group is omitted. Independent
test examples cover that risk. Each public method normalizes its own input so it
can run independently; `isGameOver` may normalize twice, an acceptable small cost
for this 16-cell board.

## Files

- `src/board.py`: input validation and normalization.
- `src/rules.py`: winning coordinate groups.
- `src/tic_tac_toe.py`: the original three-method API.
- `test/test_tic_tac_toe.py`: automated tests.
- `demo.py`: executable usage examples.
- [Detailed documentation](docs/README.md).
- [Exercise prompt](docs/PROMPT.md) and [planning notes](docs/PLANNING.md).
- [AI conversation transcript](docs/TRANSCRIPT.md).
