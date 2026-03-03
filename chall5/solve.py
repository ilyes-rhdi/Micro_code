from __future__ import annotations

import math
import re
from pathlib import Path

LINE_RE = re.compile(r"^\s*([+-]?\d+)\s*\|\s*([A-Z])\s*:\s*([A-Z])\s*$")


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    if n % 3 == 0:
        return n == 3
    i = 5
    w = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += w
        w = 6 - w
    return True


def compute_power(lines: list[str]) -> int:
    stable_count = 0
    bits: list[int] = []

    for raw in lines:
        if not raw.strip():
            continue
        m = LINE_RE.match(raw)
        if not m:
            raise ValueError(f"Invalid line format: {raw!r}")

        value_s, mode_s, mode_r = m.groups()
        if mode_s != mode_r:
            continue

        stable_count += 1
        value = abs(int(value_s))
        if value == 0:
            continue
        bits.append(1 if is_prime(value) else 0)

    n = len(bits)
    if n == 0:
        return 0

    shift = stable_count % 7
    power = 0

    for i, bit in enumerate(bits, start=1):
        e = ((i + shift - 1) % n) + 1
        if bit == 1:
            power += e * e
        else:
            power -= math.gcd(e, n)

    return power


def main() -> None:
    input_path = Path(__file__).with_name("input.txt")
    lines = input_path.read_text(encoding="utf-8-sig").splitlines()
    print(compute_power(lines))


if __name__ == "__main__":
    main()
