from enum import Enum
import numpy as np
from dataclasses import dataclass, field
import heapq
from typing import Callable, Optional


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


def show_path(grid: np.ndarray, path: list["Pos"]):
    # s = path[0]
    # scores = [grid[s.y][s.x]]

    k = grid.tolist()
    for a, b in zip(path, path[1:]):
        # scores.append(grid[b.y][b.x])
        dx = b.x - a.x
        dy = b.y - a.y
        if dx == 1:
            k[b.y][b.x] = ">"
        elif dx == -1:
            k[b.y][b.x] = "<"
        elif dy == 1:
            k[b.y][b.x] = "v"
        elif dy == -1:
            k[b.y][b.x] = "^"
        else:
            k[b.y][b.x] = str(k[b.y][b.x])

    for x in k:
        print("".join(str(y) for y in x))
    # print(scores, sum(scores))


def lines_to_2d_nparray(data: list[str]) -> np.ndarray:
    return np.array([[int(c) for c in line] for line in data])


def read_file(path: str) -> list[str]:
    with open(path, "r") as f:
        return [line.strip() for line in f.readlines()]


def sgn(x: int) -> int:
    if x == 0:
        return 0
    return 1 if x > 0 else -1


@dataclass
class Pos:
    x: int
    y: int

    @property
    def abs(self) -> int:
        return abs(self.x) + abs(self.y)

    def __eq__(self, other):
        if not isinstance(other, Pos):
            return False
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        return Pos(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Pos(self.x - other.x, self.y - other.y)

    def dx(self, x: int):
        return Pos(self.x + x, self.y)

    def dy(self, y: int):
        return Pos(self.x, self.y + y)

    @property
    def right(self) -> tuple["Pos", Direction]:
        return self.dx(1), Direction.RIGHT

    @property
    def left(self) -> tuple["Pos", Direction]:
        return self.dx(-1), Direction.LEFT

    @property
    def up(self) -> tuple["Pos", Direction]:
        return self.dy(-1), Direction.UP

    @property
    def down(self) -> tuple["Pos", Direction]:
        return self.dy(1), Direction.DOWN

    def __getitem__(self, keys):
        return self.x if keys == 0 else self.y

    def __iter__(self):
        yield self.x
        yield self.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"


@dataclass
class Node:
    pos: Pos
    direction: Direction

    cost: int
    f: int
    consecutive: int

    parent: Optional["Node"] = field(default=None)

    def __lt__(self, other):
        return self.f < other.f

    def __eq__(self, that: object) -> bool:
        return isinstance(that, Node) and self.pos == that.pos

    def reachable_states(self, grid: np.ndarray) -> list[tuple[Pos, Direction]]:
        p = self.pos
        states: list[tuple[Pos, Direction]] = []
        match self.direction:
            case Direction.UP:
                # Must move a minimum of four blocks in that direction before it can turn (or even before it can stop at the end).
                # Can move a maximum of ten consecutive blocks without turning.
                if self.consecutive >= 4:
                    states = [p.left, p.right]

                if self.consecutive < 10:
                    states.append(p.up)
            case Direction.DOWN:
                if self.consecutive >= 4:
                    states = [p.left, p.right]

                if self.consecutive < 10:
                    states.append(p.down)
            case Direction.LEFT:
                if self.consecutive >= 4:
                    states = [p.up, p.down]

                if self.consecutive < 10:
                    states.append(p.left)
            case Direction.RIGHT:
                if self.consecutive >= 4:
                    states = [p.up, p.down]

                if self.consecutive < 10:
                    states.append(p.right)

        return [p for p in states if is_in_grid(grid, p[0])]


class State:
    data: np.ndarray

    width: int
    height: int

    open_set: list[Node] = []

    seen: dict[(Pos, Direction), (int, int)]

    def __init__(self, data: np.ndarray):
        self.data = data

        self.height, self.width = data.shape

        self.open_set = []
        self.seen = {}

    def get_cost(self, pos: Pos) -> int:
        return self.data[pos.y][pos.x]

    def add_node(self, node: Node):
        heapq.heappush(self.open_set, node)

    def has_next(self):
        return len(self.open_set) > 0

    def next(self):
        return heapq.heappop(self.open_set)


def a_star(grid: np.ndarray, heuristic_fn: Callable[[Pos, float], float], start: Pos, end: Pos):
    s = State(grid)
    s.add_node(Node(pos=start, direction=Direction.RIGHT, cost=0, f=0, consecutive=0))

    def already_seen(node: Node, cached: tuple[int, int]) -> bool:
        (left_cached, right_cached) = cached

        if node.consecutive < 4:
            return left_cached > node.consecutive
        else:
            return right_cached < node.consecutive

    while s.has_next():
        node: Node = s.next()

        # Finished?
        if node.pos == end:
            if node.consecutive < 4:
                continue
            cost = node.cost
            path = []
            while node:
                path.append(node.pos)
                node = node.parent

            return cost, path[::-1]

        key = (node.pos, node.direction)

        cached = s.seen.setdefault(key, (0, np.inf))
        low, high = cached
        if already_seen(node, cached):
            continue

        # if 1 <= cached <= 3 and cached >= node.consecutive:
        #     continue
        # else:
        #     if cached < node.consecutive:
        #         continue

        if node.consecutive < 4:
            s.seen[key] = (max(low, node.consecutive), high)
        else:
            s.seen[key] = (low, min(high, node.consecutive))

        neighbors = node.reachable_states(grid)

        for pos, direction in neighbors:
            key = (pos, direction)
            consecutive = node.consecutive + 1 if node.direction == direction else 1
            cached = s.seen.get(key, (0, np.inf))

            cost = node.cost + s.get_cost(pos)
            h = heuristic_fn(pos, end)
            f = cost + h

            new_node = Node(pos=pos, direction=direction, cost=cost, f=f, consecutive=consecutive, parent=node)
            if already_seen(new_node, cached):
                continue
            s.add_node(new_node)


def is_in_grid(grid: np.ndarray, position: Pos) -> bool:
    h, w = grid.shape
    return 0 <= position.x < w and 0 <= position.y < h


def heuristic(pos: Pos, target: Pos):
    x, y = pos
    tx, ty = target
    return abs(tx - x) + abs(ty - y)


# lines = read_file("data/test")
# lines = read_file("data/test2")
# lines = read_file("data/example")
# lines = read_file("data/example_test")
lines = read_file("data/input")
data = lines_to_2d_nparray(lines)

h, w = data.shape

start_point = Pos(0, 0)
end_point = Pos(w - 1, h - 1)

total_cost, best_path = a_star(data, heuristic, start_point, end_point)
c0 = data[start_point.y][start_point.x]


show_path(data, best_path)
print(f"total cost: {total_cost}")

# Less than 1426
