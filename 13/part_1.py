from util import chunk_by_value


def read_file(path: str) -> list[str]:
    with open(path, "r") as f:
        return [line.strip() for line in f.readlines()]


def transpose(xs: list[str]) -> list[str]:
    return list(map("".join, zip(*xs)))


lines = read_file("data/input")


def is_reflection(xs: list[str], left: int, right: int):
    while left >= 0 and right < len(xs):
        if xs[left] != xs[right]:
            return False
        left -= 1
        right += 1

    return True


def find_reflection(xs: list[str]):
    for i in range(len(xs) - 1):
        if xs[i] == xs[i + 1] and is_reflection(xs, i, i + 1):
            return i


def run():
    lines_above = 0
    lines_to_the_left = 0
    for rows in chunk_by_value(lines, ""):
        found_row = find_reflection(rows)
        if found_row is not None:
            lines_above += found_row + 1

        found_col = find_reflection(transpose(rows))
        if found_col is not None:
            lines_to_the_left += found_col + 1

    print(lines_to_the_left + 100 * lines_above)


run()
