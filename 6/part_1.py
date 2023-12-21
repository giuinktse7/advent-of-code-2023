from math import floor, ceil, sqrt
import numpy as np


def read_file(path: str) -> list[str]:
    with open(path, "r") as f:
        return f.readlines()


lines = read_file("data/input")
race_times, record_distances = [map(int, x.split(":")[1].strip().split()) for x in lines]


def f(t: int, r: int) -> (int, int):
    p = sqrt(t**2 - 4 * r)
    lower_bound = floor((1 / 2) * (t - p))
    upper_bound = ceil((1 / 2) * (p + t))

    return upper_bound - lower_bound - 1


result = [f(race_time, record_distance) for race_time, record_distance in zip(race_times, record_distances)]
print(np.prod(result))
