import argparse
from array import array
from pathlib import Path


INF = 10**18
MOD_PART2 = 1_000_000_009


def build_next(grid, r, c, wrap: bool):
    n = r * c
    nxt = array("i", [-1]) * n
    for i in range(r):
        row = grid[i]
        base = i * c
        for j in range(c):
            ch = row[j]
            ni, nj = i, j
            if ch == ">":
                nj += 1
            elif ch == "<":
                nj -= 1
            elif ch == "v":
                ni += 1
            else:  # '^'
                ni -= 1
            idx = base + j
            if wrap:
                ni %= r
                nj %= c
                nxt[idx] = ni * c + nj
            else:
                if 0 <= ni < r and 0 <= nj < c:
                    nxt[idx] = ni * c + nj
                else:
                    nxt[idx] = -1
    return nxt


def compute_meta(nxt):
    n = len(nxt)
    state = array("b", [0]) * n  # 0 unvisited, 1 visiting, 2 done
    dist_exit = array("q", [INF]) * n
    dist_cycle = array("q", [INF]) * n
    cycle_len = array("q", [0]) * n

    for start in range(n):
        if state[start] != 0:
            continue
        path = []
        index = {}
        cur = start
        while True:
            if cur == -1:
                # off-grid reached
                for node in reversed(path):
                    nxt_node = nxt[node]
                    if nxt_node == -1:
                        dist_exit[node] = 1
                        dist_cycle[node] = INF
                        cycle_len[node] = 0
                    else:
                        if dist_exit[nxt_node] < INF:
                            dist_exit[node] = dist_exit[nxt_node] + 1
                        else:
                            dist_exit[node] = INF
                        if cycle_len[nxt_node] > 0:
                            cycle_len[node] = cycle_len[nxt_node]
                            dist_cycle[node] = dist_cycle[nxt_node] + 1
                        else:
                            cycle_len[node] = 0
                            dist_cycle[node] = INF
                    state[node] = 2
                break

            st = state[cur]
            if st == 0:
                state[cur] = 1
                index[cur] = len(path)
                path.append(cur)
                cur = nxt[cur]
                continue
            if st == 1:
                # cycle found
                cycle_start = index[cur]
                cycle_nodes = path[cycle_start:]
                clen = len(cycle_nodes)
                for node in cycle_nodes:
                    cycle_len[node] = clen
                    dist_cycle[node] = 0
                    dist_exit[node] = INF
                    state[node] = 2
                for idx in range(cycle_start - 1, -1, -1):
                    node = path[idx]
                    nxt_node = nxt[node]
                    cycle_len[node] = cycle_len[nxt_node]
                    dist_cycle[node] = dist_cycle[nxt_node] + 1
                    dist_exit[node] = INF
                    state[node] = 2
                break
            # st == 2
            for node in reversed(path):
                nxt_node = nxt[node]
                if nxt_node == -1:
                    dist_exit[node] = 1
                    dist_cycle[node] = INF
                    cycle_len[node] = 0
                else:
                    if dist_exit[nxt_node] < INF:
                        dist_exit[node] = dist_exit[nxt_node] + 1
                    else:
                        dist_exit[node] = INF
                    if cycle_len[nxt_node] > 0:
                        cycle_len[node] = cycle_len[nxt_node]
                        dist_cycle[node] = dist_cycle[nxt_node] + 1
                    else:
                        cycle_len[node] = 0
                        dist_cycle[node] = INF
                state[node] = 2
            break

    return dist_exit, dist_cycle, cycle_len


def build_jump(nxt, max_pow):
    n = len(nxt)
    jumps = [array("i", nxt)]
    for _ in range(1, max_pow + 1):
        prev = jumps[-1]
        cur = array("i", [-1]) * n
        for i in range(n):
            mid = prev[i]
            cur[i] = prev[mid] if mid != -1 else -1
        jumps.append(cur)
    return jumps


def jump(jumps, node, steps):
    bit = 0
    while steps and node != -1:
        if steps & 1:
            node = jumps[bit][node]
        steps >>= 1
        bit += 1
    return node


def solve_part1(data: str) -> int:
    it = iter(data.splitlines())
    r, c, t, items = map(int, next(it).split())
    grid = [next(it).strip() for _ in range(r)]

    nxt = build_next(grid, r, c, wrap=False)
    dist_exit, dist_cycle, cycle_len = compute_meta(nxt)

    max_pow = 0
    temp = t
    while temp:
        max_pow += 1
        temp >>= 1
    jumps = build_jump(nxt, max_pow)

    checksum = 0
    for _ in range(items):
        line = next(it)
        if not line:
            line = next(it)
        rr, cc = map(int, line.split())
        start = rr * c + cc
        d_exit = dist_exit[start]
        if d_exit <= t:
            continue
        if t == 0:
            end = start
        else:
            end = jump(jumps, start, t)
            if end == -1:
                continue
        checksum += (end // c) * c + (end % c)
    return checksum


def solve_part2(data: str) -> int:
    it = iter(data.splitlines())
    r, c, t, items = map(int, next(it).split())
    grid = [next(it).strip() for _ in range(r)]

    nxt = build_next(grid, r, c, wrap=True)
    n = r * c

    # doubling tables for sum of positions over steps
    max_pow = 0
    temp = t
    while temp:
        max_pow += 1
        temp >>= 1

    jumps = [array("i", nxt)]
    sums = []
    # sum over 1 step = value of next position
    base_sum = array("I", [0]) * n
    for i in range(n):
        base_sum[i] = jumps[0][i]
    sums.append(base_sum)

    for _ in range(1, max_pow + 1):
        prev_jump = jumps[-1]
        prev_sum = sums[-1]
        cur_jump = array("i", [-1]) * n
        cur_sum = array("I", [0]) * n
        for i in range(n):
            mid = prev_jump[i]
            cur_jump[i] = prev_jump[mid]
            cur_sum[i] = (prev_sum[i] + prev_sum[mid]) % MOD_PART2
        jumps.append(cur_jump)
        sums.append(cur_sum)

    def sum_steps(start, steps):
        node = start
        total = 0
        bit = 0
        while steps:
            if steps & 1:
                total = (total + sums[bit][node]) % MOD_PART2
                node = jumps[bit][node]
            steps >>= 1
            bit += 1
        return total

    total = 0
    for _ in range(items):
        line = next(it)
        while line == "":
            line = next(it)
        rr, cc = map(int, line.split())
        start = rr * c + cc
        total = (total + sum_steps(start, t)) % MOD_PART2
    return total


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="input.txt")
    parser.add_argument("--part", type=int, default=1)
    args = parser.parse_args()
    data = Path(args.input).read_text(encoding="utf-8")
    if args.part == 1:
        print(solve_part1(data))
    else:
        print(solve_part2(data))


if __name__ == "__main__":
    main()
