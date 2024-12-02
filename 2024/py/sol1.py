import argparse as ap
import re
import sys
import pyperclip
from datetime import datetime
from typing import List, Dict, Set, Callable, Tuple, Union, Optional, Any
from tqdm import tqdm, trange
from collections import Counter, defaultdict


class Solution:
    def __init__(self, filename: str):
        with open(filename, "r") as f:
            self.input = f.read()
            self.input_lines = self.input.splitlines()

        self.first, self.second = [], []
        for line in self.input_lines:
            a, b = line.split()
            self.first.append(int(a))
            self.second.append(int(b))

    def solve_part1(self) -> int:
        assert len(self.first) == len(self.second)
        fs, ss = sorted(self.first), sorted(self.second)
        total = sum(
            abs(fs[i] - ss[i])
            for i in range(len(self.first))
        )

        return total

    def solve_part2(self) -> int:
        assert len(self.first) == len(self.second)
        sc = Counter(self.second)
        total = 0
        for a in self.first:
            total += a * sc[a]

        return total


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
