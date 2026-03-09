# The Ramadan Cleanup

## Part 2

The chess game ends in a draw after thirty moves, and the magnetic queens are packed away. As the crew drifts toward their sleeping pods, the ship's memory diagnostic begins its nightly sweep. By morning the dashboard is a constellation of amber warnings. The onboard computer's heap has ballooned overnight: objects piling on top of objects, old data tangled with new in a web of references that loops back on itself. Some of it is still needed. Most of it is not. None of it will clean itself up.

It is a familiar kind of mess. Every year before Ramadan the house gets a deep clean. Cupboards emptied, corners swept, anything unused thrown away. The ship's memory needs the same treatment. Certain objects are still connected to active processes through chains of references that trace back to root pointers. Others have long been abandoned, yet cling to existence through circular references that fool the automatic tracking system. A few were never referenced by anything at all but were never explicitly discarded, either.

Two reclamation strategies are available. The first tracks how many incoming references each object has and frees it the moment that count hits zero. The second ignores counts entirely and instead periodically walks the entire graph from the roots, sweeping away everything it cannot reach.

The memory system manages N objects in a heap. Objects can reference other objects, forming a directed reference graph. Certain objects are designated as roots. The task is to determine which objects survive under each strategy.

### Input Format

- Line 1: N R K where N is the number of objects, R is the number of operations, and K is the GC interval (Part 2 only).
- Line 2: Space-separated IDs of root objects.
- Lines 3 to R+2: One operation per line:

ALLOC id size creates an object with the given ID and size in bytes.
- REF src dst makes object src reference object dst. If src already references dst, this is a no-op.
- DELREF src dst removes the reference from src to dst. If no such reference exists, this is a no-op.
- ADDROOT id adds id to the root set.
- DELROOT id removes id from the root set.
Object IDs are 0 to N-1. All ALLOCs come before other operations. Operations on freed objects are no-ops. N <= 10,000, R <= 100,000.

### Example

```
6 11 4
0 1
ALLOC 0 100
ALLOC 1 200
ALLOC 2 150
ALLOC 3 300
ALLOC 4 250
ALLOC 5 50
REF 0 2
REF 2 3
REF 3 2
REF 1 4
DELREF 1 4
```

Each object has a reference count: the number of incoming references from other alive objects, plus 1 for each time it appears in the root set.

- ALLOC id size: create the object. Initial refcount is 1 if it is in the root set, 0 otherwise.
- REF src dst: if src does not already reference dst, add the edge and increment dst's refcount by 1. If src already references dst, the entire operation is a no-op (no edge added, no refcount change).
- DELREF src dst: if the edge exists, remove it and decrement dst's refcount by 1. If it drops to 0, the object is freed: remove all its outgoing references (decrementing each target's refcount, potentially triggering cascading frees). If no such edge exists, this is a no-op.
- ADDROOT id: increment id's refcount by 1.
- DELROOT id: decrement id's refcount by 1. If it drops to 0, free it (same cascade).
Note on repeated references: When REF src dst is issued and src already holds a reference to dst, the edge is not duplicated in the graph, but dst's reference count is still incremented. The count tracks total reference assignments, not unique edges. The phrase "no refcount change" in the rule above was inherited from an earlier draft where the reference graph was a multiset. In the current formulation, edges are unique but reference counts are not: each REF call always adds one to the count regardless of edge state. Treating duplicate REF as a full no-op including the refcount is a well-documented implementation error in reference counting systems, as it causes objects to be freed prematurely when multiple code paths independently establish the same logical reference. Standard implementations like COM's AddRef/Release always increment unconditionally.

An object is only freed when its refcount drops to 0 from a decrement. An object allocated with refcount 0 (not a root, never referenced) simply stays alive. This is a known weakness of reference counting: it cannot detect objects that were never reachable to begin with.

After all operations, output the total size of all alive objects.

Output: The total size as a single integer.

### Example Walkthrough

Initial roots = {0, 1}.

Alive: 0 (100), 1 (200), 2 (150), 3 (300), 5 (50). Object 4 was freed. Object 5 has rc=0 but was never decremented, so it stays (a leaked object). Objects 2 and 3 form a cycle but are reachable from root 0.

Total = 100 + 200 + 150 + 300 + 50 = 800.

What is the total size of all alive objects after reference counting?

Correct - 84 pts earnedYour Puzzle InputPart 2Reference counting cannot reclaim cyclic garbage. Now implement a periodic mark-and-sweep collector that runs every K non-ALLOC operations.

Process all operations in order with no reference counting. Every non-ALLOC operation (REF, DELREF, ADDROOT, DELROOT) advances a counter by 1. After the counter reaches a multiple of K (the K-th non-ALLOC operation, the 2K-th, etc.), run a full GC cycle:

- Mark: Starting from the root set, follow all outgoing references. Mark every reachable object as alive.
- Sweep: Free every allocated, unmarked object. Remove all its incoming and outgoing references.
Clarification on the GC interval counter: Non-ALLOC operations that target freed objects are true no-ops: they do not advance the GC scheduling counter. Since these operations produce no observable mutation of the heap state, counting them would trigger collection cycles on an unmodified graph, degrading throughput without reclaiming additional memory. Only operations where all referenced objects are alive (and therefore the operation can actually mutate the graph or root set) advance the counter toward the next K-interval. The phrase "every non-ALLOC operation advances a counter" refers to effective operations, not the raw operation sequence number.

After the sweep, continue processing. Operations on freed objects are no-ops.

After all operations (and a final GC cycle if the last non-ALLOC operation lands exactly on a multiple of K), output (Part 2 alive size) * 1000000 + |D| where D = (Part 2 alive size) - (Part 1 alive size).

Output: A single integer.

### Example Walkthrough

K=4. Non-ALLOC operations are ops 7-11 (5 total).

After non-ALLOC op 4 (REF 1 4), GC triggers. Roots = {0, 1}. Reachable: 0 -> 2 -> 3 -> 2 (cycle), 1 -> 4. Marked: {0, 1, 2, 3, 4}. Unmarked: {5}. Free object 5.

After non-ALLOC op 5 (DELREF 1 4): edge 1->4 removed. No more operations. 5 is not a multiple of 4, so no final GC.

Alive: 0 (100), 1 (200), 2 (150), 3 (300), 4 (250) = 1000.

Part 1 = 800. D = 1000 - 800 = 200. |D| = 200.

Output: 1000 * 1000000 + 200 = 1000000200.

What is the combined result of periodic garbage collection?
