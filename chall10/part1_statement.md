# The Last Transmission

## Part 1

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
