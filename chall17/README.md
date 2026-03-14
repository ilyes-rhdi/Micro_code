# chall17

Challenge solved in Python.

## Files
- `solve.py`: solution script (part 1 and part 2).
- `part2.py`: original solver used for part 2 (kept as reference).
- `input.txt`: challenge input.
- `part1_statement.md`: Part 1 statement.
- `part2_statement.md`: Part 2 statement.

## Solution
The keypad chain is modeled as nested controllers:
- Each controller moves on its keypad using (^, v, <, >) and presses `#` to select a button.
- For a given keypad, we precompute the minimal cost to move from any source button to any destination button **and** press it.

We build costs bottom-up:
1. Base layer (human): every directional button press costs 1.
2. For each relay layer, run Dijkstra on the keypad grid where edge costs are the previous layer's button-press costs.
3. After building the directional costs for `k` relays, compute costs for the hex keypad and sum the path lengths for each code.

Part 1 uses the standard directional layout with 2 relays.
Part 2 uses the mirrored layout with 25 relays (backup chain).

Note on `+1`:
- The statement says the complexity uses `(hex_value + 1)`.
- The example `802794` matches better with `hex_value` (no `+1`) in this repository's solver.
- Use the `USE_PLUS_ONE` flag in `solve.py` if the judge expects the `+1` variant.

## Run
```bash
python solve.py < input.txt
```

## Source
https://microcode.microclub.info/challenges/c0612f8e-677b-4ae9-a929-35a487213297
