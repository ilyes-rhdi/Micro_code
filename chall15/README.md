# chall15

Challenge solved in Python.

## Files
- `solve.py`: solution script.
- `input.txt`: challenge input.
- `part1_statement.md`: Part 1 statement.
- `part2_statement.md`: Part 2 statement.

## Solution
The challenge processes encrypted range queries on a mutable string and computes a rolling checksum of palindrome results.

## Part 1
Implementation:
- Precompute palindrome radii with Manacher:
  - odd centers (`d1`),
  - even centers (`d2`).
- For each query:
  - decode `(L, R)` using `LastAns` and `K`,
  - clamp/swap, then apply shrink rule when `(L+R) % 3 == 0`,
  - check palindrome in O(1) using Manacher arrays,
  - update checksum with `31^i mod (1e9+9)`.

Overall complexity: `O(N + Q)`.

## Part 2
String mutates after each query, so static Manacher no longer works.

Implementation:
- Maintain two Fenwick trees of 64-bit rolling hash:
  - forward hash,
  - reverse hash.
- Palindrome check for `[L..R]`:
  - compare normalized forward hash with normalized reverse hash in O(log N).
- After each query:
  - if palindrome: increment `S[L]` cyclically,
  - else decrement `S[R]` cyclically,
  - apply point updates to both Fenwick trees.
- Every 1000 queries:
  - count palindromes in block,
  - `p = next_prime(count)`,
  - update `K = (K * p) mod 1_000_000_007`.
- Continue checksum accumulation as in part 1 (`mod 1_000_000_009`).

Overall complexity: `O((N + Q) log N)`.

## Run
```bash
python solve.py --part 1
python solve.py --part 2
```

## Source
https://microcode.microclub.info/challenges/337da300-3aad-4b86-be02-e21d98975788
