import numpy as np
from itertools import combinations


def read_file(path: str) -> list[str]:
    with open(path, "r") as f:
        return f.readlines()


def parse_line(line: str) -> list[int]:
    return [0 if x == "." else 1 for x in line.strip()]


def expand_universe(u: np.ndarray) -> np.ndarray:
    empty_cols = np.where(~u.any(axis=0))[0]
    empty_rows = np.where(~u.any(axis=1))[0]

    u = np.insert(u, empty_cols, 0, axis=1)
    u = np.insert(u, empty_rows, 0, axis=0)

    return u


def tile_distance(g1: tuple[int, int], g2: tuple[int, int]) -> int:
    return abs(g1[0] - g2[0]) + abs(g1[1] - g2[1])


lines = read_file("data/input")

universe = np.array(list(map(parse_line, lines)))
universe = expand_universe(universe)
rows, cols = np.where(universe == 1)

galaxies = np.column_stack((rows, cols)).tolist()
pairs = combinations(galaxies, 2)
distances = [tile_distance(g1, g2) for g1, g2 in pairs]
print(sum(distances))
