def read_file(path: str) -> list[str]:
    with open(path, "r") as f:
        return f.readlines()


tokens = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}
token_lengths = set([len(x) for x in tokens])


def find_first_match(value: str, reverse: bool = False):
    if reverse:
        value = value[::-1]

    i = 0
    while i < len(value):
        c = value[i]
        if c.isnumeric():
            return c
        else:
            for token_length in token_lengths:
                s = value[i : i + token_length]
                token_candidate = s if not reverse else s[::-1]
                if token_candidate in tokens:
                    return tokens[token_candidate]
        i += 1


total = 0
lines = read_file("data/input")
for line in lines:
    line = line.strip()
    a = find_first_match(line)
    b = find_first_match(line, reverse=True) or a
    total += int(a + b)

print(total)
