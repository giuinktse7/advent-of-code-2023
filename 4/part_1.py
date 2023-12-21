from dataclasses import dataclass


def read_file(path: str) -> list[str]:
    with open(path, "r") as f:
        return [line.strip() for line in f.readlines()]


def parse_numbers(numbers: str) -> list[int]:
    return [int(number.strip()) for number in numbers.split(" ") if number.strip() != ""]


@dataclass
class Card:
    key_numbers: list[int]
    numbers: list[int]

    @classmethod
    def from_str(cls, raw: str) -> "Card":
        _, data = raw.split(":")
        key_numbers, numbers = list(map(parse_numbers, [x.strip() for x in data.split("|")]))
        return cls(key_numbers, numbers)


def score(card: Card) -> int:
    wins = set(card.key_numbers).intersection(set(card.numbers))
    win_count = len(wins)

    return 0 if win_count == 0 else pow(2, win_count - 1)


lines = read_file("data/input")

cards = [Card.from_str(line) for line in lines]
scores = [score(card) for card in cards]
print(sum(scores))
