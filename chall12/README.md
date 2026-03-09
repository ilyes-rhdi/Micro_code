# Ramadan Cleanup - Explanation of `solve.py`

This document explains the approach implemented in `solve.py` for both parts of the challenge.

## Problem Summary

We process a sequence of heap operations over objects (`ALLOC`, `REF`, `DELREF`, `ADDROOT`, `DELROOT`) and compute:

- Part 1: alive memory size after reference-count based reclamation.
- Part 2: alive memory size after periodic mark-and-sweep GC, then return:
  - `part2_alive_size * 1000000 + abs(part2_alive_size - part1_alive_size)`

## Data Model in `solve.py`

- Each heap node is represented by class `object` with:
  - `id`, `size`
  - `refcount` (for Part 1)
  - `outgoing_ref` and `ongoing_ref` adjacency lists
  - `alive`, `marked`
- Globals for Part 1:
  - `rootset`: list of root object ids
  - `heap`: dictionary `id -> object`

## Part 1 Logic (Reference Counting)

### Allocation
- `ALLOC id size` creates an object and inserts it into `heap`.
- Initial refcount is `1` if `id` is in current `rootset`, otherwise `0`.

### Edge Updates
- `REF src dst`:
  - ignored if objects are missing/dead
  - if edge does not already exist: add `src -> dst` and increment `dst.refcount`
- `DELREF src dst`:
  - ignored if objects are missing/dead
  - if edge exists: remove edge and decrement `dst.refcount`
  - if `dst.refcount == 0`, cascade free with `FREE(dst)`

### Root Updates
- `ADDROOT id` increments refcount and appends `id` to `rootset`.
- `DELROOT id` removes one occurrence from `rootset` (if present), decrements refcount, and frees on zero.

### Free/Cascade (`FREE`)
When an object reaches refcount zero:
- mark object dead
- remove all occurrences from `rootset`
- remove its outgoing edges
- decrement targets' refcounts, recursively freeing newly-zero targets

### Part 1 Output
- sum of sizes of all alive objects in `heap`

## Part 2 Logic (Periodic Mark-and-Sweep)

Part 2 replays operations on a fresh graph (`p2_heap`, `p2_rootset`) without using refcounts for reclamation.

### Effective Operation Counter
- `ALLOC` creates/overwrites object in `p2_heap`.
- For non-ALLOC operations that can mutate alive objects, a `mutated` flag is set.
- An `effective_ops` counter is advanced based on this flow.
- Every time `effective_ops % K == 0`, run `gc(...)`.

### Mark Phase
- Start from all ids in `p2_rootset`.
- DFS over `outgoing_ref`.
- Mark every reachable alive object.

### Sweep Phase
- Dead set = alive but unmarked objects.
- For each dead object:
  - mark as not alive
  - remove all occurrences from root set
  - detach outgoing and incoming edges

### Final Part 2 Output
- `p2 = sum(size of alive objects in p2_heap)`
- `p1 = solve_p1(input)`
- return `p2 * 1000000 + abs(p2 - p1)`

## Complexity (High Level)

- Part 1:
  - near-linear in number of operations plus traversed freed edges during cascades
- Part 2:
  - operation replay is linear in operations
  - each GC is `O(V + E)` over currently alive graph

## Running

`solve.py` reads input from `input.txt` in `chall12/`:

```bash
python solve.py
```

It prints:
1. Part 1 alive size
2. Part 2 combined encoded result
