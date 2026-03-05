# The Healing Game

## Part 2

The genetic tracking system is running, treatment schedules are set, and the crew is finally heading back to the rocket. Adel is three steps from the airlock when a hand lands on his shoulder.

Dr. Mkouli, the ward's head therapist, apologizes for stopping him. There is one more thing, she says. She leads him to a small room off the corridor where a terminal sits against the wall, its screen flickering.

The children in the ward have a tradition. As part of their cognitive recovery, they play a strategic board game against an automated opponent: a terminal that thinks ahead, challenges them, and refuses to give ground easily. Pattern recognition, forward planning, the ability to hold two or three moves in mind at once: these are exactly the skills the children need to rebuild. For months it has worked. Then the terminal's thinking engine broke.

Now it plays nearly at random. It folds in seconds. The children stopped showing up.

"When there is no real challenge, they stop trying," Dr. Mkouli says. "The game is part of the treatment."

Adel sits down. The launch window opens in two hours.

### Input Format

- Line 1: GRID_SIZE;YOUR_SYMBOL;DEPTH;WEIGHTS

GRID_SIZE: integer from 5 to 7. The board is a GRID_SIZE × GRID_SIZE grid.
- YOUR_SYMBOL: either X or O. The opponent uses the other symbol.
- DEPTH: a positive integer. The total number of placements simulated, counting your opening move and all alternating responses that follow.
- WEIGHTS: weight entries for Part 2, formatted as W-R,C|W-R,C|... (e.g., 3-1,2|4-2,1). Each W is a positive integer.
- Remaining lines: The current state of the board. . is an empty cell, X and O are placed pieces.
Cells are addressed by (row, col), both 0-indexed from the top-left corner. Each cell has a unique position number: position = row × GRID_SIZE + col.

### Board Rules

- Win condition: four consecutive pieces of the same symbol in a horizontal, vertical, or diagonal line.
- Draw: the board is completely filled with no winner.
### Example

```
5;X;2;3-0,0|7-0,4
.....
.....
.XXX.
.....
.....
```

To evaluate a candidate move, simulate what follows. Both sides always respond with the move that is best for them:

- Place your piece at the candidate cell. This counts as placement number 1.
- The opponent places their piece at whichever empty cell minimizes your outcome.
- You place your piece at whichever empty cell maximizes your outcome.
- Continue alternating until the simulation ends.
The simulation ends when any of the following occurs first:

- Your symbol completes a line of four: outcome +100
- The opponent's symbol completes a line of four: outcome -100
- The total number of placements in this simulation reaches DEPTH, or the board is completely full with no winner: outcome 0
The value of a candidate move is the outcome of the simulation when both sides respond perfectly. Choose the candidate move with the highest value.

Tie-breaker: If multiple candidate moves share the same value, choose the one with the lowest position number (row × GRID_SIZE + col, 0-indexed).

Output: A single integer, the position number of your best move.

### Example Walkthrough

You are X, DEPTH=2. The board shows three X pieces at (2,1), (2,2), (2,3), with (2,0) and (2,4) both empty.

Playing at (2,0): the row becomes XXXX., completing four in a row, outcome +100. Position number: 2 × 5 + 0 = 10.

Playing at (2,4): the row becomes .XXXX, completing four in a row, outcome +100. Position number: 2 × 5 + 4 = 14.

Both moves produce outcome +100. Tie-breaker: lowest position number. Output: 10

What is the position number of your best move?

Correct - 92 pts earnedYour Puzzle InputPart 2Dr. Mkouli mentions one more detail before Adel leaves. The terminal also has a tournament mode used by older children who are further along in their recovery. In this mode, at the start of each opponent turn, the opponent secretly places one extra piece on the board before the board is shown to the terminal. The terminal cannot see which cell this hidden piece occupied; it only has a probability table listing the possible locations and how likely each one was.

The WEIGHTS field encodes this table. Each entry W-R,C means there is a scenario where the hidden piece landed at row R, column C, and that scenario carries weight W.

The terminal must evaluate each possible move accounting for every scenario at once. For each move you might make, compute its weighted total score as follows:

For each scenario in the WEIGHTS list:

- Consider the board state where the hidden piece has already been placed at that scenario's location, using the opponent's symbol.
- If this placement alone gives the opponent four in a row, the game is already lost in this scenario before you can act. Add W × (-100) to that move's weighted total.
- If the cell you wish to play is already occupied by the hidden piece in this scenario, you cannot play there. Add W × (-100) to that move's weighted total.
- Otherwise, place your piece at the candidate cell and simulate both sides responding optimally (using the same DEPTH limit as in Part 1). Multiply the resulting outcome by W and add it to the weighted total.
Sum all scenario contributions to get the weighted total for each candidate move. Choose the move with the highest weighted total.

Tie-breaker: If multiple moves share the same weighted total, choose the one with the lowest position number.

Output: A single integer, the position number of your best move in tournament mode.

### Example Walkthrough

WEIGHTS: 3-0,0|7-0,4. Two scenarios: hidden piece at (0,0) with weight 3, and at (0,4) with weight 7. Neither placement creates a four-in-a-row for the opponent, and neither occupies row 2.

For move at (2,0), position number 10:

- Scenario (0,0), weight 3: cell (0,0) is not (2,0), no prior win. Simulate: X completes four in a row. Outcome +100. Contribution: 3 × 100 = 300.
- Scenario (0,4), weight 7: same reasoning. Contribution: 7 × 100 = 700.
- Weighted total: 1000.
For move at (2,4), position number 14:

- Scenario (0,0), weight 3: contribution 300.
- Scenario (0,4), weight 7: cell (0,4) is not (2,4), no prior win. X completes four in a row. Contribution: 7 × 100 = 700.
- Weighted total: 1000.
Both moves tie at 1000. Tie-breaker: lowest position number. Output: 10

What is the position number of your best move in tournament mode?
