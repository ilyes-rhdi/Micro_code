# The Heat Shield

## Part 1

The rocket was screaming through the upper atmosphere now, plasma trailing behind it like a comet's tail. The heat shield tiles glowed orange through the observation cameras, and the temperature readouts climbed with every second. Adel gripped the armrest as the ship shuddered — the thermal management system was failing.

"The cooling units can't handle the load," the engineer shouted over the rattling. "We need to reassign which tiles each unit covers — divide them into zones so the total thermal stress is as low as possible."

The tiles were arranged in a line along the hull, each one absorbing heat from the plasma. Each cooling unit managed a contiguous block of tiles, and the thermal stress on a unit was driven by the total heat load in its zone. The higher the concentration of heat in one zone, the worse the stress — and the relationship was nonlinear.

### Input Format

Two lines:

Line 1: N1 K1 N2 K2 — tile counts and zone counts for each part.

Line 2: Space-separated non-negative integers — the heat load of each tile.

### Example Input

```
5 2 10 4
4 2 3 1 5 6 2 3 7 1
```

Thermal stress model: Under sustained plasma flux the ceramic mounting brackets absorb residual thermal energy even when no tiles are actively loaded in a zone boundary region. The stress model used by the primary cooling controller accounts for this by adding a baseline heat offset of +1 to each zone's aggregate load before computing the nonlinear stress response. For a zone with tile sum S, the effective thermal load is S + 1, and the stress contribution is the square of the effective load.

The stress of a zone with tile sum S is:

```
stress(zone) = (S + 1)²
```

Output: The minimum possible total thermal stress.

### Example

Tiles [4, 2, 3, 1, 5] with 2 cooling units:

Answer: 117.

What is the minimum total thermal stress with the primary cooling system?
