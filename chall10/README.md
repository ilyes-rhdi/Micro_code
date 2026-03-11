# chall10

Challenge solved in Python.

## Files
- `solve.py`: solution script.
- `input.txt`: challenge input.
- `part1_statement.md`: Part 1 statement.
- `part2_statement.md`: Part 2 statement.

## Solution
### Part 1
Need minimum directed cycle weight, with an extra option to reverse exactly one edge.

Implementation:
- Build adjacency list with edge indices.
- Run repeated single-target Dijkstra with cutoff pruning.

Two cases:
- No reversal:
  - For each edge `(u -> v, w)`, candidate cycle is `w + dist(v, u)`.
- Reverse one edge:
  - Treat edge `(u -> v, w)` as `(v -> u, w)`.
  - Candidate is `w + dist(u, v)` in graph where this exact edge instance is removed.

Take minimum candidate across all edges.

### Part 2
Need condensation-graph chain scoring.

Implementation:
- Compute SCCs with Kosaraju.
- For each SCC:
  - Build internal edge list.
  - Compute SCC cycle weight (minimum directed cycle inside SCC) using Dijkstra-based routine.
- Build DAG of SCCs (cross edges collapsed by min edge weight per pair).
- Run DP on DAG in reverse topological order:
  - maximize chain length,
  - tie-break by maximum sum of SCC weights.

Return best chain score.

## Complexity
- Part 1: `O(M * (M log N))` in worst case from repeated Dijkstra, with practical pruning via current best cutoff.
- Part 2: SCC decomposition plus per-SCC cycle computations and DAG DP.

## Run
```bash
python solve.py --part 1
python solve.py --part 2
```

## Source
https://microcode.microclub.info/challenges/d984fd91-e65d-4364-ba14-22e8e72c18b0
