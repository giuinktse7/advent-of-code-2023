from enum import Enum
from functools import reduce
from typing import Optional
import numpy as np


def read_file(path: str) -> str:
    with open(path, "r") as f:
        return f.read()


class TileType(Enum):
    EMPTY = 0
    HORIZONTAL = 1
    VERTICAL = 2
    FORWARD_SLASH = 3
    BACK_SLASH = 4
    VOID = 5


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class State:
    data: np.ndarray
    energized: np.ndarray
    lights: list[(int, int, Direction)]

    seen_light_states: set[tuple[int, int, Direction]]

    rows: int
    cols: int

    def __init__(self, data: np.ndarray):
        self.data = data
        self.energized = np.zeros(data.shape)

        self.lights = []

        self.rows = data.shape[0]
        self.cols = data.shape[1]

        self.seen_light_states = set()

    def has_seen_light_state(self, light: tuple[int, int, Direction]) -> bool:
        return light in self.seen_light_states

    def show_energized(self, light_spot: Optional[tuple[int, int]] = None):
        rows = self.energized.tolist()
        result = []
        for row in enumerate(rows):
            if light_spot and row[0] == light_spot[0]:
                row[1][light_spot[1]] = 2

            result.append("".join(list(map(lambda x: "." if x == 0 else "#" if x == 1 else "L", row[1]))))
        return "\n".join(result)

    def count_energized(self) -> int:
        return np.sum(self.energized)

    def next_mirror(self, row: int, col: int, direction: Direction) -> tuple[int, int, TileType]:
        match direction:
            case Direction.UP:
                if row == 0:
                    return row, col, TileType.VOID

                res = np.argwhere(~np.isin(self.data[:row, col][::-1], [TileType.EMPTY.value, TileType.VERTICAL.value]))
                if len(res) > 0:
                    r = row - (res[0, 0] + 1)
                    return r, col, TileType(self.data[r, col])
                else:
                    return 0, col, TileType.VOID
            case Direction.RIGHT:
                if col == self.cols - 1:
                    return row, col, TileType.VOID

                res = np.argwhere(
                    ~np.isin(self.data[row, col + 1 :], [TileType.EMPTY.value, TileType.HORIZONTAL.value])
                )
                if len(res) > 0:
                    c = res[0, 0] + col + 1
                    return row, c, TileType(self.data[row, c])
                else:
                    return row, self.cols - 1, TileType.VOID
            case Direction.DOWN:
                if row == self.rows - 1:
                    return row, col, TileType.VOID

                res = np.argwhere(~np.isin(self.data[row + 1 :, col], [TileType.EMPTY.value, TileType.VERTICAL.value]))
                if len(res) > 0:
                    r = res[0, 0] + row + 1
                    return r, col, TileType(self.data[r, col])
                else:
                    return self.rows - 1, col, TileType.VOID
            case Direction.LEFT:
                if col == 0:
                    return row, col, TileType.VOID

                res = np.argwhere(
                    ~np.isin(self.data[row, :col][::-1], [TileType.EMPTY.value, TileType.HORIZONTAL.value])
                )
                if len(res) > 0:
                    c = col - (res[0, 0] + 1)
                    return row, c, TileType(self.data[row, c])
                else:
                    return row, 0, TileType.VOID

    def energize(self, r0: int, c0: int, r1: int, c1: int):
        if r0 == r1:
            c_from = min(c0, c1)
            c_to = max(c0, c1) + 1
            self.energized[r0, c_from:c_to] = 1
        else:
            r_from = min(r0, r1)
            r_to = max(r0, r1) + 1
            self.energized[r_from:r_to, c0] = 1

    def step(self):
        lights = []
        for light in self.lights:
            if self.has_seen_light_state(light):
                continue

            self.seen_light_states.add(light)

            r0, c0, direction = light
            r1, c1, tile = self.next_mirror(r0, c0, direction)
            self.energize(r0, c0, r1, c1)
            if tile == TileType.VOID:
                continue

            match tile:
                case TileType.HORIZONTAL:
                    assert direction in [Direction.UP, Direction.DOWN]
                    lights.append((r1, c1, Direction.RIGHT))
                    lights.append((r1, c1, Direction.LEFT))
                case TileType.VERTICAL:
                    assert direction in [Direction.RIGHT, Direction.LEFT]
                    lights.append((r1, c1, Direction.UP))
                    lights.append((r1, c1, Direction.DOWN))
                case TileType.FORWARD_SLASH:
                    match direction:
                        case Direction.UP:
                            lights.append((r1, c1, Direction.RIGHT))
                        case Direction.RIGHT:
                            lights.append((r1, c1, Direction.UP))
                        case Direction.DOWN:
                            lights.append((r1, c1, Direction.LEFT))
                        case Direction.LEFT:
                            lights.append((r1, c1, Direction.DOWN))
                case TileType.BACK_SLASH:
                    match direction:
                        case Direction.UP:
                            lights.append((r1, c1, Direction.LEFT))
                        case Direction.RIGHT:
                            lights.append((r1, c1, Direction.DOWN))
                        case Direction.DOWN:
                            lights.append((r1, c1, Direction.RIGHT))
                        case Direction.LEFT:
                            lights.append((r1, c1, Direction.UP))

        self.lights = lights


def get_starting_light(start_tile: TileType) -> tuple[int, int, Direction]:
    match start_tile:
        case TileType.HORIZONTAL:
            return 0, 0, Direction.RIGHT
        case TileType.VERTICAL:
            return 0, 0, Direction.DOWN
        case TileType.BACK_SLASH:
            return 0, 0, Direction.DOWN
        case _:
            raise Exception("Invalid start tile")


def run():
    raw_data = read_file("data/input")
    mapping = [
        (".", TileType.EMPTY),
        ("/", TileType.FORWARD_SLASH),
        ("-", TileType.HORIZONTAL),
        ("\\", TileType.BACK_SLASH),
        ("|", TileType.VERTICAL),
    ]
    data = reduce(lambda acc, next: acc.replace(next[0], str(next[1].value)), mapping, raw_data)
    rows = [[int(c) for c in row] for row in data.split("\n")]

    s = State(np.array(rows))

    start_light = get_starting_light(TileType(s.data[0, 0]))
    s.lights.append(start_light)
    while len(s.lights) > 0:
        s.step()

    print(s.count_energized())


run()
