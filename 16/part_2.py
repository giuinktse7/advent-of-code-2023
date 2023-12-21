from enum import Enum
from functools import reduce
from typing import Generator, Optional
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


counts_as_empty = {
    Direction.UP: [TileType.EMPTY.value, TileType.VERTICAL.value],
    Direction.RIGHT: [TileType.EMPTY.value, TileType.HORIZONTAL.value],
    Direction.DOWN: [TileType.EMPTY.value, TileType.VERTICAL.value],
    Direction.LEFT: [TileType.EMPTY.value, TileType.HORIZONTAL.value],
}


def interact_with_mirror(direction: Direction, mirror: TileType) -> list[Direction]:
    match mirror:
        case TileType.HORIZONTAL:
            if direction not in [Direction.UP, Direction.DOWN]:
                return [direction]
            return [Direction.RIGHT, Direction.LEFT]
        case TileType.VERTICAL:
            if direction not in [Direction.RIGHT, Direction.LEFT]:
                return [direction]
            return [Direction.UP, Direction.DOWN]
        case TileType.FORWARD_SLASH:
            match direction:
                case Direction.UP:
                    return [Direction.RIGHT]
                case Direction.RIGHT:
                    return [Direction.UP]
                case Direction.DOWN:
                    return [Direction.LEFT]
                case Direction.LEFT:
                    return [Direction.DOWN]
        case TileType.BACK_SLASH:
            match direction:
                case Direction.UP:
                    return [Direction.LEFT]
                case Direction.RIGHT:
                    return [Direction.DOWN]
                case Direction.DOWN:
                    return [Direction.RIGHT]
                case Direction.LEFT:
                    return [Direction.UP]
        case _:
            return [direction]


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
        for i, row in enumerate(rows):
            if light_spot and i == light_spot[0]:
                row[light_spot[1]] = 2

            result.append("".join(list(map(lambda x: "." if x == 0 else "#" if x == 1 else "L", row))))
        return "\n".join(result)

    def reset(self):
        self.energized = np.zeros(self.data.shape)
        self.lights = []
        self.seen_light_states = set()

    def count_energized(self) -> int:
        return int(np.sum(self.energized))

    def get_next_interaction(self, data_slice: np.ndarray, zeroes: list[TileType]) -> int:
        res = np.argwhere(~np.isin(data_slice, zeroes))
        return next(res.flat, None)

    def next_mirror(self, row: int, col: int, direction: Direction) -> tuple[int, int, TileType]:
        empty_tiles = counts_as_empty[direction]
        m_row = row
        m_col = col
        i = 0
        match direction:
            case Direction.UP:
                if row == 0:
                    return row, col, TileType.VOID

                data_slice = self.data[:row, col][::-1]
                i = self.get_next_interaction(data_slice, empty_tiles)
                m_row = 0 if i is None else row - (i + 1)

            case Direction.RIGHT:
                if col == self.cols - 1:
                    return row, col, TileType.VOID

                data_slice = self.data[row, col + 1 :]
                i = self.get_next_interaction(data_slice, empty_tiles)
                m_col = self.cols - 1 if i is None else i + col + 1

            case Direction.DOWN:
                if row == self.rows - 1:
                    return row, col, TileType.VOID

                data_slice = self.data[row + 1 :, col]
                i = self.get_next_interaction(data_slice, empty_tiles)
                m_row = self.rows - 1 if i is None else i + row + 1

            case Direction.LEFT:
                if col == 0:
                    return row, col, TileType.VOID

                data_slice = self.data[row, :col][::-1]
                i = self.get_next_interaction(data_slice, empty_tiles)
                m_col = 0 if i is None else col - (i + 1)

        tile_type = TileType.VOID if i is None else TileType(self.data[m_row, m_col])
        return m_row, m_col, tile_type

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

            lights.extend((r1, c1, d) for d in interact_with_mirror(direction, tile))

        self.lights = lights

    def get_starting_lights(self, row: int, col: int) -> list[list[Direction]]:
        start_tile = TileType(self.data[row, col])
        directions = []
        if row == 0:
            directions.append(Direction.DOWN)

        if row == self.rows - 1:
            directions.append(Direction.UP)
        if col == 0:
            directions.append(Direction.RIGHT)

        if col == self.cols - 1:
            directions.append(Direction.LEFT)

        return [interact_with_mirror(d, start_tile) for d in directions]


def generate_square_border_indices(side_length: int) -> Generator[tuple[int, int], None, None]:
    for i in range(side_length):
        yield (0, i)
        yield (side_length - 1, i)
        yield (i, 0)
        yield (i, side_length - 1)


def parse_input(raw_data: str) -> np.ndarray:
    mapping = [
        (".", TileType.EMPTY),
        ("/", TileType.FORWARD_SLASH),
        ("-", TileType.HORIZONTAL),
        ("\\", TileType.BACK_SLASH),
        ("|", TileType.VERTICAL),
    ]
    data = reduce(lambda acc, next: acc.replace(next[0], str(next[1].value)), mapping, raw_data)
    rows = [[int(c) for c in row] for row in data.split("\n")]

    return np.array(rows)


def run():
    raw_data = read_file("data/input")
    data = parse_input(raw_data)

    s = State(data)

    solutions = []
    for row, col in generate_square_border_indices(s.rows):
        for dirs in s.get_starting_lights(row, col):
            s.lights.extend((row, col, d) for d in dirs)

            while len(s.lights) > 0:
                s.step()

            n_energized = s.count_energized()
            solutions.append(n_energized)
            s.reset()

    print(max(solutions))


run()
