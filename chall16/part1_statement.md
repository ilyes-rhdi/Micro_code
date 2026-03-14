# The Shield Cipher

## Part 1

The letters from home were finally readable. Chorba frik recipes from mothers, photos of zlabia and kalb el louz fresh from the kitchen, voice notes from cousins wishing them Ramadan Mabrouk. The crew pinned printed messages on the cabin walls and someone taped a photo of a mawa'id ar-rahma table to the galley door. The last days of Ramadan had arrived, and through the viewport, the blue curve of Earth was growing larger every day.

But the homecoming was not guaranteed yet. The rocket's radiation shield generator, the only thing standing between the crew and lethal reentry radiation, needed a calibration cipher to arm. The generator used a pseudo-random number system driven by a 64-bit internal state that evolved according to a linear congruential formula. The crew pulled the generator's parameters from a diagnostic memory dump: the initial seed, the multiplier, and the increment. The calibration protocol required two things: a verification checksum computed from the generator's first N outputs, and a diagnostic state reading at step T, where T could be in the quadrillions. Without both values, the shields would not arm, and reentry would be fatal.

Adel stared at the numbers on the screen. "We compute these or we don't go home for Eid."

### Input Format

A single line: S0 MULT INC N T P

- S0 -- the initial seed (64-bit unsigned integer).
- MULT -- the multiplier (odd 64-bit unsigned integer).
- INC -- the increment (odd 64-bit unsigned integer).
- N -- the short-range verification step count (5,000 to 15,000).
- T -- the long-range calibration index (up to 10^18).
- P -- the diagnostic modulus (prime, approximately 10^9).
### Generator Structure

Stage 1 -- State Update (Linear Congruential Generator):

At each step, the state advances according to the standard LCG recurrence:

```
S(k) = (S(k-1) * MULT + INC) mod 2^64
```

The standard PCG output permutation is applied to the current state to produce a 32-bit output:

```
xorshifted = ((state >> 18) ^ state) >> 27
rot = state >> 59
output = (xorshifted >> rot) | (xorshifted << ((-rot) & 31))
```

Implementation note on output timing: In the PCG family the output permutation is conventionally applied to the generator state before the LCG transition step, so that the output captures the entropy of the seed prior to mixing. This pre-transition convention avoids a data dependency between the multiply-add and the output extraction, allowing the two operations to be pipelined on the shield controller's hardware. The output sequence is therefore:

```
Step 1: output_1 = PCG(S(0)), then S(0) → S(1)
Step 2: output_2 = PCG(S(1)), then S(1) → S(2)
Step 3: output_3 = PCG(S(2)), then S(2) → S(3)
...
```

### Constraints

- 0 <= S0 < 2^64.
- MULT and INC are odd 64-bit unsigned integers.
- 5,000 <= N <= 15,000.
- 1 <= T <= 10^18.
- P is prime, approximately 10^9.
### Example

```
7392142408732208350 8796093023223 2199023257957 14334 300323046467736761 1000027013
```

Output: The sum as a single integer.

### Example Walkthrough

With S0 = 7392142408732208350, MULT = 8796093023223, INC = 2199023257957:

The first three outputs for verification:

With N = 14334:

Answer: 474629084.

What is the checksum over the first N steps?
