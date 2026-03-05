# The Galactic Records

## Part 2

The crew is boarding the rocket, ready to depart, when the LMKOULYIN stop them. Again. Word has spread fast: the genetic tracking system, the restored therapy terminal, the translation infrastructure that made it all possible. Now every hospital on the planet wants a piece of it. But this time, the scope is far bigger: patient records across all facilities are stored in a single massive character matrix, and each patient's file is identified by a hidden keyword embedded somewhere in the grid.

The system must locate the exact coordinate path that spells each patient's identifier under strict lookup rules, then extract related medical data using spatial proximity. Lmkouli explains that the matrix is enormous, hundreds of rows and columns, and the lookup must be precise. A wrong match could link a patient to the wrong treatment file. Adel rolls up his sleeves. One more system, and then they leave.

### Input Format

- Line 1: TARGET: T where T is a signed integer.
- Line 2: WORD: W where W is a string of characters.
- Line 3: MATRIX:
- Remaining lines: The character matrix (e.g., 600 rows by 600 columns).
Grid coordinates are 0-indexed. Let ROWS and COLS denote the matrix dimensions.

### Example

```
TARGET: 1
WORD: AB
MATRIX:
xAxxB
xxBxA
AxBxx
```

Find the sequence of coordinates [(R1,C1), (R2,C2), ..., (RL,CL)] in the matrix that spells WORD character by character, subject to:

- Column progression: Each character must be found strictly to the right of the previous one: C1 < C2 < ... < CL. Rows are unrestricted.
- Target checksum: The sum of row-minus-column differences must equal TARGET:


(R1 - C1) + (R2 - C2) + ... + (RL - CL) = TARGET
There is exactly one valid sequence satisfying both rules.

Compute the positional hash using 1-based row and column indices:

```
Hash = (R1+1)*(C1+1) + (R2+1)*(C2+1) + ... + (RL+1)*(CL+1)
```

Output: The positional hash as a single integer.

### Example Walkthrough

WORD = AB, TARGET = 1. Find 'A' then 'B' with increasing columns and checksum = 1.

All 'A' positions: (0,1), (1,4), (2,0). All 'B' positions: (0,4), (1,2), (2,2).

Unique valid sequence: A at (2,0), B at (1,2).

Converting to 1-based: A at (3,1), B at (2,3).

Hash = (3x1) + (2x3) = 3 + 6 = 9

What is the positional hash of the valid word path?

Correct - 91 pts earnedYour Puzzle InputPart 2The lookup system works, and the hospitals are thrilled, but Lmkouli raises one more requirement. For each patient record found, the system must also pull the medical file of the nearest matching patient in the database for cross-referencing. The grid wraps around (the database is stored on a toroidal memory structure), and each match yields neighboring data entries.

Keep the exact coordinates from Part 1. For each coordinate (Ri, Ci) containing character X:

- Find the nearest twin: Search the entire matrix for the closest cell that also contains character X (excluding the original cell).
- Toroidal distance: The grid wraps around. The distance between (r1, c1) and (r2, c2) is:


D = min(|r1-r2|, ROWS-|r1-r2|) + min(|c1-c2|, COLS-|c1-c2|)
- Border constraint: The twin cannot be on column 0 or column COLS-1 (it needs both left and right neighbors).
Clarification on border constraint: The column restriction (not column 0 or COLS-1) described above applies to the original coordinate from the Part 1 solution path, not to the twin candidate. Any cell in the matrix may serve as a valid twin regardless of its column position. The restriction ensures that the original position has extractable neighbors, which is guaranteed by the input construction.

- Tie-breaker: If multiple twins share the minimum distance, pick the one with the lowest row index. If still tied, pick the lowest column index.
- Extraction: Once the nearest valid twin is found at (r, c), extract its left neighbor (r, c-1) and its right neighbor (r, c+1).
Concatenate these extracted character pairs for every character in WORD. If the word has L characters, the payload string has 2L characters.

Compute the weighted ASCII sum:

```
Value = sum of ASCII(char_k) * k    for k = 1 to 2L
```

Output: The final value as a single integer.

### Example Walkthrough

Coordinates from Part 1: A at (2,0), B at (1,2).

Character 'A' at (2,0): Find nearest twin 'A' (not on col 0 or col 4).

- Other A's: (0,1), (1,4).
- (0,1): col 1, valid. Toroidal dist = min(|2-0|,3-2) + min(|0-1|,5-1) = min(2,1) + min(1,4) = 1+1 = 2.
- (1,4): col 4 = COLS-1, invalid (border constraint).
- Nearest valid twin: (0,1), distance 2.
- Extract: left (0,0)='x', right (0,2)='x'. Payload so far: xx.
Character 'B' at (1,2): Find nearest twin 'B' (not on col 0 or col 4).

- Other B's: (0,4), (2,2).
- (0,4): col 4 = COLS-1, invalid.
- (2,2): col 2, valid. Toroidal dist = min(|1-2|,3-1) + min(|2-2|,5-0) = min(1,2) + min(0,5) = 1+0 = 1.
- Nearest valid twin: (2,2), distance 1.
- Extract: left (2,1)='x', right (2,3)='x'. Payload: xxxx.
Weighted ASCII sum: (120x1) + (120x2) + (120x3) + (120x4) = 120 x 10 = 1200

What is the weighted ASCII sum of the extracted payload?
