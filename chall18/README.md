# chall18

Challenge solved in Python.

## Files
- `solve.py`: solution script (part 1 and part 2).
- `input.txt`: challenge input.
- `part1_statement.md`: Part 1 statement.
- `part2_statement.md`: Part 2 statement.

## Solution
This is a DP optimization problem with a quadratic cost, solved using the Convex Hull Trick (CHT).

Let `prefix[i]` be the prefix sum of values. The cost to end a group at `i` is:
```
(prefix[i] + offset)^2 + min_j (dp_prev[j] + prefix[j]^2 - 2 * prefix[j] * (prefix[i] + offset))
```
So each previous `j` contributes a line with:
- slope `m = -2 * prefix[j]`
- intercept `b = dp_prev[j] + prefix[j]^2`

We maintain a lower hull of lines and query it for each `i` in increasing order of `prefix[i]`, using a monotonic pointer for O(1) amortized queries. This yields O(n * k) line additions and O(n * k) queries, each O(1) amortized.

Part 1 runs the DP for `(n1, k1)`; Part 2 runs it for `(n2, k2)` using the same routine.

## Run
```bash
python solve.py
```

## Source
https://microcode.microclub.info/challenges/d9c4fe3f-045e-460d-8b5a-389052729515
