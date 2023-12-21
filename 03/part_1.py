from dataclasses import dataclass


def read_file(path: str) -> str:
    with open(path, "r") as f:
        return f.readlines()


rows = [line.strip() for line in read_file("data/input")]


@dataclass
class MapNumber:
    value: int
    x0: int
    x1: int
    y: int


class Map:
    data: list[str]
    width: int
    height: int

    def __init__(self, rows: list[str]):
        self.data = "".join(rows).replace(r"\s+", "")
        self.width = len(rows[0])
        self.height = len(rows)

    def get_char(self, x: int, y: int) -> str:
        i = y * self.height + x
        return self.data[i]

    def is_symbol(self, x: int, y: int) -> bool:
        c = self.get_char(x, y)
        return not (c == "." or c.isnumeric())

    def is_numeric(self, x: int, y: int) -> bool:
        c = self.get_char(x, y)
        return c.isnumeric()

    def has_adjacent_symbol(self, map_number: MapNumber):
        from_x = map_number.x0
        to_x = map_number.x1
        y = map_number.y

        x0 = max(from_x - 1, 0)
        x1 = min(to_x + 1, self.width - 1)

        positions = []

        # same row
        if x0 != from_x:
            positions.append((x0, y))
        if x1 != to_x:
            positions.append((x1, y))

        # row above
        if y > 0:
            positions.extend([(x, y - 1) for x in range(x0, x1 + 1)])

        # row below
        if y < self.height - 1:
            positions.extend([(x, y + 1) for x in range(x0, x1 + 1)])

        return any((self.is_symbol(x, y) for (x, y) in positions))

    def get_number(self, x: int, y: int) -> MapNumber:
        x0 = x

        digits = ""
        while x < self.width:
            c = self.get_char(x, y)
            if not c.isnumeric():
                break

            digits += c
            x += 1

        return MapNumber(int(digits), x0, x - 1, y)


m = Map(rows)
total = 0

for y in range(m.height):
    x = 0
    while x < m.width:
        if m.is_numeric(x, y):
            map_number = m.get_number(x, y)
            x = map_number.x1

            if m.has_adjacent_symbol(map_number):
                total += map_number.value

        x += 1

print(total)
