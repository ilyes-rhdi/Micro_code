# chall4

Challenge solved in Python.

## Files
- `solve.py`: solution script.
- `input.txt`: challenge input.
- `part1_statement.md`: Part 1 statement.
- `part2_statement.md`: Part 2 statement.

## Solution
The answer is computed with lower bounds, then taking their maximum.

Bounds used:
- `adjacency_bound`:
  - if one dish type: rounds = its count
  - otherwise max of:
    - maximum adjacent pair sum on the circular array
    - `ceil(total_dishes / floor(n/2))`
- `cooldown_bound`:
  - for each dish count `d > 0`: minimum rounds to place `d` items with cooldown `k` is
    - `(d - 1) * (k + 1) + 1`
  - take the maximum over all dish types

Final result:
- `max(adjacency_bound, cooldown_bound)`

This avoids simulation and computes the minimum rounds directly.

## Run
```bash
python solve.py
```

## Source
https://microcode.microclub.info/challenges/19f122ca-aea6-43e8-8da8-f281afddaa38
