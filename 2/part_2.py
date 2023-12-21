import numpy as np


def read_file(path: str) -> list[str]:
    with open(path, "r") as f:
        return f.readlines()


def parse_game(gameData: str):
    _, data = gameData.split(":")

    required = {}

    subsets = data.split(";")
    for subset in subsets:
        for cube_data in subset.split(","):
            count, color = cube_data.strip().split(" ")
            required[color] = max(required.get(color, 0), int(count))

    return np.prod(list(required.values()))


lines = read_file("data/input")
result = [game_id for game_id in map(parse_game, lines) if game_id is not None]
print(sum(result))
