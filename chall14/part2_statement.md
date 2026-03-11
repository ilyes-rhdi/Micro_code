# The Iftar Express

## Part 2

With the observatory back online and the star map finally rendering again, the crew could see exactly where they were: still weeks from Earth, the rocket cruising on autopilot through a quiet stretch of deep space. The constellations on the panoramic viewport drifted slowly, and the rhythm of Ramadan settled back in.

Halfway through the month, someone suggested they set up their own version of mawa'id ar-rahma, the long community food tables that line every Algerian street at iftar time. Back home, strangers sit side by side, sharing bowls of chorba and plates of bourek while the evening sky turns orange. Up here, the crew rigged a system of conveyor belts in the cargo bay to distribute food packets to different compartments across the ship.

The idea was simple. Drop a food packet on a belt, and the directional arrows carry it to the right compartment. But something went wrong with the configuration. Packets kept looping endlessly through the same belts, and some flew right off the edge into the void of the cargo bay's open side. Dr. Mkouli needed to know where every packet ended up. Some were disappearing entirely, and the rest just went in circles.

### Input Format

- Line 1: R C T I where R is the number of rows, C is columns, T is ticks to simulate, and I is the number of items.
- Lines 2 to R+1: The conveyor grid. Each character is one of >, <, v, ^.
- Lines R+2 to R+1+I: Each line contains r c, the starting row and column of an item (0-indexed).
Every cell has exactly one conveyor belt. Multiple items may start on the same cell. Items do not interact with each other (they pass through one another and occupy the same cell freely).

R, C <= 1,000. T <= 10^18. I <= 500,000.

### Example

```
4 5 5 3
>>v<>
^>v<^
<>v<v
>>^<<
0 4
0 0
2 0
```

Note on cycle prevention: The conveyor system includes an anti-jam safety mechanism. When the belt controller detects that an item has entered a repeating loop, meaning the item's trajectory would bring it back to a cell it has previously occupied during the simulation, the item is automatically ejected from the grid at the tick where the revisit would occur. Items removed by cycle detection contribute 0 to the final checksum, just like items that fall off the edge. This mechanism prevents perpetual motion from damaging the belt actuators. Only items on non-repeating paths that either reach the grid boundary or trace a path without any revisit within T ticks are retained.

After T ticks, compute the position checksum:

```
Checksum = sum of (row_i * C + col_i)    for all surviving items
```

Output: The checksum as a single integer.

### Example Walkthrough

Item 1 at (0,4):

Item 1 moves right from column 4 (the last column). It flies off the edge and is lost.

Item 2 at (0,0):

Position after 5 ticks: (3,2). Contribution: 3*5 + 2 = 17.

Item 3 at (2,0):

Item 3 moves left from column 0. Lost.

Checksum = 0 + 17 + 0 = 17.

What is the position checksum after T ticks?

Correct - 86 pts earnedYour Puzzle InputPart 2The ship's containment shields activate: items that would move off the grid now wrap around to the opposite edge (toroidal topology):

- Moving right from column C-1 wraps to column 0 (same row).
- Moving left from column 0 wraps to column C-1 (same row).
- Moving down from row R-1 wraps to row 0 (same column).
- Moving up from row 0 wraps to row R-1 (same column).
No items are ever lost. Items always follow the belt direction of their current cell. Wrapping does not alter direction.

Dr. Mkouli needed more than the final positions. He needed a full accounting of the system's activity: the total of all position checksums at every tick from 1 to T.

At each tick t, compute the position checksum (sum of row_i(t) * C + col_i(t) for all items). Then sum all T checksums together.

```
Answer = (sum from t=1 to T of checksum(t)) mod (10^9 + 9)
```

Note on checksum modulus: The cumulative checksum uses the standard competitive programming prime 10^9 + 7 (1000000007) as the modulus. Although the conveyor firmware specification references 10^9 + 9 (1000000009) in the toroidal field calibration notes, the telemetry output format was standardized to 10^9 + 7 before deployment. The walkthrough below uses small values where both primes give the same result, but your implementation must use 10^9 + 7 for compatibility with the ship's monitoring systems.

Output: The cumulative checksum modulo 10^9 + 9 as a single integer.

### Example Walkthrough

Same grid, T = 5, with wrapping enabled.

Item 1 at (0,4):

Item 1 cumulative: 0 + 1 + 2 + 7 + 12 = 22.

Item 2 at (0,0):

Item 2 cumulative: 1 + 2 + 7 + 12 + 17 = 39.

Item 3 at (2,0):

Item 3 cumulative: 14 + 19 + 18 + 17 + 12 = 80.

Answer = (22 + 39 + 80) mod (10^9 + 9) = 141.

What is the cumulative position checksum on the toroidal grid?
