# The Healing Game

## Part 1

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
