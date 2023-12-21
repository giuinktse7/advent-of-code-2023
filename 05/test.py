from dataclasses import dataclass


@dataclass
class Range:
    start: int
    end: int


def difference(r: Range, ranges: list[Range]) -> list[Range]:
    result = []

    ranges.sort(key=lambda r: r.start)
    for i in range(len(ranges)):
        if ranges[i].start < r.end and ranges[i].end > r.end:
            break

        start = min(ranges[i].end, r.end)
        end = r.end if i == len(ranges) - 1 else ranges[i + 1].start
        result.append(Range(start, end))

    return result


a = Range(100, 200)
b = [Range(90, 105), Range(150, 160), Range(170, 180), Range(190, 300)]

print(difference(a, b))
