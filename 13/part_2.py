from util import chunk_by_value


def read_file(path: str) -> list[str]:
    with open(path, "r") as f:
        return [line.strip() for line in f.readlines()]


def transpose(xs: list[str]) -> list[str]:
    return list(map("".join, zip(*xs)))


lines = read_file("data/input")


def count_different(a: str, b: str) -> int:
    return sum(1 for x, y in zip(a, b) if x != y)


def equal_with_smudge(a: str, b: str, has_smudge: bool) -> tuple[bool, bool]:
    if a == b:
        return True, has_smudge

    if has_smudge and count_different(a, b) == 1:
        return True, False

    return False, has_smudge


def is_reflection(xs: list[str], left: int, right: int, has_smudge: bool) -> tuple[bool, bool]:
    while left >= 0 and right < len(xs):
        equal, has_smudge = equal_with_smudge(xs[left], xs[right], has_smudge)
        if not equal:
            return False, has_smudge
        left -= 1
        right += 1

    return True, has_smudge


def find_reflection_place(xs: list[str]):
    for i in range(len(xs) - 1):
        equal, has_smudge = equal_with_smudge(xs[i], xs[i + 1], True)
        if equal:
            reflection, has_smudge = is_reflection(xs, i - 1, i + 2, has_smudge)
            if reflection and not has_smudge:
                # + 1 because we count all above the middle line
                return i + 1


def run():
    lines_above = 0
    lines_to_the_left = 0
    for rows in chunk_by_value(lines, ""):
        found_row = find_reflection_place(rows)
        if found_row is not None:
            lines_above += found_row
            continue

        columns = transpose(rows)
        found_col = find_reflection_place(columns)
        if found_col is not None:
            lines_to_the_left += found_col

    print(lines_to_the_left + 100 * lines_above)


run()
