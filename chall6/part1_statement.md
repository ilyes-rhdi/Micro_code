# The Alien Tongue

## Part 1

The crew managed to change course just in time, narrowly escaping the dead star's gravitational pull. The navigation system locked onto the nearest habitable planet, and after a tense descent, they touched down safely. But as the airlock hisses open, they're greeted not by empty terrain, but by a crowd of LMKOULYIN, weapons raised.

Just as things are about to go very wrong, one of the LMKOULYIN, Lmkouli, pushes through the crowd, waving frantically at the others to stand down. Lmkouli has been studying human languages and recognizes the crew as Earthlings. He pulls out a translation file, a structured tree of linguistic roots, where each word traces back through ancestor nodes to a common origin. Lmkouli can understand the crew, but the crew can't understand a word the LMKOULYIN say.

To establish two-way communication, Adel needs to analyze the ancestor relationships in this linguistic tree and compute aggregate values that will power the translation matrix. The tree is rooted, binary, and every relationship matters.

### Input Format

- Line 1: N, the number of nodes (1 <= N <= 2000), labeled 0 to N-1.
- Lines 2 to N: Each line contains two integers P C, meaning node P is the parent of node C.
The root is always node 0. Each node has at most two children. Parent indices always appear before their children in the input.

### Example

```
5
0 1
0 2
1 3
1 4
```

- mat[i][j] = 1 if node i is an ancestor of node j
- mat[i][j] = 0 otherwise
A node is NOT considered an ancestor of itself.

Compute the following compressed value:

```
result = sum of mat[i][j] * (j - i)^2    for all 0 <= i, j < N
```

Output: result mod 1,000,000,007

### Example Walkthrough

Tree structure:

```
0 (depth 0)
       / \
      1   2 (depth 1)
     / \
    3   4 (depth 2)
```

- Node 0 is ancestor of: 1, 2, 3, 4
- Node 1 is ancestor of: 3, 4
- Nodes 2, 3, 4 have no descendants
Compute mat[i][j] * (j - i)^2 for each ancestor pair:

result = 1 + 4 + 9 + 16 + 4 + 9 = 43

What is the compressed ancestor value modulo 1,000,000,007?
