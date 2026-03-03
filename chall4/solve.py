from pathlib import Path


def ceil_div(a: int, b: int) -> int:
    return (a + b - 1) // b


def min_rounds_with_cooldown(dishes: list[int], k: int) -> int:
    n = len(dishes)
    if n == 0:
        return 0

    if n == 1:
        adjacency_bound = dishes[0]
    else:
        max_adjacent_pair = max(dishes[i] + dishes[(i + 1) % n] for i in range(n))
        alpha = n // 2
        adjacency_bound = max(max_adjacent_pair, ceil_div(sum(dishes), alpha))

    cooldown_bound = 0
    for d in dishes:
        if d > 0:
            need = (d - 1) * (k + 1) + 1
            if need > cooldown_bound:
                cooldown_bound = need

    return max(adjacency_bound, cooldown_bound)


def main() -> None:
    input_path = Path(__file__).with_name("input.txt")
    lines = [line.strip() for line in input_path.read_text(encoding="utf-8-sig").splitlines() if line.strip()]

    dishes = [int(x) for x in lines[0].split(",")]
    k = int(lines[1])

    print(min_rounds_with_cooldown(dishes, k))


if __name__ == "__main__":
    main()
