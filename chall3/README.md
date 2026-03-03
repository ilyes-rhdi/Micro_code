# chall3

Challenge solved in Python.

## Files
- `solve.py`: solution script.
- `input.txt`: challenge input.
- `part1_statement.md`: Part 1 statement.
- `part2_statement.md`: Part 2 statement.

## Solution
The program simulates a stack-based VM with 32-bit unsigned arithmetic.

Supported instructions:
- stack ops: `push`, `dup`, `dup3`, `rol n`
- unary op: `not`
- binary ops: `sum`, `sub`, `xor`, `or`, `and`, `shl`, `shr`

Key behavior:
- Every result is masked with `0xFFFFFFFF`.
- After each binary op result `t`:
  - if MSB of `t` is `1`, the whole stack is reversed
  - else if `t` is odd, next binary op uses reversed operands
- Final answer is XOR of all remaining stack values.

This gives a direct faithful interpreter of the challenge machine.

## Run
```bash
python solve.py
```

## Source
https://microcode.microclub.info/challenges/60d5d523-ec5b-429f-9a6b-68bd17185eda
