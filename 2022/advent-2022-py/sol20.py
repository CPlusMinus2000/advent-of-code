
import argparse as ap
import re
import sys
import pyperclip
from datetime import datetime
from typing import List, Dict, Set, Callable, Tuple, Union, Optional, Any
from tqdm import tqdm, trange
from collections import defaultdict, deque


DKEY = 811589153


class Solution:
    def __init__(self, filename: str):
        with open(filename, "r") as f:
            self.input = f.read()
            self.input_lines = self.input.splitlines()
        
        self.encrypted = [int(x) for x in self.input_lines]

    def solve_part1(self) -> int:
        l = len(self.encrypted)
        indices = [False] * l
        iindex = 0
        for i in range(l):
            # Swap out pieces of self.encrypted and indices
            # and use indices to determine where everything is
            # in self.encrypted
            while indices[iindex]:
                iindex += 1

            val = self.encrypted.pop(iindex)
            self.encrypted.insert((iindex + val) % (l - 1), val)
            indices.pop(iindex)
            indices.insert((iindex + val) % (l - 1), True)

        print(self.encrypted)

        zindex = self.encrypted.index(0)
        return sum(
            self.encrypted[(i + zindex) % l]
            for i in [1000, 2000, 3000]
        )
            

    def solve_part2(self) -> int:
        for i in range(len(self.encrypted)):
            self.encrypted[i] *= DKEY

        l = len(self.encrypted)
        indices = [-1] * l
        iindex = 0
        for i in range(l):
            # Swap out pieces of self.encrypted and indices
            # and use indices to determine where everything is
            # in self.encrypted
            while indices[iindex] != -1:
                iindex += 1

            val = self.encrypted.pop(iindex)
            self.encrypted.insert((iindex + val) % (l - 1), val)
            indices.pop(iindex)
            indices.insert((iindex + val) % (l - 1), i)

        zindex = self.encrypted.index(0)
        return sum(
            self.encrypted[(i + zindex) % l]
            for i in [1000, 2000, 3000]
        )


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
