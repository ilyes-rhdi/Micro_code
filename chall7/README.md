# chall7

Challenge solved in Python.

## Files
- `part1_statement.md`: Part 1 statement
- `part2_statement.md`: Part 2 statement
- `input.txt`: challenge input

## Results
- Part 1: `227232148`
- Part 2: `157524054`

## Notes
Simulation is done for exactly 1000 generations per group.

Part 1 uses:
- strength = number of `1` bits in each 8-bit sequence
- tie-break on highest index
- split/recombination
- radiation bit flip at `(g * 3 + strength_first) mod 8`
- right rotation by `g mod 4`

Part 2 keeps the same flow with these changes:
- strength is replaced by resemblance to a drifting reference key
- initial key: `11010110` (reset per group)
- key updates each generation:
  - if `g mod 100 == 0`: rotate key left by 1, then flip bits 2 and 5
  - if `g mod 250 == 0`: reverse key (after previous rule if both trigger)
- split formula depends on number of `1` bits in current key:
  - if key has more than 4 ones: `(r1 + r2 + 2) mod 7 + 1`
  - else: `(r1 + r2) mod 7 + 1`
