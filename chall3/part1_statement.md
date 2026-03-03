# The Lost Recipe

## Part 1

It's Adel's turn to cook iftar for the crew tonight, and he has absolutely no idea what to make. Back home, he'd just pull up one of Oum Walid's legendary recipe videos and follow along. Her channel has never failed him. He fires up the ship's communication array, locks onto the broadcast frequency, and... nothing. The signal is gone.

The crew's communication engineer takes a look and delivers the bad news: the signal processing unit has crashed, and all that remains is a raw instruction log from the last working session. The unit runs on a stack-based architecture that operates on 32-bit unsigned integers (2^32 - 1), and the only way to bring it back online is to replay those instructions manually. If Adel can execute the full sequence and extract the correct output, the signal locks back in and Oum Walid's recipes are his.

The clock is ticking. Iftar is in a few hours. Time to process that stack.

### Input Format

Each line contains one instruction.

### Instructions

For all binary operations (sum, sub, xor, or, and, shl, shr), B is popped first (top of stack), then A (below it).

### Example

```
push 10
push 20
xor
push 5
sub
```

Output: If the final stack contains values [V1, V2, ..., Vk], output V1 XOR V2 XOR ... XOR Vk as a single integer.

### Example Walkthrough

```
push 10   → stack: [10]
push 20   → stack: [10, 20]
xor       → pop B=20, A=10. 10 XOR 20 = 30. stack: [30]
push 5    → stack: [30, 5]
sub       → pop B=5, A=30. 30 - 5 = 25. stack: [25]
```

What is the XOR-reduction of the final stack?
