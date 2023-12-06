import argparse as ap
import re
import sys
import pyperclip
from datetime import datetime
from typing import List, Dict, Set, Callable, Tuple, Union, Optional, Any
from tqdm import tqdm, trange
from collections import defaultdict


class Solution:
    def __init__(self, filename: str):
        with open(filename, "r") as f:
            self.input = f.read()
            self.input_lines = self.input.splitlines()

    def solve_part1(self) -> int:
        total = 0
        for line in self.input_lines:
            _, rest = line.split(":")
            wins, have = rest.split(" | ")
            win_nums = set(wins.strip().split())
            have_nums = have.strip().split()
            how_many = sum(1 for n in have_nums if n in win_nums)
            total += int(2 ** (how_many - 1))

        return total

    def solve_part2(self) -> int:
        total = {i + 1: 1 for i in range(len(self.input_lines))}
        for line in self.input_lines:
            cnum, rest = line.split(":")
            cnum = int(cnum.split()[-1].strip())
            wins, have = rest.split(" | ")
            win_nums = set(wins.strip().split())
            have_nums = have.strip().split()
            how_many = sum(1 for n in have_nums if n in win_nums)
            for i in range(cnum + 1, cnum + how_many + 1):
                if i <= len(self.input_lines):
                    total[i] += total[cnum]

        return sum(total.values())


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
