# chall2

Challenge solved in Python.

## Files
- `solve.py`: solution script.
- `input.txt`: challenge input.
- `part1_statement.md`: Part 1 statement.
- `part2_statement.md`: Part 2 statement.

## Solution
The expression is parsed in one pass using a stack of partial sums.

Rules implemented:
- `A/B/C/D` add fixed values.
- `(` starts a new group (`stack.append(0)`).
- `){n}` closes the group, applies multiplier `n`, then adds to previous level.
- If a closed group sum is `> 1000`, it is reduced with `% 1000` before multiplication.

Validation checks:
- unmatched `)`
- missing or malformed multiplier after `)`
- unmatched `(` at end
- unexpected characters

Complexity is linear in formula length: `O(n)` time and `O(depth)` memory.

## Run
```bash
python solve.py
```

## Source
https://microcode.microclub.info/challenges/ac1334df-ec1b-439b-9365-5f8fec33a342
