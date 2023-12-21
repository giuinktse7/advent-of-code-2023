from dataclasses import InitVar, dataclass
from queue import Queue
import re
from typing import Optional


def read_file(path: str) -> list[str]:
    with open(path, "r") as f:
        return [line.strip() for line in f.readlines()]


# lines = read_file("data/example")
lines = read_file("data/input")


def find_consec_overlapping(s: str, size: int, indent: int = 0) -> list[int]:
    indent_str = "  " * indent
    # print(f"{indent_str}Finding {size} in {s}")
    result = []
    i = 0
    first_index = s.find("#")
    end = first_index if first_index != -1 else len(s)
    end = min(end, len(s) - size)
    while i <= end:
        prev = s[:i]
        post = s[i + size :]
        k = s[i : i + size]
        stop_index = k.find(".")
        if stop_index != -1:
            i += stop_index + 1
            continue

        post_ok = (i + size) == len(s) or s[i + size] != "#"
        if post_ok:
            # print(f"{indent_str}{prev}[{k}]{post} (A)")
            result.append(i)
            i += 1
        else:
            # print(f"{indent_str}{prev}[{k}]{post}")
            i += 1

    return result


def validate_solution(solution: str, groups: list[int]):
    assert "?" not in solution
    # print("Validate")
    i0 = 0
    for size in groups:
        # print(f"Current solution: {solution[i0:]}")
        start = solution[i0:].find("#")
        value = solution[i0 + start : i0 + start + size]
        # print(f"value: '{value}', size: {size}")
        i0 += start + size + 1
        if value != "".join(["#"] * size):
            # print(f"Invalid solution starting at {i0}: {value} != {''.join(['#'] * size)}")
            return False

    return True


THE_SOLUTIONS = []


def solve(current: str, remaining: str, groups: list[int], original_row: str, original_groups: list[int]):
    indent = len(original_groups) - len(groups)
    indent_str = "  " * (len(original_groups) - len(groups))
    if len(groups) == 0:
        if "#" in remaining:
            # Not a valid solution
            return 0

        # print(f"{indent_str}Found solution: {current}")
        THE_SOLUTIONS.append(current + remaining.replace("?", "."))
        if not validate_solution(current, original_groups):
            # print(original_row, original_groups)
            raise Exception("Invalid solution")
        return 1

    # print(f"{indent_str}Solving for '{current} {remaining}' with {groups}")

    size = groups[0]
    r = r"(?:^|[^#])([?#]{" + str(size) + r"}(?:[^#]|$))"
    total_arrangements = 0
    # for g in re.finditer(f"(?=({r}))", remaining):
    # i0 = g.start()
    for cnt, i0 in enumerate(find_consec_overlapping(remaining, size, indent=indent)):
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

        # print(
        #     f"{current} {len(current)} {remaining} {len(remaining)} -> {c} {len(c)} {remaining[i1:]} {len(remaining[i1:])}"
        # )
        next_remaining = remaining[i1:]
        if next_remaining == "..??...?##.":
            k = 5
        # print(f"{indent_str}Using [{cnt}]")
        arrangements = solve(c, remaining[i1:], groups[1:], original_row, original_groups)
        total_arrangements += arrangements

    return total_arrangements


total_arrangements = 0
for line in lines:
    # line = "??????????#?#???#?? 3,10"
    row, groups = line.split(" ")
    groups = [int(x) for x in groups.split(",")]

    # print("--------------------------")
    # print(f"row: {row} ({groups})")

    total_arrangements += solve("", row, groups, row, groups)
    # print(total_arrangements)
    # print(row)
    # for s in THE_SOLUTIONS:
    #     print(" ".join([x for x in s]), len(s))
    # exit(0)

print(total_arrangements)


# ?.?#.???#?????? [1, 9]

# #..#.#########.
# ?###???????#?..?? 7,1
# row = "????????????????#?..??"
# size = 14
# indices = find_consec_overlapping(row, size)
# print("Solutions:")
# for i in indices:
#     a = row[:i]
#     b = row[i : i + size]
#     c = row[i + size :]
#     print(f"{a}[{b}]{c}")


# (6057, 7408)
# 7364
# not 6113
