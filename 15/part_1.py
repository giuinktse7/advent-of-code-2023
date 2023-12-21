def read_file(path: str) -> list[str]:
    with open(path, "r") as f:
        return f.readlines()


line = read_file("data/input")[0]
# line = read_file("data/example")[0]
data = line.split(",")
print(data)


def run_hash(x: str) -> int:
    value = 0
    for c in x:
        ascii = ord(c)
        value += ascii
        value *= 17
        value %= 256

    return value


print(sum([run_hash(x) for x in data]))
