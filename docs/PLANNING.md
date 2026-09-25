# Python

# Assumptions
- two players only
- 4x4 -> ignoring generic for this exercise, would be easy to extend if needed
- input is 2d list

# Solution 1
- Define class TicTacToe
 - checkWinner(board) -> bool
  - iterates through board within an OUTER loop, start at top left when we find a used tile (X or O) we perform win check for all possibilities in an INNER loop - TRUE if found 
  - print winner?
  - OPTIMIZATION: We do not need to run check for every possible win on every tile. Start at top left and if index falls in category below, we perform only tthe necessary checks
   - Vertical -> only check for top row going downard
   - Horizontal -> only check for left most column going right
   - Diagonal -> only check for top two  corners in respective direction
   - Box -> DO NOT check right most column and bbottom most row
   - Corner -> only check at top left
 - anyMovesLeft (board) -> bool
  - if there is a spot not used, return True
 - isGameOver(board) -> bool
  - composed of above functions to build conditional for output

O(1) where n is number of pieces on the board since we must visit every piece on the board

# Solution 2
Define same class structure but since we are assuming 4x4 and this is a game witth clear rules that means we can hardcode every possible way to win. This turns the problem into a pattern match problem.

EX.
Horizontal 

XXXX
NNNN
NNNN
NNNN

or 

NNNN
XXXX
NNNN
NNNN

- same class structure
- generate all possibble win combinations (tuple)
 - helper function for each so it is extensible + function that calls each to generate all
- walk each pattern for x and then for o
 - iterate through each possilbe win combination and check if they all belong to the same player... if they do winner if not next patter

Same O(1) but clever...


# Tradeoffs

- Option 1
 - Harder to extend with new win condition
 - Soupy logic - a lot of condititonals -> harder to edit in future
 - Harder to unit test?
 - More intuitive

- Option 2
 - Harder to read


# Edge Cases/Errors:
- Invalid board? -> validate in seperate function
 - if p1 has 4 moves and p2 has 2 moves this is invalid
  - genericize if diff > 2?
  - we do not enforce who goes first
 - observe something other than x or o
- Case sensittivity
- 2 winners
- empty board is no winner
- full board with no winner is over
- a player can win in more than one way