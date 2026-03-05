# The Galactic Records

## Part 1

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
