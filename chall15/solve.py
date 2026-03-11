import argparse
from array import array
from pathlib import Path

MOD = 1_000_000_009
BASE = 31
MASK64 = (1 << 64) - 1
HASH_BASE = 911382323


def manacher(s: str) -> tuple[list[int], list[int]]:
    n = len(s)
    d1 = [0] * n
    l = 0
    r = -1
    for i in range(n):
        k = 1 if i > r else min(d1[l + r - i], r - i + 1)
        while i - k >= 0 and i + k < n and s[i - k] == s[i + k]:
            k += 1
        d1[i] = k
        if i + k - 1 > r:
            l = i - k + 1
            r = i + k - 1

    d2 = [0] * n
    l = 0
    r = -1
    for i in range(n):
        k = 0 if i > r else min(d2[l + r - i + 1], r - i + 1)
        while i - k - 1 >= 0 and i + k < n and s[i - k - 1] == s[i + k]:
            k += 1
        d2[i] = k
        if i + k - 1 > r:
            l = i - k
            r = i + k - 1

    return d1, d2


def is_palindrome(l: int, r: int, d1: list[int], d2: list[int]) -> int:
    length = r - l + 1
    if length & 1:
        center = (l + r) // 2
        return 1 if d1[center] >= (length // 2 + 1) else 0
    half = length // 2
    center = l + half
    return 1 if d2[center] >= half else 0


def solve_part1_from_file(input_path: Path) -> int:
    with input_path.open("rb") as f:
        n, q, k = map(int, f.readline().split())
        s = f.readline().strip().decode("ascii")

        d1, d2 = manacher(s)

        checksum = 0
        last_ans = 0
        p = BASE

        for _ in range(q):
            line = f.readline()
            while line and not line.strip():
                line = f.readline()
            if not line:
                break

            a, b = map(int, line.split())

            key = last_ans * k
            l_raw = a ^ key
            r_raw = b ^ key

            if l_raw < 1:
                l_raw = 1
            elif l_raw > n:
                l_raw = n

            if r_raw < 1:
                r_raw = 1
            elif r_raw > n:
                r_raw = n

            if l_raw > r_raw:
                l_raw, r_raw = r_raw, l_raw

            if ((l_raw + r_raw) % 3) == 0:
                span_q = (r_raw - l_raw) // 4
                l_raw += span_q
                r_raw -= span_q

            ans = is_palindrome(l_raw - 1, r_raw - 1, d1, d2)
            last_ans = ans

            if ans:
                checksum = (checksum + p) % MOD
            p = (p * BASE) % MOD

    return checksum


class Fenwick64:
    def __init__(self, n: int):
        self.n = n
        self.bit = array("Q", [0]) * (n + 1)

    def add(self, idx: int, delta: int) -> None:
        n = self.n
        bit = self.bit
        delta &= MASK64
        while idx <= n:
            bit[idx] = (bit[idx] + delta) & MASK64
            idx += idx & -idx

    def prefix(self, idx: int) -> int:
        res = 0
        bit = self.bit
        while idx > 0:
            res = (res + bit[idx]) & MASK64
            idx -= idx & -idx
        return res

    def range_sum(self, left: int, right: int) -> int:
        return (self.prefix(right) - self.prefix(left - 1)) & MASK64


def is_prime(x: int) -> bool:
    if x < 2:
        return False
    if x % 2 == 0:
        return x == 2
    d = 3
    while d * d <= x:
        if x % d == 0:
            return False
        d += 2
    return True


def next_prime_strictly_greater(x: int) -> int:
    c = x + 1
    while not is_prime(c):
        c += 1
    return c


def solve_part2_from_file(input_path: Path, use_key_mod_n: bool = False, k_mod: int = 1_000_000_007) -> int:
    with input_path.open("rb") as f:
        n, q, k = map(int, f.readline().split())
        s = f.readline().strip().decode("ascii")

        inv_hash_base = pow(HASH_BASE, -1, 1 << 64)
        pw = array("Q", [0]) * (n + 1)
        ipw = array("Q", [0]) * (n + 1)
        pw[0] = 1
        ipw[0] = 1
        for i in range(1, n + 1):
            pw[i] = (pw[i - 1] * HASH_BASE) & MASK64
            ipw[i] = (ipw[i - 1] * inv_hash_base) & MASK64

        # 1..26 values to avoid losing information with leading zeros.
        vals = array("I", [0]) * (n + 1)
        fw = Fenwick64(n)
        rv = Fenwick64(n)

        for i, ch in enumerate(s, 1):
            v = (ord(ch) - 96)
            vals[i] = v
            fw.add(i, v * pw[i])
            j = n - i + 1
            rv.add(j, v * pw[j])

        def is_pal(l: int, r: int) -> int:
            h1 = fw.range_sum(l, r)
            h1 = (h1 * ipw[l]) & MASK64

            rl = n - r + 1
            rr = n - l + 1
            h2 = rv.range_sum(rl, rr)
            h2 = (h2 * ipw[rl]) & MASK64
            return 1 if h1 == h2 else 0

        checksum = 0
        p31 = BASE
        last_ans = 0
        block_pal_count = 0

        for qi in range(1, q + 1):
            line = f.readline()
            while line and not line.strip():
                line = f.readline()
            if not line:
                break

            a, b = map(int, line.split())

            key = last_ans * k
            if use_key_mod_n:
                key %= n
            l = a ^ key
            r = b ^ key

            if l < 1:
                l = 1
            elif l > n:
                l = n
            if r < 1:
                r = 1
            elif r > n:
                r = n
            if l > r:
                l, r = r, l

            if ((l + r) % 3) == 0:
                shrink = (r - l) // 4
                l += shrink
                r -= shrink

            ans = is_pal(l, r)
            last_ans = ans
            block_pal_count += ans

            if ans:
                checksum = (checksum + p31) % MOD

                pos = l
                old = vals[pos]
                new = 1 if old == 26 else old + 1
            else:
                pos = r
                old = vals[pos]
                new = 26 if old == 1 else old - 1

            if new != old:
                vals[pos] = new
                d = (new - old)
                fw.add(pos, d * pw[pos])
                rp = n - pos + 1
                rv.add(rp, d * pw[rp])

            if qi % 1000 == 0:
                prime_next = next_prime_strictly_greater(block_pal_count)
                k = (k * prime_next) % k_mod
                block_pal_count = 0

            p31 = (p31 * BASE) % MOD

    return checksum


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="input.txt")
    parser.add_argument("--part", type=int, default=1)
    parser.add_argument("--key-mod-n", action="store_true")
    parser.add_argument("--k-mod", type=int, default=1_000_000_007)
    args = parser.parse_args()

    if args.part == 1:
        print(solve_part1_from_file(Path(args.input)))
    else:
        print(
            solve_part2_from_file(
                Path(args.input),
                use_key_mod_n=args.key_mod_n,
                k_mod=args.k_mod,
            )
        )


if __name__ == "__main__":
    main()
