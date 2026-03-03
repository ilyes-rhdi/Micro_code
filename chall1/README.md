# chall1

Challenge solved in Python.

## Files
- `solve.py`: solution script.
- `input.txt`: challenge input.
- `part1_statement.md`: Part 1 statement.
- `part2_statement.md`: Part 2 statement.

## Solution
The solver searches a valid triplet `(a, b, c)` such that:
- `a + b + c = target`
- `c - a >= 1000` (spread constraint)
- values can be reused only if they exist enough times in input

Implementation details:
- It counts values with `Counter` to validate duplicate usage.
- It iterates over sorted unique values for `a` and `b`, then computes `c = target - a - b`.
- It skips impossible cases early (`c < b`, missing `c`, spread too small).
- It validates multiplicities for equal-value cases (`a==b==c`, `a==b`, `b==c`).
- It returns `a * b * c` for the first valid triplet.

## Run
```bash
python solve.py
```

## Source
https://microcode.microclub.info/challenges/aec13818-0c9f-414f-bc28-518630f61940
