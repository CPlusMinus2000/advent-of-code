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
        times = [int(x) for x in self.input_lines[0].split()[1:]]
        records = [int(x) for x in self.input_lines[1].split()[1:]]
        total = 1
        for i in range(len(times)):
            ways = 0
            for j in range(times[i] + 1):
                dist = j * (times[i] - j)
                if dist > records[i]:
                    ways += 1

            total *= ways

        return total

    def solve_part2(self) -> int:
        time = int("".join(self.input_lines[0].split()[1:]))
        record = int("".join(self.input_lines[1].split()[1:]))
        lo, hi = 0, 0
        for j in range(time + 1):
            dist = j * (time - j)
            if dist > record:
                lo = j
                break

        for j in range(time, -1, -1):
            dist = j * (time - j)
            if dist > record:
                hi = j
                break

        return hi - lo + 1


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
