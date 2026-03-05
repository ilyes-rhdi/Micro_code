from __future__ import annotations

import argparse
from functools import lru_cache
from pathlib import Path


def parse_input(path: Path):
    lines = [line.rstrip("\n") for line in path.read_text(encoding="utf-8-sig").splitlines() if line.strip()]
    header = lines[0]
    n_s, my_sym, depth_s, weights_s = header.split(";")
    n = int(n_s)
    depth = int(depth_s)
    board = [list(row) for row in lines[1:1 + n]]

    opp = "O" if my_sym == "X" else "X"

    weights: list[tuple[int, int, int]] = []
    if weights_s:
        for chunk in weights_s.split("|"):
            w_s, rc = chunk.split("-", 1)
            r_s, c_s = rc.split(",", 1)
            weights.append((int(w_s), int(r_s), int(c_s)))

    return n, my_sym, opp, depth, weights, board


def build_lines(n: int):
    lines = []
    # Horizontal
    for r in range(n):
        for c in range(n - 3):
            lines.append(tuple(r * n + (c + k) for k in range(4)))
    # Vertical
    for c in range(n):
        for r in range(n - 3):
            lines.append(tuple((r + k) * n + c for k in range(4)))
    # Diagonal down-right
    for r in range(n - 3):
        for c in range(n - 3):
            lines.append(tuple((r + k) * n + (c + k) for k in range(4)))
    # Diagonal down-left
    for r in range(n - 3):
        for c in range(3, n):
            lines.append(tuple((r + k) * n + (c - k) for k in range(4)))
    return lines


def has_win(board_s: str, sym: str, lines4: list[tuple[int, int, int, int]]) -> bool:
    for a, b, c, d in lines4:
        if board_s[a] == sym and board_s[b] == sym and board_s[c] == sym and board_s[d] == sym:
            return True
    return False


def empty_positions(board_s: str):
    return [i for i, ch in enumerate(board_s) if ch == "."]


def solve_part1(n: int, me: str, opp: str, depth: int, board_s: str, lines4):
    @lru_cache(maxsize=None)
    def minimax(state: str, turn_is_me: bool, rem: int) -> int:
        if has_win(state, me, lines4):
            return 100
        if has_win(state, opp, lines4):
            return -100
        empties = empty_positions(state)
        if rem == 0 or not empties:
            return 0

        if turn_is_me:
            best = -101
            for pos in empties:
                nxt = state[:pos] + me + state[pos + 1 :]
                val = minimax(nxt, False, rem - 1)
                if val > best:
                    best = val
                    if best == 100:
                        break
            return best

        best = 101
        for pos in empties:
            nxt = state[:pos] + opp + state[pos + 1 :]
            val = minimax(nxt, True, rem - 1)
            if val < best:
                best = val
                if best == -100:
                    break
        return best

    best_move = -1
    best_val = -10**18
    for pos in empty_positions(board_s):
        after = board_s[:pos] + me + board_s[pos + 1 :]
        val = minimax(after, False, depth - 1)
        if val > best_val or (val == best_val and pos < best_move):
            best_val = val
            best_move = pos

    return best_move


def solve_part2(n: int, me: str, opp: str, depth: int, weights, board_s: str, lines4):
    @lru_cache(maxsize=None)
    def minimax(state: str, turn_is_me: bool, rem: int) -> int:
        if has_win(state, me, lines4):
            return 100
        if has_win(state, opp, lines4):
            return -100
        empties = empty_positions(state)
        if rem == 0 or not empties:
            return 0

        if turn_is_me:
            best = -101
            for pos in empties:
                nxt = state[:pos] + me + state[pos + 1 :]
                val = minimax(nxt, False, rem - 1)
                if val > best:
                    best = val
                    if best == 100:
                        break
            return best

        best = 101
        for pos in empties:
            nxt = state[:pos] + opp + state[pos + 1 :]
            val = minimax(nxt, True, rem - 1)
            if val < best:
                best = val
                if best == -100:
                    break
        return best

    candidates = empty_positions(board_s)
    best_move = -1
    best_total = -10**18

    for pos in candidates:
        total = 0
        for w, r, c in weights:
            hp = r * n + c
            # Hidden piece already placed by opponent for this scenario.
            if board_s[hp] != ".":
                # If statement guarantees valid scenarios this won't happen; keep safe behavior.
                scenario_board = board_s
            else:
                scenario_board = board_s[:hp] + opp + board_s[hp + 1 :]

            if has_win(scenario_board, opp, lines4):
                total += w * (-100)
                continue

            if pos == hp:
                total += w * (-100)
                continue

            if scenario_board[pos] != ".":
                total += w * (-100)
                continue

            after = scenario_board[:pos] + me + scenario_board[pos + 1 :]
            val = minimax(after, False, depth - 1)
            total += w * val

        if total > best_total or (total == best_total and pos < best_move):
            best_total = total
            best_move = pos

    return best_move


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve The Healing Game")
    parser.add_argument("--input", default="input.txt")
    parser.add_argument("--part", type=int, choices=[1, 2], default=1)
    args = parser.parse_args()

    n, me, opp, depth, weights, board = parse_input(Path(args.input))
    board_s = "".join("".join(row) for row in board)
    lines4 = build_lines(n)

    if args.part == 1:
        print(solve_part1(n, me, opp, depth, board_s, lines4))
    else:
        print(solve_part2(n, me, opp, depth, weights, board_s, lines4))


if __name__ == "__main__":
    main()
