from dataclasses import dataclass
import time


def read_file(path: str) -> list[str]:
    with open(path, "r") as f:
        return [line.strip() for line in f.readlines()]


def parse_numbers(numbers: str) -> list[int]:
    return [int(x) for x in numbers.split()]


@dataclass
class Card:
    key_numbers: list[int]
    numbers: list[int]

    @classmethod
    def from_str(cls, raw: str) -> "Card":
        _, data = raw.split(":")
        key_numbers, numbers = [parse_numbers(x.strip()) for x in data.split("|")]
        return cls(key_numbers, numbers)


lines = read_file("data/input")

start = time.time()

cards = [Card.from_str(line) for line in lines]
card_counts = dict.fromkeys(range(len(cards)), 1)

for i, card in enumerate(cards):
    wins = set(card.key_numbers).intersection(set(card.numbers))
    win_count = len(wins)

    for k in range(i + 1, i + win_count + 1):
        card_counts[k] += card_counts[i]

end = time.time()

result = sum(card_counts.values())
print(f"{result} in {end - start} seconds")
