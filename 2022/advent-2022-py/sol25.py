
import argparse as ap
import re
import sys
import pyperclip
from datetime import datetime
from typing import List, Dict, Set, Callable, Tuple, Union, Optional, Any
from tqdm import tqdm, trange
from collections import defaultdict


CONVERTER = {
    '2': 2,
    '1': 1,
    '0': 0,
    '-': -1,
    '=': -2
}

NEGATE = {
    '2': '=',
    '1': '-',
    '0': '0',
    '-': '1',
    '=': '2'
}

DECONVERTER = {v: k for k, v in CONVERTER.items()}


def snafu_to_decimal(snafu: str) -> int:
    total = 0
    for c in snafu:
        total += CONVERTER[c]
        total *= 5

    return total // 5


def decimal_to_snafu(decimal: int, pos: int=0) -> str:
    if -2 <= decimal <= 2 and pos <= 1:
        return DECONVERTER[decimal]
    
    mul = 1
    if decimal < 0:
        mul = -1
        decimal *= -1

    # First find the largest power of 5 that fits in decimal
    power = pos
    while 5 ** power <= decimal:
        power += 1
    
    power -= 1
    # Does it start with a 2 or 1?
    result = ""
    if decimal <= sum(2 * 5 ** i for i in range(power)):
        result = DECONVERTER[0] + decimal_to_snafu(decimal, power)
    elif decimal <= 5 ** power + sum(2 * 5 ** i for i in range(power)):
        result = DECONVERTER[1] + decimal_to_snafu(decimal - 5 ** power, power)
    elif decimal <= sum(2 * 5 ** i for i in range(power + 1)):
        result = DECONVERTER[2] + decimal_to_snafu(decimal - 2 * 5 ** power, power)
    elif decimal <= 5 ** (power + 1):
        result = DECONVERTER[1] + decimal_to_snafu(decimal - 5 ** (power + 1), power + 1)
    else:
        result = DECONVERTER[2] + decimal_to_snafu(
            decimal - 2 * 5 ** (power + 1), power + 1)
    
    if mul == -1:
        result = "".join(NEGATE[c] for c in result)
    
    return result


class Solution:
    def __init__(self, filename: str):
        with open(filename, "r") as f:
            self.input = f.read()
            self.input_lines = self.input.splitlines()

    def solve_part1(self) -> str:
        total = 0
        for line in self.input_lines:
            total += snafu_to_decimal(line)
        
        return decimal_to_snafu(total)

    def solve_part2(self) -> int:
        pass


if __name__ == "__main__":
    parser = ap.ArgumentParser()
    parser.add_argument(
        "-e",
        "--example",
        help="Use the example file for input instead of main",
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

    for i in range(500):
        try:
            assert snafu_to_decimal(decimal_to_snafu(i)) == i
        except AssertionError:
            print(f"Failed for {i}")
            raise

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
