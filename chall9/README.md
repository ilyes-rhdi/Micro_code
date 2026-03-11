# chall9

Challenge solved in Python.

## Files
- `solve.py`: solution script.
- `input.txt`: challenge input.
- `part1_statement.md`: Part 1 statement.
- `part2_statement.md`: Part 2 statement.

## Solution
### Part 1
Goal: find the unique path that spells `WORD`, with strictly increasing columns and checksum:
`sum(Ri - Ci) = TARGET`.

Approach used in `solve.py`:
- Pre-index matrix positions by character and by column.
- Build DP layers over word characters.
- For each step and each column, store reachable checksum values as a bitset.
- Transition is column-increasing only, and each chosen row contributes `(r - c)` to checksum.
- At the last layer, pick the column that contains the target checksum bit.
- Backtrack through layers to reconstruct the exact coordinate path.

Then compute:
- `hash = sum((r+1)*(c+1))` over reconstructed path.

### Part 2
Using the Part 1 path:
- For each path cell `(r0,c0)` with character `X`, scan all other `X` cells.
- Use toroidal Manhattan distance:
  `min(|dr|, ROWS-|dr|) + min(|dc|, COLS-|dc|)`.
- Choose minimum distance, then row/col lexicographic tie-break.
- Extract left and right neighbors of that twin and append to payload.
- Compute weighted ASCII sum:
  `sum(ord(payload[k]) * (k+1))`.

## Complexity
- Part 1 DP: bitset-based transitions over columns and word length (optimized for large matrices).
- Part 2: linear scan over positions of each needed character from the Part 1 path.

## Run
```bash
python solve.py --part 1
python solve.py --part 2
```

## Source
https://microcode.microclub.info/challenges/478d0375-edc3-43f1-bdce-998e2b35202f
