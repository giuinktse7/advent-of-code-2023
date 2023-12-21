from functools import cmp_to_key
from dataclasses import dataclass, field
from enum import IntEnum
from collections import Counter
from typing import Tuple

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
    counter = Counter(cards)
    joker_count = counter.pop("J", 0)

    counts = sorted(list(counter.values()), reverse=True)
    if len(counts) < 2:
        return HandType.FIVE_OF_A_KIND

    r1, r2 = counts[:2]
    r1 += joker_count

    match r1, r2:
        case 5, 0:
            return HandType.FIVE_OF_A_KIND
        case 4, 1:
            return HandType.FOUR_OF_A_KIND
        case 3, 2:
            return HandType.FULL_HOUSE
        case 3, _:
            return HandType.THREE_OF_A_KIND
        case 2, 2:
            return HandType.TWO_PAIR
        case 2, _:
            return HandType.ONE_PAIR
        case _:
            return HandType.HIGH_CARD


@dataclass
class Hand:
    cards: str
    bid: int
    hand_type: HandType = field(init=False)

    def __post_init__(self):
        self.hand_type = get_hand_type(self.cards)
        pass


def first_different_chars(a: str, b: str) -> Tuple[str, str]:
    i = 0
    while a[i] == b[i]:
        i += 1

    return a[i], b[i]


def compare_hands(h1: Hand, h2: Hand) -> int:
    if h1.hand_type != h2.hand_type:
        return h1.hand_type - h2.hand_type

    c1, c2 = first_different_chars(h1.cards, h2.cards)
    return CARD_VALUES[c1] - CARD_VALUES[c2]


lines = read_file("data/input")
data = [x.split() for x in lines]
hands = [Hand(cards, int(bid)) for cards, bid in data]
hands = sorted(hands, key=cmp_to_key(compare_hands))

winnings = [(i + 1) * hand.bid for i, hand in enumerate(hands)]
print(sum(winnings))
