from dataclasses import dataclass
import re
from typing import Generator, Optional, TypeVar

T = TypeVar("T")


def read_file(path: str) -> list[str]:
    with open(path, "r") as f:
        return f.readlines()


@dataclass
class Mapping:
    src_start: int
    dest_start: int

    length: int

    def convert(self, value: int) -> Optional[int]:
        if (value < self.src_start) or (value >= self.src_start + self.length):
            return None

        return self.dest_start + (value - self.src_start)


@dataclass
class ConversionMap:
    src_id: str
    dest_id: str
    mappings: list[Mapping]

    def convert(self, value: int):
        candidates = (m.convert(value) for m in self.mappings)
        result = next((c for c in candidates if c is not None), None)

        return result or value


def chunk_by_value(xs: list[T], value: T) -> Generator[T, None, None]:
    chunk = []
    for x in xs:
        if x == value and len(chunk) > 0:
            yield chunk
            chunk = []
        else:
            if x != "":
                chunk.append(x)

    yield chunk


lines = [line.strip() for line in read_file("data/input")]
seed_line, *lines = lines

seeds = list(map(int, seed_line.removeprefix("seeds:").strip().split()))


def load_data():
    # "src -> dest" -> Mapping
    maps: dict[str, ConversionMap] = {}

    for conversion in chunk_by_value(lines, ""):
        descr, *data = conversion
        g = re.match(r"([^-]+)-to-([^-\s]+)", descr)
        src_id, dest_id = g.groups()

        mappings = []

        for line in data:
            dest_start, src_start, length = map(int, line.strip().split())
            mappings.append(Mapping(src_start=src_start, dest_start=dest_start, length=length))

        maps[src_id] = ConversionMap(src_id=src_id, dest_id=dest_id, mappings=mappings)

    return maps


def full_conversion(maps: dict[str, ConversionMap], seed: int) -> int:
    key = "seed"
    value = seed

    while key in maps:
        conversion_map = maps[key]
        src_id = conversion_map.src_id
        dest_id = conversion_map.dest_id

        new_value = maps[key].convert(value)
        # print(f"{src_id} -> {dest_id}: {value} -> {new_value}")

        key = dest_id
        value = new_value

    return value


maps = load_data()

print(min([full_conversion(maps, seed) for seed in seeds]))

# Divide and conquer: log(n), divide search space by 2 each time. n / 2 to left and right
