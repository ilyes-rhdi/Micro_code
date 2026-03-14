from __future__ import annotations

import sys
from heapq import heappop, heappush

# Toggle if the judge uses (hex_value + 1) instead of hex_value.
USE_PLUS_ONE = False

# Keypad layouts
HEX = {
    "0": (0, 0), "1": (1, 0), "2": (2, 0),
    "3": (0, 1), "4": (1, 1), "5": (2, 1),
    "6": (0, 2), "7": (1, 2), "8": (2, 2),
    "9": (0, 3), "A": (1, 3), "B": (2, 3),
    "C": (0, 4), "D": (1, 4), "E": (2, 4),
    "F": (1, 5), "#": (2, 5),
}

DIR_STANDARD = {
    "^": (1, 0), "#": (2, 0),
    "<": (0, 1), "v": (1, 1), ">": (2, 1),
}

DIR_MIRRORED = {
    "<": (0, 0), "^": (1, 0), "#": (2, 0),
    "v": (0, 1), ">": (1, 1),
}

MOVES = {
    "^": (0, -1),
    "v": (0, 1),
    "<": (-1, 0),
    ">": (1, 0),
}


def build_transition_costs(keypad: dict[str, tuple[int, int]], prev_cost: dict[str, dict[str, int]]) -> dict[str, dict[str, int]]:
    pos_to_btn = {pos: btn for btn, pos in keypad.items()}
    buttons = list(keypad.keys())
    controller_buttons = list(prev_cost.keys())
    inf = 10**30

    out: dict[str, dict[str, int]] = {src: {} for src in buttons}

    for src in buttons:
        start_state = (src, "#")
        dist = {start_state: 0}
        pq = [(0, src, "#")]

        while pq:
            cur_dist, cur_btn, last_controller_btn = heappop(pq)
            if cur_dist != dist.get((cur_btn, last_controller_btn), inf):
                continue

            x, y = keypad[cur_btn]
            for move_btn, (dx, dy) in MOVES.items():
                nx, ny = x + dx, y + dy
                if (nx, ny) not in pos_to_btn:
                    continue
                nxt_btn = pos_to_btn[(nx, ny)]
                nd = cur_dist + prev_cost[last_controller_btn][move_btn]
                state = (nxt_btn, move_btn)

                if nd < dist.get(state, inf):
                    dist[state] = nd
                    heappush(pq, (nd, nxt_btn, move_btn))

        for dst in buttons:
            best = inf
            for last_controller_btn in controller_buttons:
                d = dist.get((dst, last_controller_btn))
                if d is None:
                    continue
                best = min(best, d + prev_cost[last_controller_btn]["#"])
            out[src][dst] = best

    return out


def build_dir_costs(num_relays: int, dir_layout: dict[str, tuple[int, int]]) -> dict[str, dict[str, int]]:
    dir_buttons = list(dir_layout.keys())
    cost = {a: {b: 1 for b in dir_buttons} for a in dir_buttons}

    for _ in range(num_relays):
        cost = build_transition_costs(dir_layout, cost)

    return cost


def total_complexity(codes: list[str], num_relays: int, dir_layout: dict[str, tuple[int, int]], plus_one: bool) -> int:
    dir_cost = build_dir_costs(num_relays, dir_layout)
    hex_cost = build_transition_costs(HEX, dir_cost)

    total = 0
    for code in codes:
        code = code.strip()
        if not code:
            continue

        presses = 0
        cur = "#"
        for ch in code:
            presses += hex_cost[cur][ch]
            cur = ch

        value = int(code[:-1], 16)
        if plus_one:
            value += 1

        total += presses * value

    return total


def main() -> None:
    codes = [line.strip() for line in sys.stdin if line.strip()]
    if not codes:
        return

    part1 = total_complexity(codes, num_relays=2, dir_layout=DIR_STANDARD, plus_one=USE_PLUS_ONE)
    part2 = total_complexity(codes, num_relays=25, dir_layout=DIR_MIRRORED, plus_one=USE_PLUS_ONE)

    print(part1)
    print(part2)


if __name__ == "__main__":
    main()
