# The Fasting Formula

## Part 2

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

Correct - 66 pts earnedYour Puzzle InputPart 2The first calculation checked out, but when Adel runs the full orbital dataset, the formula has grown to enormous proportions, up to 50 MB with multipliers reaching millions. The ship's computer warns that compound chains this dense become unstable and must be collapsed before they overflow the system.

Collapse rule: After computing the energy inside a group (...), before applying the multiplier {N}, check:

- If the internal energy is strictly greater than 1,000, replace it with internal_energy mod 1,000.
- Then multiply by N.
- Then add to the parent chain.
This collapse applies at every bracket closure, not just at the end.

Output: The final stabilized energy as a single integer.

### Example Walkthrough

For the same input A(B(C){4}){2}D:

- Innermost (C): internal energy = 156. Is 156 > 1,000? No. Apply multiplier: 156 × 4 = 624.
- Next level (B(C){4}): internal energy = 383 + 624 = 1007. Is 1007 > 1,000? Yes. Replace: 1007 mod 1000 = 7. Apply multiplier: 7 × 2 = 14.
- Total: 247 + 14 + 512 = 773.
What is the stabilized energy of the formula?
