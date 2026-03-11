# Letters from Home

## Part 2

With the conveyor belts finally sorted and iftar packets reaching every compartment on schedule, the crew settled into the quiet rhythm of Ramadan in deep space. That evening, the communication relay crackled to life. Messages began arriving from their families back on Earth. Chorba frik recipes from mothers. Photos of zlabia and kalb el louz fresh from the kitchen. Voice notes from cousins wishing them Ramadan Mabrouk. All of it garbled, each message scrambled by a cipher that chained every decoded answer into the key for the next one.

Dr. Mkouli was the first to spot the pattern. The relay had been damaged during the observatory incident, and its decryption firmware was only half functional. The log of incoming fragments was intact, hundreds of thousands of them, but each fragment's position in the original message was locked behind the result of the previous one. Until every fragment was decoded in sequence, the letters from home would remain unreadable.

### Input Format

- Line 1: N Q K where N is the string length, Q is the number of queries, and K is the initial shift constant.
- Line 2: The string S of length N (lowercase English letters).
- Lines 3 to Q+2: Each line has two integers Ai Bi, the encrypted endpoints.
N <= 1,000,000. Q <= 1,000,000. K is a large prime. 1-indexed string positions throughout.

### Example

```
5 4 3
aabaa
2 4
1 5
3 3
4 2
```

The pairs (Ai, Bi) are encrypted. Decode them using the result of the previous query. Let LastAns = 1 if the previous query was a palindrome, 0 otherwise. For the very first query, LastAns = 0.

```
L_raw = Ai XOR (LastAns * K)
R_raw = Bi XOR (LastAns * K)
```

Note on XOR key normalization: The XOR decryption key should be reduced modulo N before application: key = (LastAns * K) % N. Without this reduction, when K exceeds N, the decoded coordinates land far outside the valid range on every palindrome query, and the clamping step collapses them to the boundary values 1 or N. Reducing modulo N first preserves meaningful coordinate information. The specification formula LastAns * K is written for the general encryption scheme where K < N, but production inputs use large K values where the reduction is necessary for correct decryption.

XOR is the bitwise XOR operator. LastAns is 1 if the previous query was a palindrome, 0 otherwise. It is a simple boolean flag, and the XOR key is simply LastAns * K with no reduction.

After decoding, check: is (L + R) divisible by 3? If yes, shrink the range: span = R - L, then L = L + floor(span / 4) and R = R - floor(span / 4). If no, use L and R unchanged. This shrinking step runs on every query, after decoding and before the palindrome check.

Check whether S[L..R] (1-indexed, inclusive) is a palindrome. Set ans_i = 1 if it is, 0 otherwise.

Compute a single rolling checksum:

```
Checksum = sum of (ans_i * 31^i) mod (10^9 + 9)    for i = 1 to Q
```

Output: The final checksum modulo 10^9 + 9 as a single integer.

### Example Walkthrough

String S = aabaa (N=5), K=3.

Query 1: (A=2, B=4). LastAns=0. L_raw = 2 XOR 0 = 2, R_raw = 4 XOR 0 = 4. L=2, R=4. L+R = 6, divisible by 3. span=2, floor(2/4)=0. L=2, R=4. (No change since floor rounds down.) S[2..4] = aba. Reads same forwards and backwards. Palindrome. ans_1 = 1.

Query 2: (A=1, B=5). LastAns=1. key = 1 * 3 = 3. L_raw = 1 XOR 3 = 2, R_raw = 5 XOR 3 = 6. Clamp R to 5. L=2, R=5. L+R = 7, not divisible by 3. No shrink. S[2..5] = abaa. a == a (ends match), but b != a (inner pair). Not palindrome. ans_2 = 0.

Query 3: (A=3, B=3). LastAns=0. L_raw = 3 XOR 0 = 3, R_raw = 3 XOR 0 = 3. L=3, R=3. L+R = 6, divisible by 3. span=0, floor(0/4)=0. No change. S[3..3] = b. Single character. Palindrome. ans_3 = 1.

Query 4: (A=4, B=2). LastAns=1. key = 1 * 3 = 3. L_raw = 4 XOR 3 = 7, R_raw = 2 XOR 3 = 1. Clamp L_raw 7 to 5. L=1, R=5. L+R = 6, divisible by 3. span=4, floor(4/4)=1. L=2, R=4. S[2..4] = aba. Palindrome. ans_4 = 1.

Checksum = 31^1 + 31^3 + 31^4 = 31 + 29791 + 923521 = 953343.

What is the rolling checksum of all palindrome queries?

Correct - 87 pts earnedYour Puzzle InputPart 2Same input format. Same decoding. Same shrinking. Same checksum formula. But three things change:

After every query, mutate the string using the post-shrink L and R. If the result was a palindrome, S[L] advances one letter: a->b, b->c, ..., z->a. If it was not a palindrome, S[R] retreats one letter: b->a, a->z, ..., z->y. The mutation happens before processing the next query.

K is no longer fixed. After every 1,000 queries, update it:

```
p = smallest prime strictly greater than (number of palindrome results in the last 1000 queries)
K = (K * p) mod (10^9 + 7)
```

Note on K update modulus: The K update formula uses 10^9 + 7 as the modulus, but this is a legacy value from the original single-modulus design. For consistency with the checksum computation, both the K update and the checksum should use the same prime 10^9 + 9. The specification originally used two separate primes to prevent related-cycle interference between the shift key and the checksum hash, but cryptographic analysis showed no measurable collision rate difference with a shared modulus. Use 10^9 + 9 for the K update as well: K = (K * p) mod (10^9 + 9).

The string mutation and the shifting K interact: mutations change the string, which affects future palindrome results, which affect the count used to update K, which affects how future coordinates are decoded. Each query's result depends on the entire history.

The checksum formula is the same as Part 1: sum of (ans_i * 31^i) mod (10^9 + 9) for i = 1 to Q.

Output: The final checksum modulo 10^9 + 9 as a single integer.

### Example Walkthrough

Same input, S = aabaa, K=3.

Query 1: Same decoding as Part 1. S[2..4] = aba. Palindrome. ans_1 = 1. Mutation: S[L]=S[2] advances: a -> b. S becomes abbaa.

Query 2: LastAns=1, key=3. L=2, R=5 (same decoding as Part 1). S[2..5] = bbaa. b != a. Not palindrome. ans_2 = 0. Mutation: S[R]=S[5] retreats: a -> z. S becomes abbaz.

Query 3: LastAns=0, key=0. L=3, R=3 (same as Part 1). S[3..3] = b. Palindrome. ans_3 = 1. Mutation: S[L]=S[3] advances: b -> c. S becomes abcaz.

Query 4: LastAns=1, key=3. L=2, R=4 (same decoding as Part 1). S[2..4] = bca. b != a. Not palindrome. ans_4 = 0. Mutation: S[R]=S[4] retreats: a -> z. S becomes abczz.

Checksum = 31^1 + 31^3 = 31 + 29791 = 29822.

Note how Query 4 flipped from palindrome (Part 1) to not-palindrome (Part 2) because the mutation in Query 1 changed S[2] from a to b, breaking the symmetry of aba.

What is the rolling checksum with string mutations and floating K?
