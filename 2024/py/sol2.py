import argparse as ap
import re
import sys
import pyperclip
from datetime import datetime
from typing import List, Dict, Set, Callable, Tuple, Union, Optional, Any
from tqdm import tqdm, trange
from collections import defaultdict


def is_safe(level: list[int]) -> bool:
    assert len(level) >= 2
    min_diff, max_diff = float("inf"), float("-inf")
    for i in range(len(level) - 1):
        diff = level[i + 1] - level[i]
        min_diff = min(min_diff, diff)
        max_diff = max(max_diff, diff)

    if -3 <= min_diff <= max_diff <= -1:
        return True
    elif 1 <= min_diff <= max_diff <= 3:
        return True
    else:
        return False


class Solution:
    def __init__(self, filename: str):
        with open(filename, "r") as f:
            self.input = f.read()
            self.input_lines = self.input.splitlines()

        self.levels = []
        for line in self.input_lines:
            level = [int(l) for l in line.split()]
            self.levels.append(level)

    def solve_part1(self) -> int:
        return len([l for l in self.levels if is_safe(l)])

    def solve_part2(self) -> int:
        safe = 0
        for level in self.levels:
            for i in range(len(level)):
                level_copy = level.copy()
                level_copy.pop(i)
                if is_safe(level_copy):
                    safe += 1
                    break

        return safe


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
