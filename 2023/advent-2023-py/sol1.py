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
            digits = [c for c in line if c.isdigit()]
            total += int(digits[0]) * 10 + int(digits[-1])
        
        return total

    def digits_parser(self, line: str) -> int:
        words = {
            "one": 1,
            "two": 2,
            "three": 3,
            "four": 4,
            "five": 5,
            "six": 6,
            "seven": 7,
            "eight": 8,
            "nine": 9
        }

        start, end = 0, 0
        while True:
            if line[0].isdigit():
                start = int(line[0])
                break
            elif any(line.startswith(w) for w in words):
                start = next(words[w] for w in words if line.startswith(w))
                break

            line = line[1:]
        
        while True:
            if line[-1].isdigit():
                end = int(line[-1])
                break
            elif any(line.endswith(w) for w in words):
                end = next(words[w] for w in words if line.endswith(w))
                break

            line = line[:-1]
        
        return start * 10 + end
            

    def solve_part2(self) -> int:
        total = 0
        for line in self.input_lines:
            total += self.digits_parser(line)
        
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
