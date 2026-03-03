# chall5

Challenge solved in Python.

## Files
- `solve.py`: solution script.
- `input.txt`: challenge input.
- `part1_statement.md`: Part 1 statement.

## Solution
The solver processes each non-blank transmission line using a strict parser:
- format: `VALUE | MODE_S : MODE_R` with arbitrary spaces
- `VALUE` is parsed as signed integer (leading zeros supported)

Algorithm:
1. Keep only stable transmissions where `MODE_S == MODE_R`.
2. Let `S` be the number of stable transmissions.
3. For each stable value:
- compute `abs(VALUE)`
- discard if it is `0`
- append bit `1` if prime, else `0`
4. Let `N` be number of bits and `shift = S % 7`.
5. For each bit position `i` from `1..N`:
- `E = ((i + shift - 1) % N) + 1`
- if bit is `1`: add `E * E`
- else: subtract `gcd(E, N)`

Complexity:
- parsing is linear in line count
- primality checks are efficient trial division up to `sqrt(n)` for each kept value

## Result (Part 1)
`74415219`

## Run
```bash
python solve.py
```

## Source
https://microcode.microclub.info/challenges/dcfabdd7-cf3a-4bc8-b395-c8ffa38c8349
