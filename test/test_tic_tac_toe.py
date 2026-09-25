"""Public API tests. Run from the repository root with unittest discovery."""

from copy import deepcopy
import unittest

from src import TicTacToe


# Independent examples of all 20 wins; do not derive expectations from src.rules.
# A # marks a cell in the winning group, and a . marks an empty cell.
WINNING_PATTERNS = {
    "row 0": ("####", "....", "....", "...."),
    "row 1": ("....", "####", "....", "...."),
    "row 2": ("....", "....", "####", "...."),
    "row 3": ("....", "....", "....", "####"),
    "column 0": ("#...", "#...", "#...", "#..."),
    "column 1": (".#..", ".#..", ".#..", ".#.."),
    "column 2": ("..#.", "..#.", "..#.", "..#."),
    "column 3": ("...#", "...#", "...#", "...#"),
    "main diagonal": ("#...", ".#..", "..#.", "...#"),
    "opposite diagonal": ("...#", "..#.", ".#..", "#..."),
    "corners": ("#..#", "....", "....", "#..#"),
    "box 0,0": ("##..", "##..", "....", "...."),
    "box 0,1": (".##.", ".##.", "....", "...."),
    "box 0,2": ("..##", "..##", "....", "...."),
    "box 1,0": ("....", "##..", "##..", "...."),
    "box 1,1": ("....", ".##.", ".##.", "...."),
    "box 1,2": ("....", "..##", "..##", "...."),
    "box 2,0": ("....", "....", "##..", "##.."),
    "box 2,1": ("....", "....", ".##.", ".##."),
    "box 2,2": ("....", "....", "..##", "..##"),
}


def board_from_rows(*rows: str) -> list[list[str | None]]:
    """Make readable test boards: dots become None; other characters stay intact."""
    board = []
    for row_text in rows:
        row = []
        for character in row_text:
            if character == ".":
                row.append(None)
            else:
                row.append(character)
        board.append(row)
    return board


