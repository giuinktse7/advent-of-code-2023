from functools import reduce


def read_file(path: str) -> list[str]:
    with open(path, "r") as f:
        return [x.strip() for x in f.readlines()]


lines = read_file("data/input")
histories = [list(map(int, x.split())) for x in lines]


def find_next(history: list[int]):
    xs = []

    seq = history
    while any(x for x in seq if x != 0):
        xs.append(seq[-1])
        seq = [b - a for a, b in zip(seq, seq[1:])]

    return reduce(lambda x, y: y + x, reversed(xs), 0)


result = sum([find_next(x) for x in histories])
print(result)
