# chall16

Challenge solved in Python.

## Files
- `solve.py`: solution script (part 1 and part 2).
- `input.txt`: challenge input.
- `part1_statement.md`: Part 1 statement.
- `part2_statement.md`: Part 2 statement.

## Solution
Part 1 (checksum):
- Simulate the PCG output on the 64-bit LCG state.
- For each of the first `N` outputs, add the 32-bit output to a rolling checksum modulo `P`.
- State update is `S = (S * MULT + INC) mod 2^64`, but output is taken **before** the transition as specified.

Part 2 (leap ahead):
- The LCG is an affine map `x -> MULT * x + INC`.
- Repeated squaring composes affine maps in `O(log T)` steps.
- Maintain `(acc_mult, acc_inc)` for the composed map and apply it to `S0`.
- All affine arithmetic is done modulo `P` to get `S(T) mod P` efficiently.

## Run
```bash
python solve.py
```

## Source
https://microcode.microclub.info/challenges/f54531ff-c6f1-4465-b0e6-64b1ea782021
