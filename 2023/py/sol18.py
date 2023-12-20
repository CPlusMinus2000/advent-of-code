import argparse as ap
import re
import sys
import pyperclip
from datetime import datetime
from typing import List, Dict, Set, Callable, Tuple, Union, Optional, Any
from tqdm import tqdm, trange
from collections import defaultdict, namedtuple
from bisect import insort


DIR_MAP = {"L": (-1, 0), "R": (1, 0), "U": (0, -1), "D": (0, 1)}
DIR_ORDER = ["R", "D", "L", "U"]


Trench = namedtuple("Trench", ["start", "end", "y_level"])


def print_grid(grid: Set[Tuple[int, int]]) -> None:
    min_x = min(x for x, _ in grid)
    max_x = max(x for x, _ in grid)
    min_y = min(y for _, y in grid)
    max_y = max(y for _, y in grid)

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if (x, y) in grid:
                print("#", end="")
            else:
                print(".", end="")
        print()


def dfs(grid: Set[Tuple[int, int]], stack: List[Tuple[int, int]]) -> None:
    while stack:
        x, y = stack.pop()
        if (x, y) in grid:
            continue

        grid.add((x, y))
        for dx, dy in DIR_MAP.values():
            stack.append((x + dx, y + dy))


class Solution:
    def __init__(self, filename: str):
        with open(filename, "r") as f:
            self.input = f.read()
            self.input_lines = self.input.splitlines()

        self.parsed = []
        for line in self.input_lines:
            d, step, hexcode = line.split()
            step = int(step)
            hexcode = hexcode[2:-1]
            self.parsed.append((d, step, hexcode))

    def solve_part1(self) -> int:
        grid = set()
        leftmost, topmost, rightmost, bottommost = {}, {}, {}, {}
        x, y = 0, 0
        for d, step, _ in self.parsed:
            dx, dy = DIR_MAP[d]
            for _ in range(step):
                x += dx
                y += dy
                grid.add((x, y))
                leftmost[y] = min(leftmost.get(y, x), x)
                rightmost[y] = max(rightmost.get(y, x), x)
                topmost[x] = max(topmost.get(x, y), y)
                bottommost[x] = min(bottommost.get(x, y), y)

        # Collect interior points
        stack = []
        for x in range(min(topmost), max(topmost) + 1):
            y = topmost[x] - 1
            while (x, y) not in grid:
                stack.append((x, y))
                y -= 1

        for x in range(min(bottommost), max(bottommost) + 1):
            y = bottommost[x] + 1
            while (x, y) not in grid:
                stack.append((x, y))
                y += 1

        for y in range(min(leftmost), max(leftmost) + 1):
            x = leftmost[y] + 1
            while (x, y) not in grid:
                stack.append((x, y))
                x += 1

        for y in range(min(rightmost), max(rightmost) + 1):
            x = rightmost[y] - 1
            while (x, y) not in grid:
                stack.append((x, y))
                x -= 1

        dfs(grid, stack)
        print_grid(grid)
        return len(grid)

    def solve_part2(self) -> int:
        area, boundary, x, y = 0, 0, 0, 0
        rtrenches: List[Trench] = []
        ltrenches: List[Trench] = []
        for _, _, hexcode in self.parsed:
            length, d = int(hexcode[:-1], 16), DIR_ORDER[int(hexcode[-1])]
            if d == "D":
                y += length
            elif d == "U":
                y -= length
            elif d == "R":
                t = Trench(x, x + length, y)
                rtrenches.append(t)
                x += length
            elif d == "L":
                t = Trench(x - length, x, y)
                ltrenches.append(t)
                x -= length
            
            boundary += length
        
        # Find trenches with the same endpoints
        rtrenches.sort(key=lambda t: -t.start)
        while rtrenches:
            rt = rtrenches.pop()
            try:
                ltind = next(
                    i for i, lt in enumerate(ltrenches)
                    if lt.start == rt.start
                )
            except StopIteration:
                ltrenches.sort()
                print(rt)
                print(rtrenches)
                print(ltrenches)
                raise

            lt = ltrenches.pop(ltind)
            endpoint = min(rt.end, lt.end)
            area += (lt.y_level - rt.y_level) * (endpoint - rt.start)
            if rt.end > endpoint:
                insort(rtrenches, Trench(endpoint, rt.end, rt.y_level), key=lambda t: -t.start)
            elif lt.end > endpoint:
                ltrenches.append(Trench(endpoint, lt.end, lt.y_level))

        return area + (boundary // 2) + 1


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
