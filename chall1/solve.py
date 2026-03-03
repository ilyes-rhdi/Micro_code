from pathlib import Path
from collections import Counter


MIN_SPREAD = 1000


def find_triplet_product(values: list[int], target: int) -> int:
    counts = Counter(values)
    unique = sorted(counts)
    n = len(unique)

    for i in range(n):
        a = unique[i]
        for j in range(i, n):
            b = unique[j]
            c = target - a - b

            if c < b:
                continue
            if c not in counts:
                continue
            if c - a < MIN_SPREAD:
                continue

            if a == b == c:
                if counts[a] < 3:
                    continue
            elif a == b:
                if counts[a] < 2:
                    continue
            elif b == c:
                if counts[b] < 2:
                    continue

            return a * b * c

    raise RuntimeError("No valid triplet found.")


def main() -> None:
    input_path = Path(__file__).with_name("input.txt")
    lines = input_path.read_text(encoding="utf-8-sig").splitlines()

    target = int(lines[0].strip())
    values = [int(line.strip()) for line in lines[1:] if line.strip()]

    print(find_triplet_product(values, target))


if __name__ == "__main__":
    main()
