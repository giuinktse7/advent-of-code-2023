import time
import numpy as np
from enum import Enum


def read_file(path: str) -> list[str]:
    with open(path, "r") as f:
        return [line.strip() for line in f.readlines()]


class SortOrder(Enum):
    NorthToSouth = 0
    SouthToNorth = 1
    EastToWest = 2
    WestToEast = 3


class TileType(Enum):
    EMPTY = 0
    ROUND_ROCK = 1
    CUBE_ROCK = 2


id_map: dict[tuple[int, int], int] = {}


def parse_line(line: str):
    result = []
    for c in line:
        match c:
            case "O":
                result.append(TileType.ROUND_ROCK.value)
            case "#":
                result.append(TileType.CUBE_ROCK.value)
            case ".":
                result.append(TileType.EMPTY.value)

    return result


def set_stone_ids(data: np.ndarray):
    id = 0
    for [y, x] in round_rock_indices(data, SortOrder.NorthToSouth):
        id_map[(y, x)] = id
        id += 1


def round_rock_indices(data: np.ndarray, sort_order: SortOrder):
    result = np.argwhere(data == TileType.ROUND_ROCK.value)

    match sort_order:
        case SortOrder.NorthToSouth:
            return result
        case SortOrder.SouthToNorth:
            return result[::-1]
        case SortOrder.EastToWest:
            indices = np.argsort(~result[:, 1])
            return result[indices]
        case SortOrder.WestToEast:
            indices = np.argsort(result[:, 1])
            return result[indices]


def move_rock(data: np.ndarray, x0, y0, x1, y1):
    data[y1, x1] = TileType.ROUND_ROCK.value
    data[y0, x0] = TileType.EMPTY.value
    id_map[(y1, x1)] = id_map[(y0, x0)]


def slide_north(data: np.ndarray):
    for [y, x] in round_rock_indices(data, SortOrder.NorthToSouth):
        x0, y0 = x, y
        while y > 0 and data[y - 1, x] == TileType.EMPTY.value:
            y -= 1

        if y0 != y:
            move_rock(data, x0, y0, x, y)


def slide_south(data: np.ndarray):
    rows = data.shape[0]
    for [y, x] in round_rock_indices(data, SortOrder.SouthToNorth):
        x0, y0 = x, y
        while y < rows - 1 and data[y + 1, x] == TileType.EMPTY.value:
            y += 1

        if y0 != y:
            move_rock(data, x0, y0, x, y)


def slide_east(data: np.ndarray):
    cols = data.shape[1]
    for [y, x] in round_rock_indices(data, SortOrder.EastToWest):
        x0, y0 = x, y
        while x < cols - 1 and data[y, x + 1] == TileType.EMPTY.value:
            x += 1

        if x0 != x:
            move_rock(data, x0, y0, x, y)


def slide_west(data: np.ndarray):
    for [y, x] in round_rock_indices(data, SortOrder.WestToEast):
        x0, y0 = x, y
        while x > 0 and data[y, x - 1] == TileType.EMPTY.value:
            x -= 1

        if x0 != x:
            move_rock(data, x0, y0, x, y)


def total_load_on_north_beams(data: np.ndarray):
    rows = data.shape[0]
    loads = []
    for [y, x] in round_rock_indices(data, SortOrder.NorthToSouth):
        loads.append(rows - y)

    return loads


def cycle(data: np.ndarray):
    slide_north(data)
    slide_west(data)
    slide_south(data)
    slide_east(data)


# State hash -> cycle number
seen_states: dict[str, int] = {}


def run():
    lines = read_file("data/input")
    lines = [parse_line(line) for line in lines]
    data = np.array(lines)

    set_stone_ids(data)

    target_cycles = 10**9
    n_cycles = 0

    result = None
    while True:
        cycle(data)
        n_cycles += 1
        key = hash(data.data.tobytes())
        if key in seen_states:
            loop_size = n_cycles - seen_states[key]

            remaining_cycles = (target_cycles - n_cycles) % loop_size

            while remaining_cycles > 0:
                cycle(data)
                remaining_cycles -= 1

            result = total_load_on_north_beams(data)
            break

        seen_states[key] = n_cycles

    print(sum(result))


start = time.time()
run()
end = time.time()
print(f"Time: {end-start}s.")
