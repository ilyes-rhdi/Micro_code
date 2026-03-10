# The Broken Observatory

## Part 1

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
