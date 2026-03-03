from pathlib import Path

MASK = 0xFFFFFFFF
BINARY_OPS = {"sum", "sub", "xor", "or", "and", "shl", "shr"}


def apply_binary(op: str, left: int, right: int) -> int:
    if op == "sum":
        return (left + right) & MASK
    if op == "sub":
        return (left - right) & MASK
    if op == "xor":
        return (left ^ right) & MASK
    if op == "or":
        return (left | right) & MASK
    if op == "and":
        return (left & right) & MASK
    if op == "shl":
        return (left << (right & 31)) & MASK
    if op == "shr":
        return (left >> (right & 31)) & MASK
    raise ValueError(f"Unknown binary instruction: {op}")


def run_program(lines: list[str]) -> int:
    stack: list[int] = []
    reverse_operands_next = False

    for raw in lines:
        line = raw.strip()
        if not line:
            continue

        parts = line.split()
        op = parts[0]

        if op == "push":
            stack.append(int(parts[1]) & MASK)
            continue

        if op == "dup":
            stack.append(stack[-1])
            continue

        if op == "dup3":
            stack.extend(stack[-3:])
            continue

        if op == "rol":
            n = int(parts[1])
            if n > 1:
                seg = stack[-n:]
                stack[-n:] = [seg[-1]] + seg[:-1]
            continue

        if op == "not":
            a = stack.pop()
            stack.append((~a) & MASK)
            continue

        if op not in BINARY_OPS:
            raise ValueError(f"Unknown instruction: {op}")

        b = stack.pop()
        a = stack.pop()
        if reverse_operands_next:
            left, right = b, a
            reverse_operands_next = False
        else:
            left, right = a, b

        t = apply_binary(op, left, right)
        stack.append(t)

        # Dynamic reaction after each binary operation.
        if ((t >> 31) & 1) == 1:
            stack.reverse()
        elif (t & 1) == 1:
            reverse_operands_next = True

    result = 0
    for v in stack:
        result ^= v
    return result & MASK


def main() -> None:
    input_path = Path(__file__).with_name("input.txt")
    lines = input_path.read_text(encoding="utf-8-sig").splitlines()
    print(run_program(lines))


if __name__ == "__main__":
    main()
