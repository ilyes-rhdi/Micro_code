# Dead Star Drift

## Part 2

While the crew was focused on perfecting the iftar schedule, nobody was watching the navigation console. By the time anyone notices, the ship has drifted dangerously off course and straight into the gravity well of a dead star, a collapsed remnant that hasn't burned in millennia. The only way to fire the thruster override is to recalibrate the navigation array. But when Adel powers it up, the console floods with thousands of old transmissions from the star's dying days: garbled numbers, mismatched frequencies, blank static. Somewhere in that noise are the stable signals he needs.

Each transmission is a line in the format VALUE | MODE_S : MODE_R, where VALUE is a signed integer (possibly with leading zeros), and MODE_S and MODE_R are single uppercase letters representing the send and receive channels. Whitespace is scattered randomly around the |, :, and edges of each line. Some lines are completely blank, just static bursts.

### Input Format

- 2000 to 2500 lines of transmission data.
- Non-blank lines follow the pattern: VALUE | MODE_S : MODE_R (with arbitrary whitespace).
- Blank lines are pure noise.
### Example

```
42 | A : A
 -17 | B : C
  00007 | D : D
  0 | E : E
  3  |  F :  F
```

From the example: 42 (A=A ✓), -17 (B≠C ✗), 7 (D=D ✓), 0 (E=E ✓), 3 (F=F ✓). Four stable signals, so S = 4.

Next, the navigation manual says to convert each stable value into a navigation bit. Take the absolute value of each signal. Any signal whose absolute value is 0 carries no information, discard it. For the rest, check if the absolute value is a prime number: if it is, the bit is 1; otherwise, the bit is 0.

From the example: |42| = 42 (not prime → 0), |7| = 7 (prime → 1), |0| = 0 (discarded), |3| = 3 (prime → 1). The bit sequence is [0, 1, 1] with length N = 3.

Now for the thruster calibration. The dead star's rotation has shifted all the frequencies, so the manual requires a rotating index. Let shift = S mod 7. For each position i from 1 to N, compute the effective index:

```
E = ((i + shift - 1) mod N) + 1
```

- If the bit at position i is 1, add E × E to the Power.
- If the bit is 0, subtract gcd(E, N) from the Power.
### Example Walkthrough

From the example: S = 4, shift = 4 mod 7 = 4, N = 3, bits = [0, 1, 1].

- i=1: E = ((1+4-1) mod 3)+1 = 2. Bit is 0 → subtract gcd(2, 3) = 1. Power = -1.
- i=2: E = ((2+4-1) mod 3)+1 = 3. Bit is 1 → add 3×3 = 9. Power = 8.
- i=3: E = ((3+4-1) mod 3)+1 = 1. Bit is 1 → add 1×1 = 1. Power = 9.
What is the Power Index of the filtered signal array?

Correct - 96 pts earnedYour Puzzle InputPart 2The thruster override kicks in, but the dead star's gravity is more erratic than the charts predicted. The navigation computer warns that a single calibration isn't enough, it needs a second value, the Entropy Score, computed by running the bit-stream through a mutation filter and detecting hidden patterns.

Take the same bit sequence B[0..N-1] from Part 1. Slide a window of 5 consecutive bits across it, one position at a time, producing a new mutated sequence of length N - 4.

For each window starting at position i (from 0 to N - 5):

- Pack the five bits into a single number: W = B[i]×16 + B[i+1]×8 + B[i+2]×4 + B[i+3]×2 + B[i+4].
- If W is divisible by 3, emit 1.
- Otherwise, if W is divisible by 5, emit 0.
- Otherwise, emit the parity of the window: (B[i] + B[i+1] + B[i+2] + B[i+3] + B[i+4]) mod 2.
These rules are checked in order, the first match wins.

Once you have the mutated sequence, the computer searches for a repeating cycle. Find the smallest period L such that L divides the length of the mutated sequence and the entire sequence is just the first L elements repeated over and over (i.e., M[i] == M[i mod L] for every i).

Finally, compute the position sum: for every index i where M[i] = 1, add i + 1 to the sum. The Entropy Score is this position sum multiplied by the period length L.

### Example

If the mutated sequence is [1, 0, 1, 0, 1, 0] (length 6):

- The pattern [1, 0] repeats perfectly, so L = 2.
- Positions where M[i] = 1: indices 0, 2, 4 → position sum = 1 + 3 + 5 = 9.
- Entropy = 9 × 2 = 18.
What is the Entropy Score of the mutated signal array?
