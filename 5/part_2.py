from dataclasses import dataclass, field
import re
from typing import Optional, TypeVar

from util import chunk_by_size, chunk_by_value

T = TypeVar("T")


def read_file(path: str) -> list[str]:
    with open(path, "r") as f:
        return f.readlines()


@dataclass
class Range:
    start: int
    length: int

    end: int = field(init=False)

    def __post_init__(self):
        self.end = self.start + self.length - 1

    def __contains__(self, value: int) -> bool:
        return value in self.src

    def intersect(self, r: "Range") -> Optional["Range"]:
        if (r.start > self.end) or (r.end < self.start):
            return None

        start_value = max(self.start, r.start)
        end_value = min(self.end, r.end)

        return Range(start=start_value, length=end_value - start_value + 1)

    def difference(self, ranges: list["Range"]) -> list["Range"]:
        if len(ranges) == 0:
            return [self]

        r0 = ranges[0]
        if r0 == self:
            return []

        result = []

        ranges.sort(key=lambda r: r.start)

        if ranges[0].start > self.start:
            result.append(Range(start=self.start, length=ranges[0].start - self.start + 1))

        for i in range(len(ranges)):
            r = ranges[i]
            if r.start < self.end and r.end > self.end:
                break

            start = r.end
            end = self.end if i == len(ranges) - 1 else ranges[i + 1].start
            result.append(Range(start, end - start + 1))

        return result

    def difference_old(self, ranges: list["Range"]) -> list["Range"]:
        if len(ranges) == 0:
            return [self]

        ranges.sort(key=lambda r: r.start)

        result = []
        cursor = self.start
        for r in ranges:
            range_length = r.start - cursor

            cursor = max(cursor, r.end + 1)

            if r.start <= cursor:
                continue

            result.append(Range(start=cursor, length=r.start - range_length))
            if cursor > self.end:
                return result

        if cursor > self.start:
            return [Range(start=cursor, length=self.end - cursor + 1)]

        return result


@dataclass
class Mapping:
    src: Range
    dest: Range

    @staticmethod
    def from_values(src_start: int, dest_start: int, length: int):
        return Mapping(src=Range(start=src_start, length=length), dest=Range(start=dest_start, length=length))

    def __contains__(self, value: int) -> bool:
        return (value >= self.src.start) and (value < self.src.end)

    def convert(self, value: int) -> Optional[int]:
        if (value < self.src.start) or (value > self.src.end):
            return None

        return self.dest.start + (value - self.src.start)

    def overlaps(self, r: Range) -> bool:
        return (r.start <= self.src.end) and (r.end >= self.src.start)

    def intersect(self, r: Range) -> Optional[Range]:
        if not self.overlaps(r):
            return None

        start_value = max(self.src.start, r.start)
        end_value = min(self.src.end, r.end)

        return Range(start=start_value, length=end_value - start_value + 1)

    def map_range(self, r: Range) -> list[Range]:
        intersection = self.src.intersect(r)
        if intersection is None:
            return r

        start_value = self.convert(intersection.start)
        length = intersection.length
        ranges = [Range(start=start_value, length=length)]

        if intersection.start > r.start:
            ranges.append(Range(start=r.start, length=intersection.start - r.start))

        if intersection.end < r.end:
            ranges.append(Range(start=intersection.end, length=r.end - intersection.end))

        return ranges


@dataclass
class ConversionMap:
    src_id: str
    dest_id: str
    mappings: list[Mapping]

    def __init__(self, src_id: str, dest_id: str, mappings: list[Mapping]):
        self.src_id = src_id
        self.dest_id = dest_id
        self.mappings = mappings

    def map_range(self, r: Range):
        result = []
        intersections = []

        for mapping in self.mappings:
            if intersection := mapping.intersect(r):
                result.extend(mapping.map_range(intersection))
                intersections.append(intersection)

        result.extend(r.difference(intersections))

        return result


def load_data(lines: list[str]):
    maps: dict[str, ConversionMap] = {}

    for conversion in chunk_by_value(lines, ""):
        descr, *data = conversion
        g = re.match(r"([^-]+)-to-([^-\s]+)", descr)
        src_id, dest_id = g.groups()

        mappings = []

        for line in data:
            dest_start, src_start, length = map(int, line.strip().split())
            mappings.append(Mapping.from_values(src_start=src_start, dest_start=dest_start, length=length))

        maps[src_id] = ConversionMap(src_id=src_id, dest_id=dest_id, mappings=mappings)

    return maps


lines = [line.strip() for line in read_file("data/input")]
seed_line, *lines = lines


seed_chunks = chunk_by_size(map(int, seed_line.removeprefix("seeds:").strip().split()), 2)
seed_ranges = [Range(start=start_value, length=length) for start_value, length in seed_chunks]

maps = load_data(lines)

key = "seed"
ranges = seed_ranges
while key in maps:
    conversion_map = maps[key]
    next_key = conversion_map.dest_id

    new_ranges = []

    for r in ranges:
        new_ranges.extend(conversion_map.map_range(r))

    ranges = new_ranges

    key = next_key


ranges.sort(key=lambda r: r.start)
# print(ranges)
print(ranges[0].start)
