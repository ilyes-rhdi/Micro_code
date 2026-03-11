# chall13

Challenge solved in Python.

## Files
- `solve.py`: solution script.
- `input.txt`: challenge input.
- `part1_statement.md`: Part 1 statement.
- `part2_statement.md`: Part 2 statement.

## Solution
Each operation defines a transformed 3D lattice cuboid. Energy is sum of `x^2 + y^2 + z^2` over active points.

## Part 1
For each operation independently:
- Parse mode and ranges.
- Convert to transformed axis descriptors `(lo, hi, step)` for each axis.
- Compute contribution analytically with formulas:
  - count of terms,
  - sum of squares on interval,
  - multiply by counts of other axes.
- Add all operation energies modulo `1_000_000_009`.

No explicit point enumeration in Part 1.

## Part 2
Queries can delete/replace operations and need cumulative answer over time.

Strategy:
- Keep descriptors and single-op energies for all operations.
- Maintain active flags.
- After each query, recompute current union energy approximately by overlap graph:
  - put active cuboids in coarse 3D bins,
  - test pair intersections only for candidate pairs from same bins,
  - build component graph of intersecting cuboids.
- For each connected component:
  - size 1: add single energy,
  - size 2: inclusion-exclusion with exact intersection energy,
  - larger: enumerate integer points with dedup set and sum exact energy.

Accumulate each query result into final modulo answer.

## Complexity
- Uses analytical interval math for most work.
- Uses spatial binning to reduce pair checks.
- Falls back to exact point enumeration only for complex overlap components.

## Run
```bash
python solve.py --part 1
python solve.py --part 2
```

## Source
https://microcode.microclub.info/challenges/9e5f4c8f-b7df-48c9-8fcd-fb87437620c6
