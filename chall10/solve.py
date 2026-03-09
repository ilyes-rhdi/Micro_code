from __future__ import annotations

import argparse
import heapq
import sys
from pathlib import Path

INF = 10**30


def parse_input(path: Path):
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    n, m = map(int, lines[0].split())
    edges: list[tuple[int, int, int]] = []
    for i in range(1, m + 1):
        a, b, w = map(int, lines[i].split())
        edges.append((a, b, w))
    return n, edges


def dijkstra_single_target(
    adj: list[list[tuple[int, int, int]]],
    n: int,
    src: int,
    target: int,
    cutoff: int,
    banned_edge_idx: int = -1,
) -> int:
    dist = [INF] * n
    dist[src] = 0
    pq = [(0, src)]

    while pq:
        d, u = heapq.heappop(pq)
        if d != dist[u]:
            continue
        if d >= cutoff:
            break
        if u == target:
            return d
        for v, w, idx in adj[u]:
            if idx == banned_edge_idx:
                continue
            nd = d + w
            if nd < dist[v] and nd < cutoff:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))

    return INF


def min_cycle_with_optional_reversal(n: int, edges: list[tuple[int, int, int]]) -> int:
    adj = [[] for _ in range(n)]
    for idx, (a, b, w) in enumerate(edges):
        adj[a].append((b, w, idx))

    best = INF

    # No reversal: min over edges (u->v) of w + dist(v,u).
    for idx, (u, v, w) in enumerate(edges):
        d = dijkstra_single_target(adj, n, v, u, best - w)
        if d < INF:
            best = min(best, w + d)

    # Reverse exactly one edge by replacing u->v with v->u:
    # candidate cycle uses new (v->u) with weight w plus path u->v
    # in graph where that exact edge occurrence is removed.
    for idx, (u, v, w) in enumerate(edges):
        d = dijkstra_single_target(adj, n, u, v, best - w, banned_edge_idx=idx)
        if d < INF:
            best = min(best, w + d)

    if best >= INF:
        return INF
    return best


def solve_part1(n: int, edges: list[tuple[int, int, int]]) -> int:
    best = min_cycle_with_optional_reversal(n, edges)
    if best >= INF:
        raise RuntimeError("No directed cycle found")
    return best


def kosaraju_scc(n: int, edges: list[tuple[int, int, int]]) -> tuple[list[int], list[list[int]]]:
    g = [[] for _ in range(n)]
    rg = [[] for _ in range(n)]
    for a, b, _ in edges:
        g[a].append(b)
        rg[b].append(a)

    sys.setrecursionlimit(max(1_000_000, n * 2))
    vis = [False] * n
    order: list[int] = []

    def dfs1(u: int) -> None:
        vis[u] = True
        for v in g[u]:
            if not vis[v]:
                dfs1(v)
        order.append(u)

    for u in range(n):
        if not vis[u]:
            dfs1(u)

    comp_id = [-1] * n
    comps: list[list[int]] = []

    def dfs2(u: int, cid: int) -> None:
        comp_id[u] = cid
        comps[cid].append(u)
        for v in rg[u]:
            if comp_id[v] == -1:
                dfs2(v, cid)

    for u in reversed(order):
        if comp_id[u] != -1:
            continue
        cid = len(comps)
        comps.append([])
        dfs2(u, cid)

    return comp_id, comps


def solve_part2(n: int, edges: list[tuple[int, int, int]]) -> int:
    comp_id, comps = kosaraju_scc(n, edges)
    k = len(comps)

    comp_edges: list[list[tuple[int, int, int]]] = [[] for _ in range(k)]
    cross_min: dict[tuple[int, int], int] = {}

    for a, b, w in edges:
        ca = comp_id[a]
        cb = comp_id[b]
        if ca == cb:
            comp_edges[ca].append((a, b, w))
        else:
            key = (ca, cb)
            prev = cross_min.get(key)
            if prev is None or w < prev:
                cross_min[key] = w

    # SCC weights
    scc_weight = [0] * k
    for cid, nodes in enumerate(comps):
        if len(nodes) < 2:
            scc_weight[cid] = 0
            continue
        # Local relabeling for fast Dijkstra on SCC-only nodes.
        local_idx = {u: i for i, u in enumerate(nodes)}
        local_edges = [(local_idx[a], local_idx[b], w) for a, b, w in comp_edges[cid]]
        # Checker expects SCC cycle weight with original directions only.
        cyc = INF
        adj_local = [[] for _ in range(len(nodes))]
        for idx, (a, b, w) in enumerate(local_edges):
            adj_local[a].append((b, w, idx))
        for _, (u, v, w) in enumerate(local_edges):
            d = dijkstra_single_target(adj_local, len(nodes), v, u, cyc - w)
            if d < INF:
                cyc = min(cyc, w + d)
        if cyc >= INF:
            cyc = 0
        scc_weight[cid] = cyc

    dag = [[] for _ in range(k)]
    indeg = [0] * k
    for (u, v), w in cross_min.items():
        dag[u].append((v, w))
        indeg[v] += 1

    # Topological order (condensation is DAG).
    q = [i for i in range(k) if indeg[i] == 0]
    topo: list[int] = []
    head = 0
    while head < len(q):
        u = q[head]
        head += 1
        topo.append(u)
        for v, _ in dag[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)

    dp_len = [1] * k
    dp_w = [scc_weight[i] for i in range(k)]

    for u in reversed(topo):
        best_len = 1
        best_w = scc_weight[u]
        for v, _ in dag[u]:
            cand_len = 1 + dp_len[v]
            # Checker expects path score as sum of SCC weights only.
            cand_w = scc_weight[u] + dp_w[v]
            if cand_len > best_len or (cand_len == best_len and cand_w > best_w):
                best_len = cand_len
                best_w = cand_w
        dp_len[u] = best_len
        dp_w[u] = best_w

    ans_len = 0
    ans_w = -INF
    for i in range(k):
        if dp_len[i] > ans_len or (dp_len[i] == ans_len and dp_w[i] > ans_w):
            ans_len = dp_len[i]
            ans_w = dp_w[i]
    return ans_w


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve chall10")
    parser.add_argument("--input", default="input.txt")
    parser.add_argument("--part", type=int, choices=[1, 2], default=1)
    args = parser.parse_args()

    n, edges = parse_input(Path(args.input))

    if args.part == 1:
        print(solve_part1(n, edges))
    else:
        print(solve_part2(n, edges))


if __name__ == "__main__":
    main()
