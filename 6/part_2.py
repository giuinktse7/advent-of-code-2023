import re
from math import floor, ceil, sqrt


def read_file(path: str) -> list[str]:
    with open(path, "r") as f:
        return f.readlines()


lines = read_file("data/input")
data = [x.split(":")[1].strip() for x in lines]
race_time, record_distance = [int(re.sub(r"\s+", "", x)) for x in data]


def f(t: int, r: int) -> (int, int):
    p = sqrt(t**2 - 4 * r)
    lower_bound = floor((1 / 2) * (t - p))
    upper_bound = ceil((1 / 2) * (p + t))

    return upper_bound - lower_bound - 1


result = f(race_time, record_distance)
print(result)
