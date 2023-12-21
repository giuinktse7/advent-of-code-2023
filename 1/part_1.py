def read_file(path: str) -> list[str]:
    with open(path, "r") as f:
        return f.readlines()


total = 0
lines = read_file("data/input")
for line in lines:
    a = next(x for x in line if x.isnumeric())
    b = next(x for x in reversed(line) if x.isnumeric())
    value: str = a + b
    total += int(value)

print(total)
