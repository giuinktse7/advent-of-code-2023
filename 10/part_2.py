from enum import Enum
from queue import Empty, Queue
from typing import Generator
import numpy as np


def print_enclosing(data: np.array, distances: np.array):
    result = ""
    for y, x in np.ndindex(distances.shape):
        if x == 0 and y > 0:
            result += "\n"

        if distances[y, x] == 0 and data[y, x] != "S":
            result += "."
        else:
            result += data[y, x]

    print(result)


def print_map(data: np.array):
    result = ""
    for y, x in np.ndindex(data.shape):
        if x == 0 and y > 0:
            result += "\n"

        result += str(data[y, x]) or "."

    print(result)


def read_file(path: str) -> list[str]:
    with open(path, "r") as f:
        return f.readlines()


lines = read_file("data/input")


class Dir(Enum):
    North = (0, -1)
    East = (1, 0)
    South = (0, 1)
    West = (-1, 0)


SYMBOL_TO_POSSIBLE_DIRS = {
    "S": [Dir.North, Dir.East, Dir.South, Dir.West],
    "|": [Dir.North, Dir.South],
    "-": [Dir.East, Dir.West],
    "L": [Dir.North, Dir.East],
    "J": [Dir.North, Dir.West],
    "7": [Dir.South, Dir.West],
    "F": [Dir.South, Dir.East],
}


class PipeMap:
    data: np.array

    @property
    def width(self):
        return self.data.shape[1]

    @property
    def height(self):
        return self.data.shape[0]

    def __init__(self, data: list[str]):
        self.data = np.array([list(line.strip()) for line in data])

    def start_pos(self):
        for y, x in np.ndindex(self.data.shape):
            if self.data[y, x] == "S":
                return (x, y)

    def expand(self):
        d = np.insert(self.data, np.arange(2, self.width - 1), ".", axis=1)
        d = np.insert(d, np.arange(2, self.height - 1), ".", axis=0)

        x_end = d.shape[1]
        y_end = d.shape[0]

        for y in range(2, y_end, 2):
            for x in range(0, x_end):
                stitch_horizontal(d, x, y)

        for x in range(2, x_end, 2):
            for y in range(0, y_end):
                stitch_vertical(d, x, y)

        self.data = d

    def contract(self):
        d = np.delete(self.data, np.arange(2, self.width - 1, 2), axis=1)
        d = np.delete(d, np.arange(2, self.height - 1, 2), axis=0)

        self.data = d

    def get(self, x: int, y: int) -> str:
        return self.data[y, x]

    def connects(self, direction: Dir, c: str) -> bool:
        match direction:
            case Dir.North if c in ["|", "F", "7"]:
                return True
            case Dir.East if c in ["-", "J", "7"]:
                return True
            case Dir.South if c in ["|", "L", "J"]:
                return True
            case Dir.West if c in ["-", "L", "F"]:
                return True
            case _:
                return False

    def compute_loop_distances(self, x0: int, y0: int):
        distances = np.zeros(self.data.shape, dtype=int)

        q = Queue()
        q.put((x0, y0, 0))
        try:
            while p := q.get(block=False):
                px, py, distance = p
                c = self.get(px, py)
                if not (potential_connectors := SYMBOL_TO_POSSIBLE_DIRS.get(c, None)):
                    continue

                for direction in potential_connectors:
                    x, y = direction.value
                    x += px
                    y += py

                    if distances[y, x] > 0 and distances[y, x] <= distance + 1:
                        continue

                    c = self.get(x, y)
                    if self.connects(direction, c):
                        q.put((x, y, distance + 1))
                        distances[y, x] = distance + 1

        except Empty:
            return distances


def stitch_horizontal(data: np.array, x: int, y: int):
    match data[y - 1, x]:
        case "|" | "F" | "7" | "S":
            data[y, x] = "|"


def stitch_vertical(data: np.array, x: int, y: int):
    match data[y, x - 1]:
        case "-" | "L" | "F" | "S":
            data[y, x] = "-"


def flood_fill(data: np.array, loop_distances: np.array, x: int, y: int):
    width = data.shape[1]
    height = data.shape[0]

    def in_loop(x: int, y: int) -> bool:
        return loop_distances[y, x] > 0 or data[y, x] == "S"

    def inside_bounds(x: int, y: int) -> bool:
        return x >= 0 and x < width and y >= 0 and y < height

    reached_edge = False
    visited: set[tuple[int, int]] = set()
    q = Queue()
    q.put((x, y))
    try:
        while p := q.get(block=False):
            if p in visited:
                continue

            px, py = p
            visited.add((px, py))

            if px == 0 or py == 0 or px == width - 1 or py == height - 1:
                reached_edge = True

            for direction in Dir:
                dx, dy = direction.value
                dx += px
                dy += py
                if (dx, dy) in visited or not inside_bounds(dx, dy) or in_loop(dx, dy):
                    continue

                q.put((dx, dy))
    except Empty:
        return visited, reached_edge


def flood_fill_pos_generator(m: PipeMap, distances: np.array) -> Generator[tuple[int, int], None, None]:
    for y, x in np.ndindex(distances.shape):
        if distances[y, x] == 0 and m.get(x, y) not in ["0", "I", "S"]:
            yield (x, y)


def solve():
    pipe_map = PipeMap(lines)

    # Add extra positions between all tiles to handle the "travel-between-tiles" rule.
    pipe_map.expand()

    x, y = pipe_map.start_pos()
    ds = pipe_map.compute_loop_distances(x, y)

    flood_start_pos = flood_fill_pos_generator(pipe_map, ds)

    while start_pos := next(flood_start_pos, None):
        x, y = start_pos
        positions, reached_edge = flood_fill(pipe_map.data, ds, x, y)

        if len(positions) == 0:
            break

        c = "0" if reached_edge else "I"
        for x, y in positions:
            pipe_map.data[y, x] = c

    # Remove the extra positions between tiles added earlier by expand.
    pipe_map.contract()
    result = (pipe_map.data.flatten() == "I").sum()
    print(result)


solve()
