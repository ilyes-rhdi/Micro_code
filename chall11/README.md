# chall11

Challenge solved in Python.

## Files
- `solve.py`: solution script.
- `input.txt`: challenge input.
- `part1_statement.md`: Part 1 statement.
- `part2_statement.md`: Part 2 statement.

## Solution
The input is an `N x N` board with one queen per row (`N <= 16`).
The solver enumerates all valid N-Queens target layouts, then computes minimum relocation cost from the initial board to each target using assignment.

### Core steps
- Parse initial queen column per row.
- Generate all N-Queens placements with bitmask DFS:
  - `cols_used`, `diag1`, `diag2` masks.
- For each valid target placement:
  - Build cost matrix `cost[src_row][target_row]`.
  - Compute minimum perfect matching with Hungarian algorithm.

### Cost model
- Part 1:
  - `0` if queen already exact,
  - `1` if same row or same column,
  - `2` otherwise.
- Part 2:
  - Manhattan move cost: `abs(src_r - dst_r) + abs(src_c - dst_c)`.

After minimal cost is found, encode final arrangement as required by challenge:
- `sum(col_i * C^exp_i)` with challenge-specific exponent pattern,
- output modulo `10_000_027`.
- If multiple layouts have same minimum cost, keep smallest pre-mod encoded value.

## Complexity
- N-Queens generation is exponential (feasible for `N <= 16`).
- For each valid layout, Hungarian runs in `O(N^3)`.

## Run
```bash
python solve.py --part 1
python solve.py --part 2
```

## Source
https://microcode.microclub.info/challenges/b407c98f-aae5-41a3-ab27-09a11c9ad620
