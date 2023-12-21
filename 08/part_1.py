import re
from typing import Generator


def read_file(path: str) -> list[str]:
    with open(path, "r") as f:
        return [line.strip() for line in f.readlines()]


node_lines = read_file("data/input")
directions, _, *node_lines = node_lines

node_map: dict[str, tuple[str, str]] = {}
for line in node_lines:
    node, l, r = re.match(r"([A-Z]{3}) = \(([A-Z]{3}), ([A-Z]{3})\)", line).groups()

    node_map[node] = (l, r)


def repeat(xs: list[str]) -> Generator[str, None, None]:
    while True:
        for x in xs:
            yield x


direction_generator = repeat(directions)

steps = 0
node = "AAA"
while node != "ZZZ":
    steps += 1
    l, r = node_map[node]
    node = l if next(direction_generator) == "L" else r

print(steps)
