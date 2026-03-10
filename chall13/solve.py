import argparse
from pathlib import Path

MOD = 1_000_000_009


def sum_squares(a: int, b: int) -> int:
    if a > b:
        a, b = b, a
    # S(n) = n(n+1)(2n+1)/6, so sum_{k=a..b} k^2 = S(b) - S(a-1)
    def s(n: int) -> int:
        return n * (n + 1) * (2 * n + 1) // 6

    return s(b) - s(a - 1)


def parse_op(line: str) -> tuple[int, int, int, int, int, int, int]:
    mode_str, ranges = line.split()
    xr, yr, zr = ranges.split(",")
    x1, x2 = map(int, xr.split(".."))
    y1, y2 = map(int, yr.split(".."))
    z1, z2 = map(int, zr.split(".."))
    return int(mode_str), x1, x2, y1, y2, z1, z2


def sum_step1(lo: int, hi: int) -> tuple[int, int]:
    if lo > hi:
        return 0, 0
    n = hi - lo + 1
    return n, sum_squares(lo, hi)


def sum_step2_even(lo: int, hi: int) -> tuple[int, int]:
    if lo > hi:
        return 0, 0
    first = lo if lo % 2 == 0 else lo + 1
    last = hi if hi % 2 == 0 else hi - 1
    if first > last:
        return 0, 0
    a = first // 2
    b = last // 2
    n = b - a + 1
    return n, 4 * sum_squares(a, b)


def axis_stats(lo: int, hi: int, step: int) -> tuple[int, int]:
    if step == 1:
        return sum_step1(lo, hi)
    return sum_step2_even(lo, hi)


def axis_intersection(a_lo: int, a_hi: int, a_step: int, b_lo: int, b_hi: int, b_step: int) -> tuple[int, int, int]:
    lo = max(a_lo, b_lo)
    hi = min(a_hi, b_hi)
    if lo > hi:
        return 0, -1, 1
    if a_step == 1 and b_step == 1:
        return lo, hi, 1
    # all step-2 axes are even-only in this challenge
    first = lo if lo % 2 == 0 else lo + 1
    last = hi if hi % 2 == 0 else hi - 1
    if first > last:
        return 0, -1, 1
    return first, last, 2


def energy_from_axes(x: tuple[int, int, int], y: tuple[int, int, int], z: tuple[int, int, int]) -> int:
    cx, sx2 = axis_stats(*x[:2], x[2])
    cy, sy2 = axis_stats(*y[:2], y[2])
    cz, sz2 = axis_stats(*z[:2], z[2])
    if cx == 0 or cy == 0 or cz == 0:
        return 0
    return sx2 * cy * cz + sy2 * cx * cz + sz2 * cx * cy


def build_desc(mode: int, x1: int, x2: int, y1: int, y2: int, z1: int, z2: int, replaced: bool) -> tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]]:
    x1, x2 = (x1, x2) if x1 <= x2 else (x2, x1)
    y1, y2 = (y1, y2) if y1 <= y2 else (y2, y1)
    z1, z2 = (z1, z2) if z1 <= z2 else (z2, z1)

    if replaced:
        return (x1, x2, 1), (y1, y2, 1), (z1, z2, 1)
    if mode == 0:
        return (-y2, -y1, 1), (x1, x2, 1), (z1, z2, 1)
    if mode == 1:
        return (2 * x1, 2 * x2, 2), (2 * y1, 2 * y2, 2), (2 * z1, 2 * z2, 2)
    return (z1, z2, 1), (y1, y2, 1), (x1, x2, 1)


def op_energy(desc: tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]]) -> int:
    return energy_from_axes(desc[0], desc[1], desc[2])


def intersection_energy(
    a: tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]],
    b: tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]],
) -> int:
    ix = axis_intersection(*a[0], *b[0])
    iy = axis_intersection(*a[1], *b[1])
    iz = axis_intersection(*a[2], *b[2])
    if ix[0] > ix[1] or iy[0] > iy[1] or iz[0] > iz[1]:
        return 0
    return energy_from_axes(ix, iy, iz)


def part1(lines: list[str]) -> int:
    m = int(lines[0].strip())
    total = 0

    for i in range(1, m + 1):
        mode, x1, x2, y1, y2, z1, z2 = parse_op(lines[i].strip())
        d = build_desc(mode, x1, x2, y1, y2, z1, z2, replaced=False)
        total = (total + op_energy(d)) % MOD

    return total


