# chall6

Challenge solved in Python.

## Files
- `solve.py`: solution script (currently prints Part 2 answer).
- `input.txt`: challenge input.
- `part1_statement.md`: Part 1 statement.
- `part2_statement.md`: Part 2 statement.

## Solution
### Part 1
For each node `i`, we need:
- all descendants `j` of `i`
- contribution `(j - i)^2`

Use one DFS post-order on the rooted tree to compute for each subtree:
- `size[u]`: number of nodes
- `label_sum[u]`: sum of node labels in subtree
- `label_sq_sum[u]`: sum of squared labels in subtree

For node `u`, descendants are subtree nodes excluding `u`.
Then:
- `sum((j-u)^2)` over descendants =
  `sum(j^2) - 2u*sum(j) + count*u^2`

Sum this for all nodes and take modulo `1_000_000_007`.

Part 1 result: `229738030`

### Part 2
Need:
`S = sum(depth(LCA(i,j)))` for all `0 <= i < j < N`.

Approach:
- Precompute depths with DFS/BFS.
- Build binary-lifting table `up[k][v]` (2^k-th ancestor of `v`).
- Compute each `LCA(i,j)` in `O(log N)`.
- Sum depths for all pairs `i < j`.

Complexity:
- Preprocess: `O(N log N)`
- Pair loop: `O(N^2 log N)`
- Works comfortably for `N <= 2000`.

Part 2 result: `2016140`

## Run
```bash
python solve.py
```

## Source
https://microcode.microclub.info/challenges/8f8f30a6-7e28-422d-9638-bd8a63c61f97
