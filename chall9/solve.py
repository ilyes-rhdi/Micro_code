from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import argparse


@dataclass
class Puzzle:
    target: int
    word: str
    matrix: list[str]


def parse_input(path: Path) -> Puzzle:
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    if len(lines) < 4:
        raise ValueError("Invalid input: too short")
    if not lines[0].startswith("TARGET:"):
        raise ValueError("Invalid input: missing TARGET")
    if not lines[1].startswith("WORD:"):
        raise ValueError("Invalid input: missing WORD")
    target = int(lines[0].split(":", 1)[1].strip())
    word = lines[1].split(":", 1)[1].strip()
    matrix = lines[3:]
    if not matrix:
        raise ValueError("Invalid input: empty MATRIX")
    cols = len(matrix[0])
    if any(len(r) != cols for r in matrix):
        raise ValueError("Invalid input: non-rectangular matrix")
    return Puzzle(target=target, word=word, matrix=matrix)


def shift_bits(bits: int, delta: int, mask: int) -> int:
    if bits == 0:
        return 0
    if delta >= 0:
        return (bits << delta) & mask
    return bits >> (-delta)


def solve_part1_with_path(p: Puzzle) -> tuple[int, list[tuple[int, int]]]:
    rows = len(p.matrix)
    cols = len(p.matrix[0])
    word = p.word
    l = len(word)

    max_pos = l * (rows - 1)
    max_neg = l * (cols - 1)
    offset = max_neg
    width = max_pos + max_neg + 1
    mask = (1 << width) - 1

    by_char_col: dict[str, list[list[int]]] = {}
    for r, row in enumerate(p.matrix):
        for c, ch in enumerate(row):
            cols_list = by_char_col.get(ch)
            if cols_list is None:
                cols_list = [[] for _ in range(cols)]
                by_char_col[ch] = cols_list
            cols_list[c].append(r)

    for ch in set(word):
        if ch not in by_char_col:
            raise ValueError(f"Character {ch!r} not found in matrix")

    layers: list[list[int]] = []

    for i, ch in enumerate(word):
        cur = [0] * cols
        char_cols = by_char_col[ch]

        if i == 0:
            base_by_col = [1 << offset] * cols
        else:
            prev = layers[-1]
            base_by_col = [0] * cols
            acc = 0
            for c in range(cols):
                base_by_col[c] = acc
                acc |= prev[c]

        for c in range(cols):
            rows_here = char_cols[c]
            if not rows_here:
                continue
            base = base_by_col[c]
            if base == 0:
                continue
            bits = 0
            for r in rows_here:
                bits |= shift_bits(base, r - c, mask)
            cur[c] = bits

        if not any(cur):
            raise RuntimeError(f"No valid states at step {i}")
        layers.append(cur)

    target_bit = 1 << (p.target + offset)
    end_col = -1
    for c, bits in enumerate(layers[-1]):
        if bits & target_bit:
            end_col = c
            break
    if end_col < 0:
        raise RuntimeError("No solution reaches target checksum")

    path: list[tuple[int, int]] = [(-1, -1)] * l
    need_sum = p.target
    cur_col = end_col

    for i in range(l - 1, -1, -1):
        ch = word[i]
        rows_here = by_char_col[ch][cur_col]

        if i == 0:
            chosen_r = -1
            for r in rows_here:
                if need_sum == (r - cur_col):
                    chosen_r = r
                    break
            if chosen_r < 0:
                raise RuntimeError("Backtracking failed at first character")
            path[i] = (chosen_r, cur_col)
            break

        prev_layer = layers[i - 1]
        prefix_or = [0] * cols
        acc = 0
        for c in range(cols):
            prefix_or[c] = acc
            acc |= prev_layer[c]

        chosen_r = -1
        prev_needed = 0
        for r in rows_here:
            s_prev = need_sum - (r - cur_col)
            bit_idx = s_prev + offset
            if bit_idx < 0 or bit_idx >= width:
                continue
            if prefix_or[cur_col] & (1 << bit_idx):
                chosen_r = r
                prev_needed = s_prev
                break

        if chosen_r < 0:
            raise RuntimeError(f"Backtracking failed at index {i}")

        prev_col = -1
        bit = 1 << (prev_needed + offset)
        for c in range(cur_col - 1, -1, -1):
            if prev_layer[c] & bit:
                prev_col = c
                break
        if prev_col < 0:
            raise RuntimeError(f"Could not find predecessor column at index {i}")

        path[i] = (chosen_r, cur_col)
        need_sum = prev_needed
        cur_col = prev_col

    checksum = sum(r - c for r, c in path)
    if checksum != p.target:
        raise RuntimeError(f"Checksum mismatch: got {checksum}, expected {p.target}")

    part1_hash = sum((r + 1) * (c + 1) for r, c in path)
    return part1_hash, path


def toroidal_dist(r1: int, c1: int, r2: int, c2: int, rows: int, cols: int) -> int:
    dr = abs(r1 - r2)
    dc = abs(c1 - c2)
    return min(dr, rows - dr) + min(dc, cols - dc)


def solve_part2(p: Puzzle, path: list[tuple[int, int]]) -> int:
    rows = len(p.matrix)
    cols = len(p.matrix[0])

    positions_by_char: dict[str, list[tuple[int, int]]] = {}
    for r, row in enumerate(p.matrix):
        for c, ch in enumerate(row):
            positions_by_char.setdefault(ch, []).append((r, c))

    payload: list[str] = []
    for r0, c0 in path:
        ch = p.matrix[r0][c0]
        # Guaranteed by the statement's construction.
        if c0 == 0 or c0 == cols - 1:
            raise RuntimeError("Part 1 coordinate is on border column; invalid input construction")

        best: tuple[int, int, int] | None = None
        for r, c in positions_by_char[ch]:
            if r == r0 and c == c0:
                continue
            key = (toroidal_dist(r0, c0, r, c, rows, cols), r, c)
            if best is None or key < best:
                best = key

        if best is None:
            raise RuntimeError(f"No twin found for char {ch!r} at {(r0, c0)}")

        _, tr, tc = best
        payload.append(p.matrix[tr][tc - 1])
        payload.append(p.matrix[tr][tc + 1])

    total = 0
    for i, ch in enumerate(payload, start=1):
        total += ord(ch) * i
    return total


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve challenge 19")
    parser.add_argument("--input", default="input.txt", help="Path to input.txt")
    parser.add_argument("--part", type=int, choices=[1, 2], default=1, help="Part to solve")
    args = parser.parse_args()

    puzzle = parse_input(Path(args.input))
    ans1, path = solve_part1_with_path(puzzle)
    if args.part == 1:
        print(ans1)
    else:
        print(solve_part2(puzzle, path))


if __name__ == "__main__":
    main()
