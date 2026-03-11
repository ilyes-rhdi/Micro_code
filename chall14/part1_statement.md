# The Iftar Express

## Part 1

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
