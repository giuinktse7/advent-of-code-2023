import re
from typing import Generator
from math import gcd
from functools import reduce


def read_file(path: str) -> list[str]:
    with open(path, "r") as f:
        return [line.strip() for line in f.readlines()]


node_lines = read_file("data/input")
directions, _, *node_lines = node_lines

node_map: dict[str, tuple[str, str]] = {}
for line in node_lines:
    node, l, r = re.match(r"([[A-Z\d]{3}) = \(([A-Z\d]{3}), ([A-Z\d]{3})\)", line).groups()

    node_map[node] = (l, r)


def repeat(xs: list[str]) -> Generator[str, None, None]:
    while True:
        for x in xs:
            yield x


step = 1
direction_generator = repeat(directions)
nodes = [x for x in node_map.keys() if x.endswith("A")]


factors = []
z_hits: dict[str, int] = {}
while len(nodes) > 0:
    direction = next(direction_generator)
    dir_index = 0 if direction == "L" else 1

    # Reversed to be able to delete nodes while iterating
    for i in reversed(range(len(nodes))):
        node = nodes[i]
        next_node = node_map[node][dir_index]
        nodes[i] = next_node

        if next_node.endswith("Z"):
            if next_node in z_hits:
                factors.append(step - z_hits[next_node])
                del nodes[i]
            else:
                z_hits[next_node] = step
    step += 1


def lcd(xs: list[int]) -> int:
    return reduce(lambda a, b: a * b // gcd(a, b), xs)


print(lcd(factors))