def parse_query(line: str) -> tuple[str, int, tuple[int, int, int, int, int, int] | None]:
    parts = line.split()
    typ = parts[0]
    idx = int(parts[1])
    if typ == "D":
        return typ, idx, None
    xr, yr, zr = parts[2].split(",")
    x1, x2 = map(int, xr.split(".."))
    y1, y2 = map(int, yr.split(".."))
    z1, z2 = map(int, zr.split(".."))
    return typ, idx, (x1, x2, y1, y2, z1, z2)


def enumerate_component_energy(comp: list[int], descs) -> int:
    seen_points: set[tuple[int, int, int]] = set()
    total = 0
    for idx in comp:
        (x1, x2, xs), (y1, y2, ys), (z1, z2, zs) = descs[idx]
        for x in range(x1, x2 + 1, xs):
            for y in range(y1, y2 + 1, ys):
                for z in range(z1, z2 + 1, zs):
                    p = (x, y, z)
                    if p in seen_points:
                        continue
                    seen_points.add(p)
                    total += x * x + y * y + z * z
    return total


def compute_unique_energy(active: list[bool], descs, energies) -> int:
    from collections import defaultdict, deque

    active_ids = [i for i, on in enumerate(active) if on]
    if not active_ids:
        return 0

    B = 256
    bins: dict[tuple[int, int, int], list[int]] = defaultdict(list)
    for idx in active_ids:
        (x1, x2, _), (y1, y2, _), (z1, z2, _) = descs[idx]
        for bx in range(x1 // B, x2 // B + 1):
            for by in range(y1 // B, y2 // B + 1):
                for bz in range(z1 // B, z2 // B + 1):
                    bins[(bx, by, bz)].append(idx)

    adj = [set() for _ in range(len(active))]
    inter_map: dict[tuple[int, int], int] = {}
    seen: set[tuple[int, int]] = set()

    for ids in bins.values():
        n = len(ids)
        for i in range(n):
            a = ids[i]
            da = descs[a]
            for j in range(i + 1, n):
                b = ids[j]
                key = (a, b) if a < b else (b, a)
                if key in seen:
                    continue
                seen.add(key)
                db = descs[b]
                ie = intersection_energy(da, db)
                if ie == 0:
                    continue
                adj[a].add(b)
                adj[b].add(a)
                inter_map[key] = ie

    visited = [False] * len(active)
    total = 0

    for i in active_ids:
        if visited[i]:
            continue
        if not adj[i]:
            visited[i] = True
            total += energies[i]
            continue

        comp: list[int] = []
        q = deque([i])
        visited[i] = True
        while q:
            u = q.popleft()
            comp.append(u)
            for v in adj[u]:
                if not visited[v]:
                    visited[v] = True
                    q.append(v)

        if len(comp) == 2:
            a, b = comp[0], comp[1]
            key = (a, b) if a < b else (b, a)
            total += energies[a] + energies[b] - inter_map[key]
        else:
            total += enumerate_component_energy(comp, descs)

    return total % MOD


def part2(lines: list[str]) -> int:
    m = int(lines[0].strip())

    modes: list[int] = [0] * m
    descs: list[tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]]] = []
    energies = [0] * m
    active = [True] * m

    for i in range(m):
        mode, x1, x2, y1, y2, z1, z2 = parse_op(lines[1 + i].strip())
        modes[i] = mode
        d = build_desc(mode, x1, x2, y1, y2, z1, z2, replaced=False)
        descs.append(d)
        energies[i] = op_energy(d)

    q = int(lines[m + 1].strip())
    queries = [parse_query(lines[m + 2 + i].strip()) for i in range(q)]

    ans = 0
    for typ, idx1, repl in queries:
        i = idx1
        if 0 <= i < m:
            if typ == "D":
                active[i] = False
            else:
                x1, x2, y1, y2, z1, z2 = repl  # type: ignore[misc]
                d = build_desc(modes[i], x1, x2, y1, y2, z1, z2, replaced=False)
                descs[i] = d
                energies[i] = op_energy(d)

        current = compute_unique_energy(active, descs, energies)
        ans = (ans + current) % MOD

    return ans


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="input.txt")
    parser.add_argument("--part", type=int, default=2)
    args = parser.parse_args()

    lines = Path(args.input).read_text(encoding="utf-8").splitlines()
    if args.part == 1:
        print(part1(lines))
    else:
        print(part2(lines))


if __name__ == "__main__":
    main()
