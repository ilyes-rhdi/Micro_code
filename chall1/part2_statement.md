# The Crescent Signal

## Part 2

Three months ago, Adel and a small crew boarded a research vessel and launched into deep space on a scientific mission that would take them further from Earth than any human had gone before. Weeks of routine data collection turned into months, marked only by equipment checks and the quiet hum of the ship between the stars. Then one evening, the ship's calendar rolls past sunset on what should be the eve of Ramadan, and a question ripples through the crew: has the crescent moon actually appeared?

On Earth, you'd simply look up. Out here, millions of kilometers from home, there's no horizon to scan - only the hum of instruments and the endless dark. The crew powers up the ship's long-range telescope array, which immediately floods the console with 50,000 frequency readings bouncing off nearby celestial bodies. Somewhere in that noise, a specific resonance signature will confirm the crescent moon's position.

The telescope's calibration manual is clear: find the readings that sum to the target resonance, then multiply them together to produce the confirmation code. The crew gathers around the console. Ramadan can't begin until that code is found.

### Input Format

- Line 1: The target resonance T (a positive integer).
- Lines 2 to 50001: A list of 50,000 frequency readings (positive integers, each smaller than T).
### Constraints

- There is exactly one valid pair for Part 1 and one valid triplet for Part 2.
- The valid entries are placed near the end of the list.
### Example

```
10000
1200
4500
3300
5500
```

Two entries are considered distinct if they come from different lines. The same numeric value may be used twice only if it appears on two separate lines.

Once you find the two frequencies A and B, compute their product.

Output: A single integer: A * B.

### Example Walkthrough

With T = 10000, scan for pairs:

- 1200 + 4500 = 5700 (no)
- 4500 + 5500 = 10000 ✓
The pair is 4500 and 5500. Output: 4500 * 5500 = 24750000.

What is the product of the two frequencies that sum to the target resonance?

Correct - 92 pts earnedYour Puzzle InputPart 2The initial scan locked onto the crescent, but the signal is noisy. For full triangulation across three distinct sky regions, the crew needs a triple-frequency lock - three readings that together hit the target resonance, spread wide enough across the spectrum to triangulate the moon's exact position.

Find three entries from the list (each on a different line) that sum to exactly T. The triplet must also satisfy a spread condition:

```
max(A, B, C) - min(A, B, C) >= 1000
```

Output: A single integer: A * B * C.

### Example Walkthrough

With T = 10000, scan for triplets summing to T with sufficient spread:

- 1200 + 3300 + 5500 = 10000 ✓
- Spread: max(5500) - min(1200) = 4300 ≥ 1000 ✓
The triplet is 1200, 3300, 5500. Output: 1200 * 3300 * 5500 = 21780000000.

What is the product of the three frequencies that sum to the target resonance?
