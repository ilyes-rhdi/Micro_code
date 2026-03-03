from pathlib import Path

VALUES = {
    "A": 247,
    "B": 383,
    "C": 156,
    "D": 512,
}
COLLAPSE_LIMIT = 1000


def evaluate_formula(formula: str) -> int:
    stack = [0]
    i = 0
    n = len(formula)

    while i < n:
        ch = formula[i]

        if ch in VALUES:
            stack[-1] += VALUES[ch]
            i += 1
            continue

        if ch == "(":
            stack.append(0)
            i += 1
            continue

        if ch == ")":
            if len(stack) < 2:
                raise ValueError("Unmatched ')'")
            if i + 1 >= n or formula[i + 1] != "{":
                raise ValueError("Missing multiplier after ')'")

            j = i + 2
            while j < n and formula[j].isdigit():
                j += 1
            if j == i + 2 or j >= n or formula[j] != "}":
                raise ValueError("Invalid multiplier format")

            mult = int(formula[i + 2 : j])
            group_sum = stack.pop()
            if group_sum > COLLAPSE_LIMIT:
                group_sum %= COLLAPSE_LIMIT
            stack[-1] += group_sum * mult
            i = j + 1
            continue

        if ch.isspace():
            i += 1
            continue

        raise ValueError(f"Unexpected character: {ch!r}")

    if len(stack) != 1:
        raise ValueError("Unmatched '('")

    return stack[0]


def main() -> None:
    input_path = Path(__file__).with_name("input.txt")
    formula = input_path.read_text(encoding="utf-8-sig").strip()
    print(evaluate_formula(formula))


if __name__ == "__main__":
    main()
