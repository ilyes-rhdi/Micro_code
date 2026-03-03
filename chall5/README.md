# chall5

Challenge solved in Python.

## Files
- `solve.py`: solution script (prints Part 2 Entropy Score).
- `input.txt`: challenge input.
- `part1_statement.md`: Part 1 statement.
- `part2_statement.md`: Part 2 statement.

## Solution
### Shared parsing
Each non-blank line is parsed as:
- `VALUE | MODE_S : MODE_R` (arbitrary spaces allowed)

Stable transmissions are lines where `MODE_S == MODE_R`.
From these lines:
- `S` = number of stable transmissions
- build bit sequence `B` by taking `abs(VALUE)`:
  - discard `0`
  - prime -> `1`, non-prime -> `0`

### Part 1 (Power Index)
- `shift = S % 7`
- for each 1-based bit position `i` in `B` (length `N`):
  - `E = ((i + shift - 1) % N) + 1`
  - if bit is `1`: add `E * E`
  - else: subtract `gcd(E, N)`

Part 1 result: `74415219`

### Part 2 (Entropy Score)
- Slide a window of 5 bits over `B` to create mutated sequence `M` (length `N - 4`).
- For each window packed into `W = b0*16 + b1*8 + b2*4 + b3*2 + b4`:
  - if `W % 3 == 0` -> emit `1`
  - else if `W % 5 == 0` -> emit `0`
  - else emit parity `(b0+b1+b2+b3+b4) % 2`
- Find smallest period `L` dividing `len(M)` such that `M` is repetition of first `L` values.
- Let `position_sum = sum(i+1 for all i where M[i] == 1)`.
- Entropy Score = `position_sum * L`.

Part 2 result: `1576041652`

## Run
```bash
python solve.py
```

## Source
https://microcode.microclub.info/challenges/dcfabdd7-cf3a-4bc8-b395-c8ffa38c8349
