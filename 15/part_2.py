from typing import Optional, TypeVar


T = TypeVar("T")


def read_file(path: str) -> list[str]:
    with open(path, "r") as f:
        return f.readlines()


line = read_file("data/input")[0]
data = line.split(",")


def run_hash(x: str) -> int:
    value = 0
    for c in x:
        ascii = ord(c)
        value += ascii
        value *= 17
        value %= 256

    return value


def remove_first(xs: list[T], f: lambda x: bool) -> None:
    for i, x in enumerate(xs):
        if f(x):
            del xs[i]
            return


def find_first_index(xs: list[T], f: lambda x: bool) -> Optional[int]:
    for i, x in enumerate(xs):
        if f(x):
            return i
    return None


class State:
    boxes: list[int, list[tuple[str, int]]]

    def __init__(self):
        self.boxes = {}

    def execute_step(self, step: str):
        is_remove = step[-1] == "-"
        if is_remove:
            label = step[:-1]
            self.remove(label)
        else:
            label, focal_length = step.split("=")
            self.add(label, int(focal_length))

    def add(self, label: str, focal_length: int):
        h = run_hash(label)
        box = self.boxes.setdefault(h, [])

        match find_first_index(box, lambda x: x[0] == label):
            case None:
                box.append((label, focal_length))
            case i:
                box[i] = (label, focal_length)

    def remove(self, label: str):
        h = run_hash(label)
        if h in self.boxes:
            k = self.boxes[h]

            remove_first(self.boxes[h], lambda x: x[0] == label)
            if len(k) == 0:
                del self.boxes[h]


def run():
    s = State()

    for step in data:
        s.execute_step(step)

    boxes = s.boxes
    total_focusing_power = 0
    for box in boxes.keys():
        for slot, value in enumerate(boxes[box]):
            _, focal_length = value
            total_focusing_power += (box + 1) * (slot + 1) * focal_length

    print(total_focusing_power)


run()
