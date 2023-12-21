import re
import time
from typing import Generator


def read_file(path: str) -> list[str]:
    with open(path, "r") as f:
        return [line.strip() for line in f.readlines()]


lines = read_file("data/input")


def find_consec_overlapping(s: str, size: int, indent: int = 0) -> Generator[int, None, None]:
    i = 0
    first_index = s.find("#")
    end = first_index if first_index != -1 else len(s)
    end = min(end, len(s) - size)
    while i <= end:
        k = s[i : i + size]

        stop_index = k.find(".")
        if stop_index != -1:
            i += stop_index + 1
            continue

        if (i + size) == len(s) or s[i + size] != "#":
            yield i

        i += 1


def completable(pattern: str, groups: list[int]):
    if len(pattern) < len(groups):
        return False
    if len(pattern) < sum(groups) + len(groups) - 1:
        return False

    n_dots = len(re.findall(r"[?.]", pattern))
    if n_dots < len(groups) - 1:
        return False

    if len(re.findall(r"[?#]", pattern)) < sum(groups):
        return False

    return True


def solve(current: str, remaining: str, groups: list[int]):
    if len(groups) == 0:
        return 0 if "#" in remaining else 1

    if known_dead_ends.get(len(groups), -1) >= len(remaining):
        return 0

    cache_id = (len(remaining), len(groups))
    if cached := cached_states.get(cache_id):
        return cached

    if not completable(remaining, groups):
        for n_groups in range(len(groups) + 1):
            min_remaining_required = max(known_dead_ends.get(n_groups, 0), len(remaining))
            known_dead_ends[n_groups] = min_remaining_required

        return 0

    size = groups[0]
    total_arrangements = 0
    for i0 in find_consec_overlapping(remaining, size):
        # print(i0)
        i1 = i0 + size + 1

        c = current
        # Set question marks before the current group to dots
        c += remaining[:i0].replace("?", ".")
        # Set the current group to #
        c += "".join(["#"] * size)
        # Set question marks after the current group to dots
        if i1 <= len(remaining):
            c += "."

        arrangements = solve(c, remaining[i1:], groups[1:])
        if arrangements == 0 and total_arrangements == 0 and "#" not in remaining[i1:]:
            for n_groups in range(len(groups) + 1):
                min_remaining_required = max(known_dead_ends.get(n_groups, 0), len(remaining))
                known_dead_ends[n_groups] = min_remaining_required
            cached_states[cache_id] = 0
            return 0

        total_arrangements += arrangements

    cached_states[cache_id] = total_arrangements

    return total_arrangements


# len(remaining)_len(groups) -> arrangements
cached_states = {}
# len(groups) -> min(len(remaining))
known_dead_ends = {}


def run():
    start = time.time()
    total_arrangements = 0
    for line in lines:
        row, groups = line.split(" ")
        row = "?".join([row] * 5)
        groups = ",".join([groups] * 5)

        groups = [int(x) for x in groups.split(",")]

        cached_states.clear()
        known_dead_ends.clear()
        arrangements = solve(current="", remaining=row, groups=groups)
        total_arrangements += arrangements

    print(f"{total_arrangements} in {time.time() - start} seconds")


run()
