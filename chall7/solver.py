from __future__ import annotations

import argparse
from pathlib import Path


def parse_input(path: Path) -> tuple[int, list[int]]:
    lines = [ln.strip() for ln in path.read_text(encoding="utf-8-sig").splitlines() if ln.strip()]
    p = int(lines[0])
    seq = [int(x, 2) for x in lines[1:]]
    if len(seq) != 4 * p:
        raise ValueError("Invalid input: expected 4 sequences per group")
    return p, seq


def reverse8(x: int) -> int:
    out = 0
    for i in range(8):
        out = (out << 1) | ((x >> i) & 1)
    return out


def solve_part1(path: Path) -> int:
    p, seq = parse_input(path)
    total = 0
    idx = 0

    for _ in range(p):
        arr = seq[idx : idx + 4]
        idx += 4

        for g in range(1, 1001):
            strengths = [x.bit_count() for x in arr]
            order = sorted(range(4), key=lambda i: (strengths[i], i), reverse=True)
            first_i, second_i = order[0], order[1]

            first = arr[first_i]
            second = arr[second_i]
            s_first = strengths[first_i]
            s_second = strengths[second_i]

            split = (s_first + s_second) % 7 + 1
            right = 8 - split
            high_mask = ((1 << split) - 1) << right
            low_mask = (1 << right) - 1

            off1 = (first & high_mask) | (second & low_mask)
            off2 = (second & high_mask) | (first & low_mask)

            strike = (g * 3 + s_first) % 8
            bit = 1 << (7 - strike)  # position 0 is leftmost
            off1 ^= bit
            off2 ^= bit

            new_arr = [first, second, off1, off2]
            rot = g % 4
            if rot:
                new_arr = new_arr[-rot:] + new_arr[:-rot]
            arr = new_arr

            total += sum(arr)

    return total


def solve_part2(path: Path) -> int:
    p, seq = parse_input(path)
    total = 0
    idx = 0

    for _ in range(p):
        arr = seq[idx : idx + 4]
        idx += 4
        ref = int("11010110", 2)

        for g in range(1, 1001):
            if g % 100 == 0:
                ref = ((ref << 1) & 0xFF) | ((ref >> 7) & 1)
                ref ^= 1 << (7 - 2)
                ref ^= 1 << (7 - 5)
            if g % 250 == 0:
                ref = reverse8(ref)

            resemblance = [8 - ((x ^ ref).bit_count()) for x in arr]
            order = sorted(range(4), key=lambda i: (resemblance[i], i), reverse=True)
            first_i, second_i = order[0], order[1]

            first = arr[first_i]
            second = arr[second_i]
            r_first = resemblance[first_i]
            r_second = resemblance[second_i]

            if ref.bit_count() > 4:
                split = (r_first + r_second + 2) % 7 + 1
            else:
                split = (r_first + r_second) % 7 + 1

            right = 8 - split
            high_mask = ((1 << split) - 1) << right
            low_mask = (1 << right) - 1

            off1 = (first & high_mask) | (second & low_mask)
            off2 = (second & high_mask) | (first & low_mask)

            strike = (g * 3 + r_first) % 8
            bit = 1 << (7 - strike)
            off1 ^= bit
            off2 ^= bit

            new_arr = [first, second, off1, off2]
            rot = g % 4
            if rot:
                new_arr = new_arr[-rot:] + new_arr[:-rot]
            arr = new_arr

            total += sum(arr)

    return total


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve chall7")
    parser.add_argument("--part", choices=["1", "2", "both"], default="both")
    args = parser.parse_args()

    input_path = Path(__file__).with_name("input.txt")
    if args.part in {"1", "both"}:
        print(solve_part1(input_path))
    if args.part in {"2", "both"}:
        print(solve_part2(input_path))


if __name__ == "__main__":
    main()

