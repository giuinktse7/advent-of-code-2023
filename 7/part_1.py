from functools import cmp_to_key
from dataclasses import dataclass, field
from enum import IntEnum
from collections import Counter

CARD_VALUES = {
    "A": 13,
    "K": 12,
    "Q": 11,
    "T": 9,
    "9": 8,
    "8": 7,
    "7": 6,
    "6": 5,
    "5": 4,
    "4": 3,
    "3": 2,
    "2": 1,
    "J": 0,
}


def read_file(path: str) -> list[str]:
    with open(path, "r") as f:
        return f.readlines()


class HandType(IntEnum):
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    FULL_HOUSE = 5
    FOUR_OF_A_KIND = 6
    FIVE_OF_A_KIND = 7


def get_hand_type(cards: str):
    frequencies: dict[int, list[str]] = {}
    for k, v in Counter(cards).items():
        frequencies.setdefault(v, []).append(k)

    match max(frequencies.keys()):
        case 1:
            return HandType.HIGH_CARD
        case 2:
            return HandType.ONE_PAIR if len(frequencies[2]) == 1 else HandType.TWO_PAIR
        case 3 if 2 in frequencies:
            return HandType.FULL_HOUSE
        case 3:
            return HandType.THREE_OF_A_KIND
        case 4:
            return HandType.FOUR_OF_A_KIND
        case 5:
            return HandType.FIVE_OF_A_KIND


@dataclass
class Hand:
    cards: str
    bid: int
    hand_type: HandType = field(init=False)

    def __post_init__(self):
        self.hand_type = get_hand_type(self.cards)
        pass


def compare_hands(a: Hand, b: Hand) -> int:
    if a.hand_type != b.hand_type:
        return a.hand_type - b.hand_type

    i = 0
    while a.cards[i] == b.cards[i]:
        i += 1

    return CARD_VALUES[a.cards[i]] - CARD_VALUES[b.cards[i]]


lines = read_file("data/input")
data = [x.split() for x in lines]
hands = [Hand(cards, int(bid)) for cards, bid in data]
hands = sorted(hands, key=cmp_to_key(compare_hands))


winnings = [(i + 1) * hand.bid for i, hand in enumerate(hands)]
print(winnings)
print(sum(winnings))
