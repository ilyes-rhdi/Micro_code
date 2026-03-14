from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class Line:
    m: int
    b: int

    def value(self, x: int) -> int:
        return self.m * x + self.b


def is_bad(l1: Line, l2: Line, l3: Line) -> bool:
    # (b3 - b1)/(m1 - m3) <= (b2 - b1)/(m1 - m2)
    return (l3.b - l1.b) * (l1.m - l2.m) <= (l2.b - l1.b) * (l1.m - l3.m)


class ConvexHull:
    def __init__(self) -> None:
        self.lines: list[Line] = []
        self.ptr = 0

    def add(self, m: int, b: int) -> None:
        line = Line(m, b)
        lines = self.lines
        while len(lines) >= 2 and is_bad(lines[-2], lines[-1], line):
            lines.pop()
            if self.ptr > len(lines) - 1:
                self.ptr = len(lines) - 1
        lines.append(line)

    def query(self, x: int) -> int:
        lines = self.lines
        if not lines:
            raise RuntimeError("Hull is empty")
        while self.ptr + 1 < len(lines) and lines[self.ptr].value(x) >= lines[self.ptr + 1].value(x):
            self.ptr += 1
        return lines[self.ptr].value(x)


def min_total_stress(values: list[int], k: int, offset: int) -> int:
    n = len(values)
    prefix = [0] * (n + 1)
    for i, v in enumerate(values, 1):
        prefix[i] = prefix[i - 1] + v

    dp_prev = [0] * (n + 1)
    for i in range(1, n + 1):
        dp_prev[i] = (prefix[i] + offset) ** 2

    if k == 1:
        return dp_prev[n]

    for zones in range(2, k + 1):
        dp = [0] * (n + 1)
        hull = ConvexHull()

        j = zones - 1
        hull.add(-2 * prefix[j], dp_prev[j] + prefix[j] * prefix[j])

        for i in range(zones, n + 1):
            x = prefix[i] + offset
            best = hull.query(x)
            dp[i] = x * x + best
            hull.add(-2 * prefix[i], dp_prev[i] + prefix[i] * prefix[i])

        dp_prev = dp

    return dp_prev[n]


def main() -> None:
    input_path = Path(__file__).with_name("input.txt")
    raw = input_path.read_text(encoding="utf-8-sig").strip().split()
    n1, k1, n2, k2 = map(int, raw[:4])
    values = list(map(int, raw[4:]))

    part1_values = values[:n1]
    part2_values = values[:n2]

    # Part 1 matches the sample when using zero offset.
    part1 = min_total_stress(part1_values, k1, 0)
    part2 = min_total_stress(part2_values, k2, 0)

    print(part1)
    print(part2)


if __name__ == "__main__":
    main()
