import argparse as ap
import re
import sys
import pyperclip
from datetime import datetime
from typing import List, Dict, Set, Callable, Tuple, Union, Optional, Any
from tqdm import tqdm, trange
from collections import defaultdict


def value_of_reflection(g: List[str], curr_val: Optional[int] = None) -> int:
    total = 0
    for v in range(1, len(g[0])):
        for c in range(min(v, len(g[0]) - v)):
            if any(g[r][v - c - 1] != g[r][v + c] for r in range(len(g))):
                break
        else:
            if curr_val is None or v != curr_val:
                total += v
                break

    else:
        for h in range(1, len(g)):
            for c in range(min(h, len(g) - h)):
                if g[h - c - 1] != g[h + c]:
                    break
            else:
                if curr_val is None or h * 100 != curr_val:
                    total += h * 100
                    break

    return total


class Solution:
    def __init__(self, filename: str):
        with open(filename, "r") as f:
            self.input = f.read()
            self.input_lines = self.input.splitlines()

        self.groups = [x.splitlines() for x in self.input.split("\n\n")]

    def solve_part1(self) -> int:
        total = 0
        for g in self.groups:
            total += value_of_reflection(g)

        return total

    def solve_part2(self) -> int:
        def other_char(c: str) -> str:
            return "." if c == "#" else "#"

        total = 0
        for g in self.groups:
            # Change exactly one character
            breakout = False
            curr_val = value_of_reflection(g)
            for r in range(len(g)):
                for c in range(len(g[0])):
                    g[r] = g[r][:c] + other_char(g[r][c]) + g[r][c + 1 :]
                    value = value_of_reflection(g, curr_val)
                    if value != 0 and value != curr_val:
                        total += value
                        breakout = True
                        break

                    g[r] = g[r][:c] + other_char(g[r][c]) + g[r][c + 1 :]

                if breakout:
                    break

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
