# The Fasting Formula

## Part 1

The crescent has been confirmed. Ramadan has begun! But fasting in space is nothing like fasting on Earth. There's no sunrise or sunset out here, just the cold glow of distant stars. The crew needs to compute precise fasting windows based on their orbital trajectory, and the ship's navigation computer expresses these calculations as deeply nested compound formulas.

Each formula uses a compressed notation: base elements (A, B, C, D) carry fixed energy values, and parenthesized groups with multipliers represent nested orbital adjustments. The deeper the nesting, the more complex the calculation. Adel pulls up the formula on screen, one massive line of brackets and letters, and gets to work.

### Input Format

A single line containing a formula string using the following elements and syntax:

- A = 247 energy, B = 383 energy, C = 156 energy, D = 512 energy.
- (...){N} means the contents inside the parentheses are multiplied by N.
- Parentheses can be nested up to 50 levels deep.
- Every ( has a matching ) immediately followed by {N}.
### Example

```
A(B(C){4}){2}D
```

Output: The total energy as a single integer.

### Example Walkthrough

For input A(B(C){4}){2}D:

- C = 156
- (C){4} = 156 × 4 = 624
- B(C){4} = 383 + 624 = 1007
- (B(C){4}){2} = 1007 × 2 = 2014
- Total: A + 2014 + D = 247 + 2014 + 512 = 2773
What is the total energy of the formula?
