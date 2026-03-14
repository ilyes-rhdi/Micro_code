from __future__ import annotations

from pathlib import Path

MASK64 = (1 << 64) - 1
MASK32 = (1 << 32) - 1


def pcg_output(state: int) -> int:
    xorshifted = ((state >> 18) ^ state) >> 27
    rot = state >> 59
    return ((xorshifted >> rot) | (xorshifted << ((-rot) & 31))) & MASK32


def checksum_first_n(s0: int, mult: int, inc: int, n: int, mod_p: int) -> int:
    state = s0 & MASK64
    checksum = 0
    for _ in range(n):
        checksum = (checksum + pcg_output(state)) % mod_p
        state = (state * mult + inc) & MASK64
    return checksum


def leap_state_mod_p(s0: int, mult: int, inc: int, t: int, mod_p: int) -> int:
    acc_mult = 1 % mod_p
    acc_inc = 0
    cur_mult = mult % mod_p
    cur_inc = inc % mod_p

    while t > 0:
        if t & 1:
            acc_inc = (acc_inc * cur_mult + cur_inc) % mod_p
            acc_mult = (acc_mult * cur_mult) % mod_p
        cur_inc = (cur_inc * (cur_mult + 1)) % mod_p
        cur_mult = (cur_mult * cur_mult) % mod_p
        t >>= 1

    return (acc_mult * (s0 % mod_p) + acc_inc) % mod_p


def main() -> None:
    input_path = Path(__file__).with_name("input.txt")
    raw = input_path.read_text(encoding="utf-8-sig").strip().split()
    if not raw:
        return

    s0, mult, inc, n, t, mod_p = map(int, raw)
    part1 = checksum_first_n(s0, mult, inc, n, mod_p)
    part2 = leap_state_mod_p(s0, mult, inc, t, mod_p)

    print(part1)
    print(part2)


if __name__ == "__main__":
    main()
