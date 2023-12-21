import numpy as np
from itertools import combinations


def read_file(path: str) -> list[str]:
    with open(path, "r") as f:
        return f.readlines()


def parse_line(line: str) -> list[int]:
    return [0 if x == "." else 1 for x in line.strip()]


def expand_empty_space(empty_indices: list[int], galaxies: list[list[int]], axis: int):
    c = 0
    for i in range(len(galaxies)):
        row = galaxies[i][axis]
        while c < len(empty_indices) and empty_indices[c] < row:
            c += 1

        galaxies[i][axis] += (1000000 - 1) * c


def get_expanded_galaxies(u: np.ndarray) -> list[list[int]]:
    empty_cols = np.where(~u.any(axis=0))[0]
    empty_rows = np.where(~u.any(axis=1))[0]

    rows, cols = np.where(universe == 1)
    galaxies = np.column_stack((rows, cols)).tolist()

    expand_empty_space(empty_rows, galaxies, 0)

    galaxies.sort(key=lambda x: x[1])
    expand_empty_space(empty_cols, galaxies, 1)

    return galaxies


def tile_distance(g1: tuple[int, int], g2: tuple[int, int]) -> int:
    return abs(g1[0] - g2[0]) + abs(g1[1] - g2[1])


lines = read_file("data/input")
universe = np.array(list(map(parse_line, lines)))
galaxies = get_expanded_galaxies(universe)

pairs = combinations(galaxies, 2)
distances = [tile_distance(g1, g2) for g1, g2 in pairs]

print(sum(distances))
