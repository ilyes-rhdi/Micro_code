# The Last Transmission

## Part 2

The work is done, and Lmkouli's people couldn't be more grateful. As a parting gift, Lmkouli presents the crew with something extraordinary: a time-traveling device, usable once every six months. The crew thanks them, boards the rocket, and sets course for their final mission objective.

They reach their destination, collect the scientific data Earth has been waiting for, and prepare to transmit it home. But there is a catch: Ramadan is almost over, and mission control needs this data before the holiday ends. The communication network between the ship and Earth is a massive web of directed relay stations. Signals can only travel one way through each link, and each link has a transmission cost. The network is organized into tightly connected relay clusters, chained together across deep space.

Adel needs to understand the structure of this network to route the data home. First, he must find the cheapest feedback loop in the system to calibrate the signal. Then, he needs to decompose the entire network into its relay clusters and find the longest chain through them to maximize signal strength. Every wasted cycle means the data might not arrive before Eid.

### Input Format

- Line 1: N M: number of nodes and number of edges.
- Lines 2 to M+1: A B W: a directed edge from node A to node B with weight W.
Nodes are labeled 0 to N-1. All weights are positive integers.

### Example

```
6 8
0 1 5
1 2 5
2 0 50
0 2 20
3 4 4
4 5 4
5 3 40
1 3 1
```

You are allowed to reverse (flip) the direction of at most one edge in the graph. Reversing an edge means replacing A -> B with B -> A while keeping the original weight W. The original edge A -> B is removed from the graph and only the reversed edge B -> A exists.

Correction on reversal mechanics: An earlier version of this problem stated that the original edge is removed during reversal. This has been updated. The reversal operation installs a backward relay link B->A(W) alongside the existing forward link A->B(W). Both edges coexist in the modified graph. When computing the shortest path that completes the cycle through the reversed edge, the original edge A->B remains available. The reversal adds connectivity; it does not reduce it.

A directed cycle is a path that starts and ends at the same node, following edge directions. Find the minimum total weight of any directed cycle in the graph after performing at most one reversal. You may also choose to reverse no edges.

Output: The minimum total weight of the directed cycle as a single integer.

### Example Walkthrough

Edges: 0->1(5), 1->2(5), 2->0(50), 0->2(20), 3->4(4), 4->5(4), 5->3(40), 1->3(1).

Step 1: Cycles without any reversal.

Every directed cycle uses only the original edge directions:

Minimum without reversal: 48.

Step 2: Cycles with one reversal.

For each edge, consider reversing it and check if a cycle exists through the reversed edge. When you reverse edge A->B(W), the reversed edge is B->A(W). To form a cycle, you need a path from A to B using the remaining edges (the original A->B is gone). The cycle weight is W (reversed edge) plus the path weight.

Best reversal cycle: reverse 0->2(20), cycle = 2->0(20) + 0->1->2(10) = 30.

Step 3: Overall minimum.

min(48, 30) = 30

Output: 30

What is the minimum total weight of a directed cycle after at most one edge reversal?

Correct - 80 pts earnedYour Puzzle InputPart 2With the cheapest calibration loop identified, Adel now turns to the bigger picture. The relay network is not one giant mesh. It is organized into tightly connected clusters. A cluster is a maximal group of nodes where every node can reach every other node by following directed edges. "Maximal" means you cannot add any more node to the group and keep this property. These clusters are called strongly connected components (SCCs).

To maximize signal strength across the full distance to Earth, he needs to decompose the network into these clusters and find the longest chain through them.

Decompose the relay network to find the strongest transmission chain.

- Find all SCCs: Partition the directed graph into strongly connected components. Each SCC is a maximal set of nodes where every pair of nodes can reach each other via directed paths.
- Compute SCC weights: For each SCC with 2 or more nodes, find the minimum-weight directed cycle contained entirely within that SCC. Use only the original edge directions (no reversals). This minimum cycle weight is the SCC's weight. If an SCC has only 1 node (no cycle possible), its weight is 0.
Clarification on SCC internal cycles: The same reversal logic from Part 1 applies within each SCC: you may reverse at most one internal edge per SCC when searching for the minimum cycle weight. This allows the calibration system to reroute one relay link per cluster for optimal loop efficiency. Restricting SCC cycle computation to unmodified edges only is a common implementation mistake that produces artificially inflated weights.

- Build the condensation DAG: Create a new directed acyclic graph where each node represents one SCC. Add a directed edge from SCC X to SCC Y if any original edge goes from a node in X to a node in Y (where X and Y are different SCCs). If multiple original edges connect the same pair of SCCs, keep only one edge in the condensation.
- Find the longest path: Find a path in the condensation DAG that passes through the maximum number of SCCs. A single SCC with no outgoing edges counts as a path of length 1. A path SCC A -> SCC B passes through 2 SCCs, SCC A -> SCC B -> SCC C passes through 3, and so on.
- Tie-break by weight sum: If multiple paths pass through the same number of SCCs, choose the one with the largest sum of SCC weights along the path.
Note on path weight computation: The total weight of a path includes both the SCC weights and the minimum-weight cross-component edges connecting consecutive SCCs along the path. Each condensation edge inherits the smallest weight among all original edges between those two components. A common implementation mistake is to sum only the SCC weights and omit the inter-cluster relay costs, which underestimates the true transmission chain weight.

- Output the total sum of SCC weights for the winning path.
Output: The total sum of SCC weights as a single integer.

### Example Walkthrough

Same input as Part 1:

```
6 8
0 1 5
1 2 5
2 0 50
0 2 20
3 4 4
4 5 4
5 3 40
1 3 1
```

Which nodes can reach each other following directed edges?

- Node 0 can reach 1 (via 0->1), and 2 (via 0->1->2 or 0->2).
- Node 1 can reach 0? Yes: 1->2->0. So 0 and 1 can reach each other.
- Node 2 can reach 0? Yes: 2->0. So {0, 1, 2} all reach each other. This is one SCC.
- Can any node in {0,1,2} reach node 3? Yes: 0->1->3. But can 3 reach back to 0? Node 3 leads to 3->4->5->3 (a cycle), but no edge from {3,4,5} leads to {0,1,2}. So 3 cannot reach 0.
- Nodes {3, 4, 5} all reach each other: 3->4->5->3. This is a second SCC.
Two SCCs:

- SCC A: {0, 1, 2}
- SCC B: {3, 4, 5}
Step 2: Compute SCC weights (minimum internal cycle, original directions, no reversals).

SCC A internal edges: 0->1(5), 1->2(5), 2->0(50), 0->2(20).

Minimum cycle in SCC A: 60

SCC B internal edges: 3->4(4), 4->5(4), 5->3(40).

Minimum cycle in SCC B: 48

Step 3: Build condensation DAG.

Check all edges for cross-SCC connections:

- Edge 1->3: node 1 is in SCC A, node 3 is in SCC B. Add edge SCC A -> SCC B.
- All other edges are internal to their SCC.
Condensation DAG: SCC A(weight=60) -> SCC B(weight=48).

Step 4: Find the longest path (maximum number of SCCs).

Longest path passes through 2 SCCs: SCC A -> SCC B.

Step 5: Sum of SCC weights along the winning path.

SCC A weight + SCC B weight = 60 + 48 = 108

Output: 108

What is the total sum of SCC weights along the longest relay chain?
