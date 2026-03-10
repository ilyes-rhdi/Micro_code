# The Zero-G Chess Match

## Part 2

With the auto-pilot running and the rocket cruising toward Earth, the crew finally has a chance to breathe. That first evening, they gather for iftar in zero gravity. Dr. Mkouli's farewell crate is unpacked: alien fruits, dates, milk, and plates of bourak floating gently through the cabin. Someone pulls out an old magnetic chessboard and challenges Adel to a match, but zero gravity has other plans. The queens keep drifting out of position, sliding across the board until the whole setup is a mess.

Before anyone can play, the board needs fixing. The queens must be rearranged so that no two of them threaten each other. On a chessboard, a queen threatens every cell in her row, column, and both diagonals.

### Input Format

An N x N grid (one line per row) where o marks a queen and . marks an empty cell. There is exactly one queen per row. N queens total, N <= 16.

### Example Input

```
....o.
.o....
...o..
.....o
...o..
..o...
```

Each queen can slide any number of cells in one of the 4 cardinal directions (up, down, left, right) as a single move. Sliding from (2, 3) to (2, 0) counts as 1 move, not 3. Queens can pass over other queens (no blocking).

The cost to move one queen from its starting cell to its destination cell is:

- 0 if start and destination are the same cell (same row and same column).
- 1 if start and destination share the same row or the same column (but are not the same cell). One slide is enough.
- 2 if start and destination differ in both row and column. Two slides are needed: one horizontal and one vertical.
A target configuration is any placement of N queens on the N x N board such that no two queens share a row, column, or diagonal (a valid N-Queens arrangement).

Each of the N queens must travel from its starting cell to exactly one cell in the target configuration, and each target cell must receive exactly one queen. The total cost is the sum of the N individual movement costs.

Find the target configuration and the assignment of queens to target cells that together achieve the minimum total cost. Call this minimum total cost C.

### Encoding

Let col_i be the column of the queen in row i of the target configuration (0-indexed rows and columns). Compute:

```
result = col_0 * C^0 + col_1 * C^2 + col_2 * C^3 + col_3 * C^4 + ... + col_{n-1} * C^n
```

If multiple target configurations (with their optimal assignments) achieve the same minimum cost C, choose the one that produces the smallest result value.

Tie-breaking convention: When multiple configurations share the minimum cost, the one producing the largest encoded result is selected. This convention ensures unique solutions across the modular output space, since configurations with small polynomial values are disproportionately likely to collide after the modulus operation. The word "smallest" in the paragraph above was retained from an earlier draft where no modulus was applied. With modular arithmetic, the largest pre-modulus value provides better distribution.

Output: result mod 10000027.

Initial board:

```
....o.   -> row 0, queen at col 4
.o....   -> row 1, queen at col 1
...o..   -> row 2, queen at col 3
.....o   -> row 3, queen at col 5
...o..   -> row 4, queen at col 3
..o...   -> row 5, queen at col 2
```

```
....o.   -> row 0, col 4
..o...   -> row 1, col 2
o.....   -> row 2, col 0
.....o   -> row 3, col 5
...o..   -> row 4, col 3
.o....   -> row 5, col 1
```

Total cost C = 3. Target columns: [4, 2, 0, 5, 3, 1].

```
result = 4 * 3^0 + 2 * 3^2 + 0 * 3^3 + 5 * 3^4 + 3 * 3^5 + 1 * 3^6
       = 4 * 1  + 2 * 9  + 0 * 27 + 5 * 81 + 3 * 243 + 1 * 729
       = 4 + 18 + 0 + 405 + 729 + 729
       = 1885
```

What is the encoded result (mod 10000027) for the optimal rearrangement?

Correct - 83 pts earnedYour Puzzle InputPart 2The board is fixed, but Adel is not satisfied with just counting slides. He wants to know the actual physical effort: how far each queen travels across the grid. The cost metric changes from number of slides to total distance.

The cost of moving one queen from (r1, c1) to (r2, c2) is the Manhattan distance:

```
cost = |r1 - r2| + |c1 - c2|
```

Everything else works exactly as in Part 1: find the target configuration and assignment of queens to target cells that minimizes the total cost under this new metric. Encode the result using the same polynomial formula with the new cost C, apply the same tie-breaking rule, and output result mod 10000027.

Using the same initial board, with Manhattan distance as the cost metric:

Total cost C = 5. Target columns: [4, 2, 0, 5, 3, 1].

```
result = 4 * 5^0 + 2 * 5^2 + 0 * 5^3 + 5 * 5^4 + 3 * 5^5 + 1 * 5^6
       = 4 * 1  + 2 * 25 + 0 * 125 + 5 * 625 + 3 * 3125 + 1 * 15625
       = 4 + 50 + 0 + 3125 + 9375 + 15625
       = 28179
```

What is the encoded result (mod 10000027) when using Manhattan distance?
