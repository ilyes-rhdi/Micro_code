# The Relay Chain

## Part 1

The radiation shields were armed and humming. Through the viewport, the blue curve of Earth filled half the sky now, and the crew could make out the coastline of the Mediterranean. But as they began pre-landing checks, the main flight computer locked up. A cascade failure in the communication bus had left the landing sequence controller unreachable — the only way to operate it was through a chain of emergency relay robots, each one controlling the next through a small directional pad.

"How many relays?" Adel asked, staring at the wiring diagram.

"At least two between us and the landing pad," the engineer replied. "Maybe more if we need the backup chain."

The bottom relay sat directly in front of the hexadecimal keypad that controlled the landing system. To arm the sequence, the crew needed to type a series of hex codes on that keypad — but they couldn't reach it directly. They had to send commands through the relay chain, each relay translating their directional inputs into movements on the next relay's keypad.

### Input Format

Multiple lines, each containing a code to type on the hex keypad.

Each code is exactly 4 characters: three uppercase hexadecimal digits followed by # (e.g., 1A3#, F00#). The # button confirms each code entry.

### Example Input

```
1A3#
F00#
B7E#
042#
D1C#
```

```
+---+---+---+
| 0 | 1 | 2 |
+---+---+---+
| 3 | 4 | 5 |
+---+---+---+
| 6 | 7 | 8 |
+---+---+---+
| 9 | A | B |
+---+---+---+
| C | D | E |
+---+---+---+
    | F | # |
    +---+---+
```

```
+---+---+
    | ^ | # |
+---+---+---+
| < | v | > |
+---+---+---+
```

To type a character: navigate the arm to the target key using directional moves (^, v, <, >), then press #.

The chain has 2 intermediate directional relays between you and the hex keypad (3 layers total). Find the minimum number of button presses you need to type each code through the full relay chain.

The complexity of a code is:

```
complexity = shortest_sequence_length × (hex_value_of_code + 1)
```

Output: The sum of complexities over all codes.

### Example

Answer: 802794.

What is the sum of complexities with the 2-relay chain?
