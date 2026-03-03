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


def extract_stable_bits(lines: list[str]) -> tuple[int, list[int]]:
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

    return stable_count, bits


def compute_power(lines: list[str]) -> int:
    stable_count, bits = extract_stable_bits(lines)

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


def smallest_period(values: list[int]) -> int:
    n = len(values)
    if n == 0:
        return 0

    divisors = [d for d in range(1, n + 1) if n % d == 0]
    for d in divisors:
        ok = True
        for i in range(n):
            if values[i] != values[i % d]:
                ok = False
                break
        if ok:
            return d
    return n


def compute_entropy(lines: list[str]) -> int:
    _, bits = extract_stable_bits(lines)
    n = len(bits)
    if n < 5:
        return 0

    mutated: list[int] = []
    for i in range(n - 4):
        b0, b1, b2, b3, b4 = bits[i], bits[i + 1], bits[i + 2], bits[i + 3], bits[i + 4]
        w = b0 * 16 + b1 * 8 + b2 * 4 + b3 * 2 + b4
        if w % 3 == 0:
            mutated.append(1)
        elif w % 5 == 0:
            mutated.append(0)
        else:
            mutated.append((b0 + b1 + b2 + b3 + b4) % 2)

    period = smallest_period(mutated)
    pos_sum = 0
    for i, v in enumerate(mutated):
        if v == 1:
            pos_sum += i + 1

    return pos_sum * period


def main() -> None:
    input_path = Path(__file__).with_name("input.txt")
    lines = input_path.read_text(encoding="utf-8-sig").splitlines()
    print(compute_entropy(lines))


if __name__ == "__main__":
    main()
