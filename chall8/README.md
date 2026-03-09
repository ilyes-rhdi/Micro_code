# chall8

Challenge: The Healing Game  
Source: https://microcode.microclub.info/challenges/5d11b432-ca7e-4886-9311-c680b099697c

## Files
- `challenge_url.txt`: challenge URL
- `input.txt`: puzzle input
- `part1_statement.md`: Part 1 statement
- `part2_statement.md`: Part 2 statement
- `solve.py`: solver for both parts
- `part1_answer.txt`: saved Part 1 answer
- `part2_answer.txt`: saved Part 2 answer
- `fetch_part1_status.txt`: fetch status for Part 1
- `fetch_part2_status.txt`: fetch status for Part 2

## Approach
- Build all 4-cell winning lines (horizontal, vertical, both diagonals).
- Use minimax (perfect play) with memoization:
  - terminal scores: `+100` (you win), `-100` (opponent wins), `0` (depth limit or draw)
- Part 1:
  - evaluate each legal opening move, keep max score, tie-break by lowest position index.
- Part 2:
  - for each weighted hidden-piece scenario, inject opponent piece, apply loss/blocked checks, then simulate minimax from your move.
  - aggregate weighted totals, tie-break by lowest position index.

## Run
```bash
python chall8/solve.py --input chall8/input.txt --part 1
python chall8/solve.py --input chall8/input.txt --part 2
```

## Results
- Part 1: `43`
- Part 2: `47`
