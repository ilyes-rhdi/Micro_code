from __future__ import annotations

from pathlib import Path

MOD = 1_000_000_007


def parse_tree(lines: list[str]) -> tuple[int, list[list[int]], list[int]]:
    data = [line.strip() for line in lines if line.strip()]
    n = int(data[0])

    children = [[] for _ in range(n)]
    parent = [-1] * n
    parent[0] = 0
    for row in data[1:]:
        p, c = map(int, row.split())
        children[p].append(c)
        parent[c] = p
    return n, children, parent


def solve_part1(lines: list[str]) -> int:
    n, children, _ = parse_tree(lines)

    size = [0] * n
    label_sum = [0] * n
    label_sq_sum = [0] * n
    answer = 0

    def dfs(u: int) -> None:
        nonlocal answer
        s = 1
        sm = u
        sq = u * u
        for v in children[u]:
            dfs(v)
            s += size[v]
            sm += label_sum[v]
            sq += label_sq_sum[v]

        size[u] = s
        label_sum[u] = sm
        label_sq_sum[u] = sq

        # Descendants are all nodes in subtree except u itself.
        cnt = s - 1
        if cnt == 0:
            return
        desc_sum = sm - u
        desc_sq_sum = sq - u * u

        contrib = desc_sq_sum - 2 * u * desc_sum + cnt * u * u
        answer = (answer + contrib) % MOD

    dfs(0)
    return answer


def solve_part2(lines: list[str]) -> int:
    n, children, parent = parse_tree(lines)
    if n <= 1:
        return 0

    log = n.bit_length()
    up = [[0] * n for _ in range(log)]
    depth = [0] * n

    stack = [0]
    while stack:
        u = stack.pop()
        for v in children[u]:
            depth[v] = depth[u] + 1
            up[0][v] = u
            stack.append(v)
    up[0][0] = 0

    for k in range(1, log):
        prev = up[k - 1]
        cur = up[k]
        for v in range(n):
            cur[v] = prev[prev[v]]

    def lca(a: int, b: int) -> int:
        if depth[a] < depth[b]:
            a, b = b, a

        diff = depth[a] - depth[b]
        bit = 0
        while diff:
            if diff & 1:
                a = up[bit][a]
            diff >>= 1
            bit += 1

        if a == b:
            return a

        for k in range(log - 1, -1, -1):
            if up[k][a] != up[k][b]:
                a = up[k][a]
                b = up[k][b]
        return parent[a]

    total = 0
    for i in range(n):
        for j in range(i + 1, n):
            total += depth[lca(i, j)]
    return total % MOD


def main() -> None:
    input_path = Path(__file__).with_name("input.txt")
    lines = input_path.read_text(encoding="utf-8-sig").splitlines()
    print(solve_part2(lines))


if __name__ == "__main__":
    main()
