# chall14

Challenge solved in Python.

## Files
- `solve.py`: solution script.
- `input.txt`: challenge input.
- `part1_statement.md`: Part 1 statement.
- `part2_statement.md`: Part 2 statement.

## Solution
The grid is a functional graph: each cell has exactly one outgoing next cell (from arrow direction).

## Part 1
Movement without wrapping (items can leave grid).

Implementation:
- Build `nxt` array (`-1` means exit).
- Compute metadata with DFS states:
  - distance to exit,
  - distance to cycle,
  - cycle length.
- Build binary lifting jump table for fast `T`-step transition.
- For each item start:
  - if exits within `T`, ignore,
  - otherwise jump exactly `T` steps and add final index contribution.

## Part 2
Movement with wrapping (torus), so no `-1` exits.

Implementation:
- Build wrapped `nxt`.
- Build doubling tables:
  - `jumps[k][u]`: node after `2^k` steps,
  - `sums[k][u]`: sum of visited node indices over those `2^k` steps.
- For each item, decompose `T` in binary and aggregate `sums`.
- Return total modulo `1_000_000_009`.

## Complexity
- Preprocessing: `O(R*C*log T)`.
- Each item query: `O(log T)`.
- Fits large `T` and many items efficiently.

## Run
```bash
python solve.py --part 1
python solve.py --part 2
```

## Source
https://microcode.microclub.info/challenges/83e2c1cd-66c6-46a3-b74a-2f7f199d72b5
