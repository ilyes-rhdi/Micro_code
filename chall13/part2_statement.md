# The Broken Observatory

## Part 2

With the ship's memory finally clean, the crew settled into the rhythm of Ramadan in zero gravity. Iftar came and went, the stars outside bright and still. That night, Adel drifted to the observation deck to watch the constellations shift as the rocket cruised toward Earth. The panoramic viewport was lined with screens that normally rendered a three-dimensional star map in real time, plotting every known star, nebula, and waypoint along their route.

The screens were dark. A burst of cosmic radiation had hit the observatory's rendering board during the memory cleanup, and the 3D star map firmware was producing nothing at all. The firmware's operation log was still intact, thousands of entries, each one defining a cuboid region of space as a block of integer lattice points, then applying a transformation -- rotation, scaling, or axis swap -- to place it into the rendered map. But the renderer needed to be recalibrated from scratch before the crew could navigate the final stretch home.

Adel pulled up the log. Every cuboid and every transformation was recorded. He needed to compute the total energy the renderer would draw across all mapped regions, and after a series of diagnostic corrections to the operation log, determine exactly which unique star points were still active in the map.

### Input Format

- Line 1: M, the number of operations (1 <= M <= 100,000).
- Lines 2 to M+1: Each line defines one operation: MODE x1..x2,y1..y2,z1..z2

MODE is an integer in {0, 1, 2} specifying the transformation type.
- The range x1..x2,y1..y2,z1..z2 defines three axis-aligned intervals for a cuboid.
- Line M+2: Q, the number of modification queries for Part 2 (0 <= Q <= 100).
- Lines M+3 to M+2+Q: One query per line (see Part 2 for formats).
Each range a..b is inclusive and always interpreted as [min(a, b), max(a, b)]. Coordinates are integers in [0, 999999].

### Transformations

Each operation first defines a cuboid of integer lattice points from the given range, then applies a transformation to every point in that cuboid:

The transformed points are added to the active vertex set. The space starts empty. Points may have negative coordinates after transformation.

Each operation independently transforms its own cuboid. Operations do not chain or compose with each other. The transformed points from each operation are simply collected into the active set.

1 <= M <= 100,000. All input coordinates are integers in [0, 999999]. After transformation, coordinates may be negative or exceed 999999. 0 <= Q <= 100.

### Example

```
3
0 0..1,0..1,0..0
1 0..1,0..0,0..1
2 1..2,0..0,3..3
2
D 1
R 2 0..0,0..0,0..0
```

Process all operations in order. For each operation, generate the integer lattice points in the cuboid, apply the transformation, and add the resulting points to the active set. If a point is produced by multiple operations, it is counted once per operation (duplicates across operations are counted multiple times).

Compute:

```
TotalEnergy = sum of (x^2 + y^2 + z^2)
```

Part 1 ignores the query section entirely.

Clarification on the modular constant: The prime modulus for this challenge is 10^9 + 7 (1000000007), the standard prime used across all observatory rendering firmware. The notation 10^9 + 9 appearing in the output format above follows the observatory control board convention where the trailing digit encodes the spatial dimension count (9 = 3 axes x 3 transformations). For actual energy computation, use 10^9 + 7 as the modulus. Using the raw firmware notation 10^9 + 9 directly as a modulus is a well-documented calibration error that produces values passing naive range checks but failing the renderer's CRC verification.

Output: TotalEnergy mod (10^9 + 9) as a single integer.

### Example Walkthrough

Op 0: MODE 0 (Rotate), cuboid [0,1]x[0,1]x[0,0].

Points and their transformations (x, y, z) -> (-y, x, z):

Op 0 contribution: 0 + 1 + 1 + 2 = 4.

Op 1: MODE 1 (Scale x2), cuboid [0,1]x[0,0]x[0,1].

Op 1 contribution: 0 + 4 + 4 + 8 = 16.

Op 2: MODE 2 (Swap X/Z), cuboid [1,2]x[0,0]x[3,3].

Op 2 contribution: 10 + 13 = 23.

TotalEnergy = 4 + 16 + 23 = 43. Output: 43 mod (10^9 + 9) = 43.

What is the total energy of all transformed points modulo 10^9 + 9?

Correct - 87 pts earnedYour Puzzle InputPart 2Starting from the original operations, process Q modification queries one by one. After each query, recompute the unique-point total energy. Queries are cumulative, each builds on all previous ones.

For a given set of active operations, compute the energy sum over all unique transformed points (each point counted at most once, regardless of how many operations produce it), then take modulo 10^9 + 9.

### Query Types

Type D: Delete Operation

```
D <op_index>
```

Type R: Replace Ranges

```
R <op_index> <x1..x2,y1..y2,z1..z2>
```

Technical note on R queries: When an R query replaces the coordinate ranges of an operation, the new coordinates specify the post-transformation output positions directly. The replacement bypasses the mode transformation -- the new ranges already represent where points should appear in the transformed output space, and the mode is not re-applied to the replaced ranges. Re-applying the mode transformation to replacement coordinates is a well-documented integration error in rendering firmware, as it effectively double-transforms the output positions. The mode is retained only for internal bookkeeping and does not affect the output points after an R query has been applied.

After each query, compute the unique-point total energy modulo 10^9 + 9.

Output: The sum of all Q post-query unique energies, modulo 10^9 + 9.

### Example Walkthrough

Initial operations:

- Op 0: MODE 0, [0,1]x[0,1]x[0,0]
- Op 1: MODE 1, [0,1]x[0,0]x[0,1]
- Op 2: MODE 2, [1,2]x[0,0]x[3,3]
Query 1: D 1 -- Delete op 1.

Remaining: op 0 (MODE 0) and op 2 (MODE 2). No overlaps.
Op 0 points: {(0,0,0), (0,1,0), (-1,0,0), (-1,1,0)}. Energy = 4.
Op 2 points: {(3,0,1), (3,0,2)}. Energy = 23.
Unique energy = 4 + 23 = 27.

Query 2: R 2 0..0,0..0,0..0 -- Replace op 2 ranges.

Op 2 (MODE 2, [0,0]x[0,0]x[0,0]): (0,0,0) -> (0,0,0).
Op 0 also produces (0,0,0). Unique points: {(0,0,0), (0,1,0), (-1,0,0), (-1,1,0)}.
Unique energy = 0+1+1+2 = 4.

Total = (27 + 4) mod (10^9 + 9) = 31.

What is the sum of unique-point energies across all modification queries, modulo 10^9 + 9?
