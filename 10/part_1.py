from enum import Enum
from queue import Empty, Queue
import numpy as np


def read_file(path: str) -> list[str]:
    with open(path, "r") as f:
        return f.readlines()


# lines = read_file("data/example")
# lines = read_file("data/example2")
lines = read_file("data/input")


class Dir(Enum):
    North = (0, -1)
    East = (1, 0)
    South = (0, 1)
    West = (-1, 0)


class PipeMap:
    data: np.array

    def __init__(self, data: list[str]):
        self.data = np.array([list(line.strip()) for line in data])

    def get_start_pos(self):
        for y, x in np.ndindex(self.data.shape):
            if self.data[y, x] == "S":
                return (x, y)

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

    def count_distances(self, x0: int, y0: int):
        distances = np.zeros(self.data.shape, dtype=int)

        potential_connectors = []

        q = Queue()
        q.put((x0, y0, 0))
        try:
            while p := q.get(block=False):
                px, py, distance = p
                match self.get(px, py):
                    case "S":
                        potential_connectors = [Dir.North, Dir.East, Dir.South, Dir.West]
                    case "|":
                        potential_connectors = [Dir.North, Dir.South]
                    case "-":
                        potential_connectors = [Dir.East, Dir.West]
                    case "L":
                        potential_connectors = [Dir.North, Dir.East]
                    case "J":
                        potential_connectors = [Dir.North, Dir.West]
                    case "7":
                        potential_connectors = [Dir.South, Dir.West]
                    case "F":
                        potential_connectors = [Dir.South, Dir.East]
                    case _:
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


# | is a vertical pipe connecting north and south.
# - is a horizontal pipe connecting east and west.
# L is a 90-degree bend connecting north and east.
# J is a 90-degree bend connecting north and west.
# 7 is a 90-degree bend connecting south and west.
# F is a 90-degree bend connecting south and east.
# . is ground; there is no pipe in this tile.
# S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.

# The pipe that contains the animal is one large, continuous loop.
m = PipeMap(lines)
x, y = m.get_start_pos()
ds = m.count_distances(x, y)
result = np.max(ds)
print(ds)
print(result)
