import numpy as np
from enum import Enum


def read_file(path: str) -> list[str]:
    with open(path, "r") as f:
        return [line.strip() for line in f.readlines()]


class TileType(Enum):
    EMPTY = 0
    ROUND_ROCK = 1
    CUBE_ROCK = 2


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


lines = read_file("data/input")
# lines = read_file("data/example")
lines = [parse_line(line) for line in lines]
data = np.array(lines)
print(data.shape)


def round_rock_indices(data: np.ndarray):
    return np.argwhere(data == TileType.ROUND_ROCK.value)


def slide_north(data: np.ndarray):
    rows = data.shape[0]
    loads = []
    for [y, x] in round_rock_indices(data):
        x0, y0 = x, y
        while y > 0 and data[y - 1, x] == TileType.EMPTY.value:
            y -= 1

        if y0 != y:
            data[y, x] = TileType.ROUND_ROCK.value
            data[y0, x0] = TileType.EMPTY.value

        loads.append(rows - y)

    print(sum(loads))


slide_north(data)
