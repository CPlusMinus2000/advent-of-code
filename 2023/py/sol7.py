import argparse as ap
import re
import sys
import pyperclip
from datetime import datetime
from typing import List, Dict, Set, Callable, Tuple, Union, Optional, Any
from tqdm import tqdm, trange
from collections import defaultdict
from functools import cmp_to_key


POINT_VALS = {str(i): i for i in range(2, 10)} | {
    "T": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14,
}

JUNK = 0
PAIR = 1
TWO_PAIR = 2
THREE = 3
FULL_HOUSE = 4
FOUR = 5
FIVE = 6
PART2 = False


def type_of_hand(hand: str):
    if len(set(hand)) == 5:
        return JUNK
    elif len(set(hand)) == 4:
        return PAIR
    elif any(hand.count(card) == 3 for card in hand) and len(set(hand)) == 3:
        return THREE
    elif len(set(hand)) == 3:
        return TWO_PAIR
    elif any(hand.count(card) == 4 for card in hand):
        return FOUR
    elif len(set(hand)) == 2:
        return FULL_HOUSE
    else:
        return FIVE


def cmp_hands(hand1: str, hand2: str) -> int:
    best_hand_1, best_hand_2 = type_of_hand(hand1), type_of_hand(hand2)

    if best_hand_1 > best_hand_2:
        return 1
    elif best_hand_1 < best_hand_2:
        return -1
    else:
        for i in range(5):
            if POINT_VALS[hand1[i]] > POINT_VALS[hand2[i]]:
                return 1
            elif POINT_VALS[hand1[i]] < POINT_VALS[hand2[i]]:
                return -1

    return 0


cmp_hands_key = cmp_to_key(cmp_hands)


class Solution:
    def __init__(self, filename: str):
        with open(filename, "r") as f:
            self.input = f.read()
            self.input_lines = self.input.splitlines()

    def solve_part1(self) -> int:
        hands = []
        for line in self.input_lines:
            hand, bid = line.split()
            bid = int(bid)
            hands.append((hand, bid))

        hands.sort(key=lambda x: cmp_hands_key(x[0]))
        sum = 0
        for i in range(len(hands)):
            print(hands[i])
            sum += (i + 1) * hands[i][1]

        return sum

    def solve_part2(self) -> int:
        global PART2
        PART2 = True

        hands = []
        for line in self.input_lines:
            hand, bid = line.split()
            bid = int(bid)
            hands.append((hand, bid))

        hands.sort(key=lambda x: cmp_hands_key(x[0]))
        sum = 0
        for i in range(len(hands)):
            print(hands[i])
            sum += (i + 1) * hands[i][1]

        return sum


if __name__ == "__main__":
    parser = ap.ArgumentParser()
    parser.add_argument(
        "-e",
        "--example",
        help="Use the example file for input instead of main",
        action="store_true",
    )

    parser.add_argument(
        "-m",
        "--michael",
        help="Use Michael's input file",
        action="store_true",
    )

    args = parser.parse_args()
    day = re.search(r"\d+", sys.argv[0])
    if day:
        day = day.group(0)
    else:
        day = datetime.now().day + 1

    filename = f"../data/day{day}.txt"
    if args.example:
        filename = f"../data/day{day}ex.txt"
    elif args.michael:
        filename = f"../data/day{day}m.txt"

    sol = Solution(filename)
    x = sol.solve_part1()
    print(f"Part 1: {x}")
    if x is not None:
        pyperclip.copy(x)

    sol = Solution(filename)
    x = sol.solve_part2()
    print(f"Part 2: {x}")
    if x is not None:
        pyperclip.copy(x)
