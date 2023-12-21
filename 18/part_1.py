from dataclasses import dataclass
from enum import Enum
from queue import Empty, Queue

import numpy as np


def read_file(path: str) -> list[str]:
    with open(path, "r") as f:
        return [line.strip() for line in f.readlines()]


class Direction(Enum):
    NORTH = (0, -1)
    EAST = (1, 0)
    SOUTH = (0, 1)
    WEST = (-1, 0)


@dataclass
class Instruction:
    direction: Direction
    meters: int


lines = read_file("data/input")
# lines = read_file("data/example")


def parse_direction(x: str) -> Direction:
    match x:
        case "U":
            return Direction.NORTH
        case "R":
            return Direction.EAST
        case "D":
            return Direction.SOUTH
        case "L":
            return Direction.WEST


instructions = []
for line in lines:
    d, m, c = line.split(" ")

    meters = int(m)
    instructions.append(Instruction(parse_direction(d), meters))

side_length = 1000


def flood_fill(data: np.array, x: int, y: int):
    height, width = data.shape

    def in_loop(x: int, y: int) -> bool:
        return data[y, x] == 1

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

            for direction in Direction:
                dx, dy = direction.value
                dx += px
                dy += py
                if (dx, dy) in visited or not inside_bounds(dx, dy) or in_loop(dx, dy):
                    continue

                q.put((dx, dy))
    except Empty:
        return visited, reached_edge


class State:
    grid: np.ndarray

    @property
    def contracted_grid(self) -> np.ndarray:
        x0, y0 = self.top_left
        x1, y1 = self.bottom_right
        return self.grid[y0 : y1 + 1, x0 : x1 + 1]

    @property
    def contracted_zero(self) -> tuple[int, int]:
        x0, y0 = self.top_left
        x, y = (side_length // 2, side_length // 2)
        return (x - x0, y - y0)

    def __init__(self, side_length: int):
        self.side_length = side_length
        self.grid = np.zeros((side_length, side_length), dtype=int)
        self.pos = (side_length // 2, side_length // 2)
        self.top_left = self.pos
        self.bottom_right = self.pos

    def apply_instruction(self, instruction: Instruction):
        x, y = self.pos
        m = instruction.meters
        match instruction.direction:
            case Direction.NORTH:
                self.grid[y - m : y, x] = 1
                self.pos = (x, y - m)
            case Direction.EAST:
                self.grid[y, x : x + m + 1] = 1
                self.pos = (x + m, y)
            case Direction.SOUTH:
                self.grid[y : y + m + 1, x] = 1
                self.pos = (x, y + m)
            case Direction.WEST:
                self.grid[y, x - m : x] = 1
                self.pos = (x - m, y)

        x, y = self.pos
        x0, y0 = self.top_left
        x1, y1 = self.bottom_right
        self.top_left = (min(x0, x), min(y0, y))
        self.bottom_right = (max(x1, x), max(y1, y))


s = State(side_length)

for instruction in instructions:
    s.apply_instruction(instruction)


print(s.contracted_grid)

x0, y0 = s.contracted_zero
flood_fill_candidates = [
    (x0 + 1, y0 + 1),
    (x0 - 1, y0 - 1),
    (x0 + 1, y0 - 1),
    (x0 - 1, y0 + 1),
]

contracted_grid = s.contracted_grid
edges = contracted_grid.sum()

for candidate in flood_fill_candidates:
    visited, reached_edge = flood_fill(s.contracted_grid, *candidate)
    if not reached_edge and len(visited) > 1:
        filled_tiles = len(visited)
        print(f"{edges} edges + {filled_tiles} filled tiles = {edges + filled_tiles}")

# x0, y0 = top_left
# x1, y1 = bottom_right
# print(grid[y0 - 5 : y1 + 5, x0 - 5 : x1 + 5])
# print(grid[x0, y0])
