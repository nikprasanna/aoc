from enum import Enum
from typing import List

FILENAME = "./aoc7.txt"

with open(FILENAME) as file:
    raw_data = [line.rstrip() for line in file]

SUIT_VALUES = [2, 3, 4, 5, 6, 7, 8, 9, 'T', 'J', 'Q', 'K', 'A']

SUIT_MAP = {
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'T': 10,
    'J': 11,
    'Q': 12,
    'K': 13,
    'A': 14,
}

class WinningTypes(Enum):
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    FULL_HOUSE = 4
    FOUR_OF_A_KIND = 5
    FIVE_OF_A_KIND = 6

class Hand:
    cards: List[str]
    bid: int

    def __init__(self, raw_hand: str):
        self.cards = list(raw_hand.split()[0])
        self.bid = int(raw_hand.split()[1])

        print(self.cards, self.bid)

    def play_round(self, opponent_hand: 'Hand'):
        pass

for raw_value in raw_data:
    hand = Hand(raw_value)

# Bucket all cards into their winning type (play_round)
# Sort each bucket (implement sort method on Hand to compare first card)
# Iterate through winning hands from FIVE_OF_A_KIND down