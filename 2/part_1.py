def read_file(path: str) -> list[str]:
    with open(path, "r") as f:
        return f.readlines()


cube_counts = {"red": 12, "green": 13, "blue": 14}


def parse_game(gameData: str):
    info, data = gameData.split(":")
    id = int(info.split(" ")[1])

    subsets = data.split(";")
    for subset in subsets:
        for cube_data in subset.split(","):
            count, color = cube_data.strip().split(" ")
            if int(count) > cube_counts[color]:
                return None

    return id


lines = read_file("data/input")
result = [game_id for game_id in map(parse_game, lines) if game_id is not None]
print(sum(result))
