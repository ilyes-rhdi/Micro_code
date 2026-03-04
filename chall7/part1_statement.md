# The Children's Ward

## Part 1

Communication is finally flowing between the crew and the LMKOULYIN. Lmkouli spent the evening sharing what life on the planet is like while Adel explained Ramadan: the fasting from dawn to dusk, the iftars shared with family, the sense that the whole world slows down and breathes together for a month. The LMKOULYIN were fascinated.

But as the crew powers up the rocket the next morning, Lmkouli raises a hand. There is one more thing.

He leads them across the settlement to a low building, quieter than the rest. Inside, young patients lie in beds connected to monitoring arrays. The planet's children are born with 8-bit genetic codes that drift over time under the planet's intense cosmic radiation. Each generation, the codes shift: bits flip, sequences recombine, patterns emerge. The hospital tracks these changes to predict which treatments each child will need months in advance. But their computing system broke down weeks ago, and without a simulation engine, the doctors can no longer plan ahead.

Adel pulls up a chair at the broken terminal. Dr. Mkouli, the ward's lead researcher, spreads out the patient files. The crew has time before the launch window opens.

### Input Format

- Line 1: A single integer P, the number of patient groups.
- Lines 2 to 4P+1: Genetic sequences. Every block of 4 consecutive lines is one group. Each line is exactly 8 characters of 0 and 1.
Within each group, the 4 sequences are indexed 0 through 3. Bit positions are also 0-indexed from the left (position 0 is the leftmost bit, position 7 is the rightmost).

### Example

```
1
10100000
00001010
11100000
00000111
```

Dr. Mkouli explains the first model: the strength of a genetic code is simply the number of 1 bits it contains (for example, 11100000 has strength 3). Every day, the two strongest codes in a group combine to produce a new generation: their patterns blend and then the radiation strikes.

For each patient group, simulate exactly 1000 generations. For each generation g (from 1 to 1000), apply the following steps in this exact order:

Step 1: Selection. Assign each sequence a strength equal to the count of 1 bits it contains. Identify the sequence with the highest strength: call it First. Identify the sequence with the second-highest strength: call it Second. If two sequences share the same strength, the one at the higher index wins.

Step 2: Blend point. Compute split = (strength_First + strength_Second) mod 7 + 1. This value is always between 1 and 7 inclusive.

Step 3: Recombination. Produce two offspring:

- Offspring 1 = First[0 : split] concatenated with Second[split : 8]
- Offspring 2 = Second[0 : split] concatenated with First[split : 8]
(The notation S[a : b] means the substring of S from position a up to but not including position b.)

Step 4: Radiation strike. Compute strike = (g x 3 + strength_First) mod 8. Flip the bit at position strike in both Offspring 1 and Offspring 2.

Step 5: Array rotation. Form the ordered array [First, Second, Offspring 1, Offspring 2]. Rotate this array to the right by g mod 4 positions. In a right rotation by k, the last k elements wrap to the front. For example, rotating [A, B, C, D] right by 1 gives [D, A, B, C]. The rotated array becomes the group's population for the next generation.

After each generation, record the sum of the decimal values of all 4 sequences in the new population (each sequence is an 8-bit binary number, so its decimal value is between 0 and 255 inclusive). The treatment burden for a group is the sum of these recorded values across all 1000 generations.

Output: Sum the treatment burdens of all P groups. Output this grand total as a single integer.

### Example Walkthrough (Generation 1)

Starting population: [10100000, 00001010, 11100000, 00000111]

Strengths: 2, 2, 3, 3.

Selection: Highest strength = 3, appears at indices 2 and 3. Tie: the higher index wins, so First = 00000111 (index 3, strength 3). Next highest = 3 at index 2, so Second = 11100000 (index 2, strength 3).

Blend point: split = (3 + 3) mod 7 + 1 = 6 mod 7 + 1 = 7.

Recombination:

- Offspring 1 = 0000011 + 0 = 00000110
- Offspring 2 = 1110000 + 1 = 11100001
Radiation strike: strike = (1 x 3 + 3) mod 8 = 6. Flip bit 6:

- Offspring 1: 00000110 -> 00000100
- Offspring 2: 11100001 -> 11100011
Rotation: g mod 4 = 1. Array = [00000111, 11100000, 00000100, 11100011]. Rotate right by 1 -> [11100011, 00000111, 11100000, 00000100].

Decimal values: 227 + 7 + 224 + 4 = 462.

(This continues for all 1000 generations, accumulating each sum.)

What is the total treatment burden across all patient groups?
