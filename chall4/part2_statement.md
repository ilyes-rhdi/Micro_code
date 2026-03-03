# The Iftar Table

## Part 2

The signal is back, Oum Walid's recipe saved the day, and dinner was a hit. But the crew quickly realizes they need a better system for the rest of Ramadan. They agree on a rotation: each day, some crew members prepare iftar while the others keep the mission running. The problem? They all eat together around the ship's circular dining module, and the galley stations between seats are so tight that no two crew members seated next to each other can cook at the same time, they'd be elbowing each other in zero gravity.

Each crew member has a certain number of dishes they need to prepare over the course of Ramadan. Cooking happens in discrete rounds: each round, you choose a group of non-adjacent crew members, and each chosen person prepares exactly one dish. Adel needs to figure out the minimum number of rounds to get everything done.

### Input Format

- Line 1: A comma-separated list of positive integers representing the number of dishes each crew member must cook, in clockwise order around the table.
- Line 2: An integer K.
The table is circular: the first and last crew members are neighbors.

In each round, you choose a subset of non-adjacent crew members (no two neighbors may be chosen), and each chosen crew member prepares exactly one dish.

### Example

```
3,2,1,4,2
1
```

You must schedule optimally: in each round, choose any valid set of non-adjacent crew members who still have remaining dishes, and each prepares one dish.

Output: The minimum number of rounds as a single integer.

### Example Walkthrough

For 3,2,1,4,2, the answer is 6. One optimal schedule: round 1 {0,3}, round 2 {2,4}, round 3 {0,3}, round 4 {1,4}, round 5 {0,3}, round 6 {1,3}.

What is the minimum number of rounds?

Correct - 72 pts earnedYour Puzzle InputPart 2The schedule works for the first few days, but the crew quickly discovers a problem: cooking in zero gravity is exhausting. After preparing dishes in one round, each crew member needs time to recover before they can cook again.

Each crew member now has a cooldown: after cooking in a round, that crew member cannot cook again for the next K rounds (the value from line 2 of the input). This is in addition to the adjacency constraint during each round.

For example, if K = 1 and a crew member cooks in round 3, they are unavailable in round 4 but can cook again in round 5.

Find the minimum number of rounds needed for all crew members to finish all their dishes under both the adjacency constraint and the cooldown constraint.

Output: The minimum number of rounds as a single integer.

### Example Walkthrough

For 3,2,1,4,2 with K = 1, the answer is 7. Crew member 3 needs 4 cooking sessions and can cook at most every other round (rounds 1, 3, 5, 7), which is the bottleneck.

What is the minimum number of rounds with cooldown?