class TicTacToeTests(unittest.TestCase):
    def setUp(self):
        self.game = TicTacToe()

    def test_every_winning_group_for_both_players_and_cases(self):
        for pattern_name, pattern_rows in WINNING_PATTERNS.items():
            for player in ("X", "O", "x", "o"):
                with self.subTest(pattern=pattern_name, player=player):
                    rows = []
                    for row_text in pattern_rows:
                        rows.append(row_text.replace("#", player))
                    board = board_from_rows(*rows)

                    self.assertEqual(self.game.checkWinner(board), player.upper())
                    self.assertTrue(self.game.anyMovesLeft(board))
                    self.assertTrue(self.game.isGameOver(board))

    def test_each_winning_group_needs_all_four_matching_marks(self):
        for pattern_name, pattern_rows in WINNING_PATTERNS.items():
            for player, opponent in (("X", "O"), ("O", "X")):
                rows = []
                for row_text in pattern_rows:
                    rows.append(row_text.replace("#", player))
                complete_board = board_from_rows(*rows)

                for row_index in range(4):
                    for column_index in range(4):
                        if complete_board[row_index][column_index] != player:
                            continue
                        for replacement in (None, "", opponent):
                            with self.subTest(
                                pattern=pattern_name, player=player,
                                row=row_index, column=column_index,
                                replacement=replacement,
                            ):
                                board = deepcopy(complete_board)
                                board[row_index][column_index] = replacement
                                self.assertIsNone(self.game.checkWinner(board))
                                self.assertTrue(self.game.anyMovesLeft(board))
                                self.assertFalse(self.game.isGameOver(board))

    def test_mixed_case_marks_belong_to_the_same_player(self):
        for row_text, winner in (("XxXx", "X"), ("oOoO", "O")):
            with self.subTest(winner=winner):
                board = board_from_rows(row_text, "....", "....", "....")
                self.assertEqual(self.game.checkWinner(board), winner)

    def test_empty_board(self):
        board = board_from_rows("....", "....", "....", "....")
        self.assertIsNone(self.game.checkWinner(board))
        self.assertTrue(self.game.anyMovesLeft(board))
        self.assertFalse(self.game.isGameOver(board))

    def test_full_board_without_winner_is_a_draw(self):
        board = board_from_rows("XXOO", "OOXX", "XXOO", "OOXX")
        self.assertIsNone(self.game.checkWinner(board))
        self.assertFalse(self.game.anyMovesLeft(board))
        self.assertTrue(self.game.isGameOver(board))

    def test_board_of_empty_strings_has_no_winner(self):
        board = [
            ["", "", "", ""],
            ["", "", "", ""],
            ["", "", "", ""],
            ["", "", "", ""],
        ]
        self.assertIsNone(self.game.checkWinner(board))
        self.assertTrue(self.game.anyMovesLeft(board))
        self.assertFalse(self.game.isGameOver(board))

    def test_empty_string_in_last_cell_keeps_game_open(self):
        board = board_from_rows("XXOO", "OOXX", "XXOO", "OOX.")
        board[3][3] = ""
        self.assertIsNone(self.game.checkWinner(board))
        self.assertTrue(self.game.anyMovesLeft(board))
        self.assertFalse(self.game.isGameOver(board))

    def test_mixed_empty_values_and_marks_preserve_input(self):
        board = [
            ["x", "X", "x", "X"],
            ["o", "", None, ""],
            [None, "", None, ""],
            ["", None, "", None],
        ]
        original_board = deepcopy(board)
        self.assertEqual(self.game.checkWinner(board), "X")
        self.assertEqual(board, original_board)
        self.assertTrue(self.game.anyMovesLeft(board))
        self.assertEqual(board, original_board)
        self.assertTrue(self.game.isGameOver(board))
        self.assertEqual(board, original_board)

    def test_last_cell_empty_is_still_a_move(self):
        board = board_from_rows("XXOO", "OOXX", "XXOO", "OOX.")
        self.assertIsNone(self.game.checkWinner(board))
        self.assertTrue(self.game.anyMovesLeft(board))
        self.assertFalse(self.game.isGameOver(board))

    def test_full_board_with_winner(self):
        board = board_from_rows("XXXX", "XXXX", "XXXX", "XXXX")
        self.assertEqual(self.game.checkWinner(board), "X")
        self.assertFalse(self.game.anyMovesLeft(board))
        self.assertTrue(self.game.isGameOver(board))

    def test_multiple_winning_groups_for_one_player(self):
        board = board_from_rows("XXXX", "X...", "X...", "X...")
        self.assertEqual(self.game.checkWinner(board), "X")
        self.assertTrue(self.game.isGameOver(board))

    def test_two_winners_raise_regardless_of_scan_order(self):
        for first_row, second_row in (("XXXX", "oooo"), ("OOOO", "xxxx")):
            board = board_from_rows(first_row, second_row, "....", "....")
            for method in (self.game.checkWinner, self.game.isGameOver):
                with self.subTest(first_row=first_row, method=method.__name__):
                    with self.assertRaisesRegex(ValueError, "both players"):
                        method(board)
            # This method only checks space, not conflicting winners.
            self.assertTrue(self.game.anyMovesLeft(board))

    def test_winner_outside_first_rule_family_is_not_missed(self):
        board = board_from_rows("XXXX", "....", ".OO.", ".OO.")
        with self.assertRaisesRegex(ValueError, "both players"):
            self.game.checkWinner(board)
        with self.assertRaisesRegex(ValueError, "both players"):
            self.game.isGameOver(board)

    def test_marks_outside_winning_group_do_not_cancel_win(self):
        board = board_from_rows("XXXX", "O...", ".O..", "....")
        self.assertEqual(self.game.checkWinner(board), "X")

    def test_move_counts_and_first_player_are_not_enforced(self):
        board = board_from_rows("OOO.", "....", "....", "....")
        self.assertIsNone(self.game.checkWinner(board))
        self.assertFalse(self.game.isGameOver(board))

    def test_all_methods_reject_invalid_dimensions(self):
        valid_board = board_from_rows("....", "....", "....", "....")
        invalid_boards = [
            None, "XXXX", {}, (), [],
            valid_board[:3], valid_board + [[None, None, None, None]],
            [None, valid_board[1], valid_board[2], valid_board[3]],
            ["XXXX", valid_board[1], valid_board[2], valid_board[3]],
            [tuple(valid_board[0]), valid_board[1], valid_board[2], valid_board[3]],
            [valid_board[0], valid_board[1], valid_board[2], [None] * 3],
            [valid_board[0], valid_board[1], valid_board[2], [None] * 5],
        ]
        for board in invalid_boards:
            for method in (self.game.checkWinner, self.game.anyMovesLeft, self.game.isGameOver):
                with self.subTest(board=board, method=method.__name__):
                    with self.assertRaises(ValueError):
                        method(board)

    def test_all_methods_reject_invalid_cells_even_after_a_win(self):
        for invalid_cell in (" ", "\t", "\n", "Z", "XX", " X", 0, 1, False, [], {}):
            board = board_from_rows("XXXX", "....", "....", "....")
            board[3][3] = invalid_cell
            for method in (self.game.checkWinner, self.game.anyMovesLeft, self.game.isGameOver):
                with self.subTest(cell=invalid_cell, method=method.__name__):
                    with self.assertRaises(ValueError):
                        method(board)

    def test_public_methods_do_not_modify_input(self):
        board = board_from_rows("xXxx", "o...", "....", "....")
        for method in (self.game.checkWinner, self.game.anyMovesLeft, self.game.isGameOver):
            with self.subTest(method=method.__name__):
                original_board = deepcopy(board)
                original_first_row = board[0]
                method(board)
                self.assertEqual(board, original_board)
                self.assertIs(board[0], original_first_row)

    def test_invalid_board_is_not_modified(self):
        board = board_from_rows("xxxx", "....", "....", "...?")
        original_board = deepcopy(board)
        with self.assertRaises(ValueError):
            self.game.checkWinner(board)
        self.assertEqual(board, original_board)

    def test_repeated_calls_observe_changes_to_input(self):
        board = board_from_rows("XXX.", "....", "....", "....")
        self.assertIsNone(self.game.checkWinner(board))
        board[0][3] = "x"
        self.assertEqual(self.game.checkWinner(board), "X")
        board[0][3] = None
        self.assertFalse(self.game.isGameOver(board))

    def test_either_player_can_open_in_any_cell(self):
        for player in ("X", "O"):
            for row_index in range(4):
                for column_index in range(4):
                    with self.subTest(player=player, row=row_index, column=column_index):
                        board = board_from_rows("....", "....", "....", "....")
                        board[row_index][column_index] = player
                        self.assertIsNone(self.game.checkWinner(board))
                        self.assertTrue(self.game.anyMovesLeft(board))
                        self.assertFalse(self.game.isGameOver(board))

    def test_game_can_progress_from_bottom_right_with_top_left_empty(self):
        board = board_from_rows("....", "....", "....", "....")
        moves = [
            (3, 3, "X"),
            (0, 1, "O"),
            (3, 2, "X"),
            (1, 0, "O"),
            (2, 3, "X"),
            (0, 2, "O"),
            (2, 2, "X"),
        ]
        for move_index, (row_index, column_index, player) in enumerate(moves):
            board[row_index][column_index] = player
            with self.subTest(move=move_index + 1):
                self.assertIsNone(board[0][0])
                self.assertTrue(self.game.anyMovesLeft(board))
                if move_index == len(moves) - 1:
                    self.assertEqual(self.game.checkWinner(board), "X")
                    self.assertTrue(self.game.isGameOver(board))
                else:
                    self.assertIsNone(self.game.checkWinner(board))
                    self.assertFalse(self.game.isGameOver(board))


if __name__ == "__main__":
    unittest.main()
