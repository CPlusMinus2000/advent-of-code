import argparse as ap
import re
import sys
import pyperclip
from datetime import datetime
from typing import Dict, Tuple, Optional
from collections import defaultdict


def elf_nearby(x: int, y: int, grid: Dict[Tuple[int, int], str]) -> bool:
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue

            if grid[x + dx, y + dy] == "#":
                return True

    return False


def propose_north(
    x: int, y: int, grid: Dict[Tuple[int, int], str]
) -> Optional[Tuple[int, int]]:
    n = grid[x, y - 1]
    ne = grid[x + 1, y - 1]
    nw = grid[x - 1, y - 1]
    if all([n == ".", ne == ".", nw == "."]):
        return x, y - 1

    return None


def propose_south(
    x: int, y: int, grid: Dict[Tuple[int, int], str]
) -> Optional[Tuple[int, int]]:
    s = grid[x, y + 1]
    se = grid[x + 1, y + 1]
    sw = grid[x - 1, y + 1]
    if all([s == ".", se == ".", sw == "."]):
        return x, y + 1

    return None


def propose_west(
    x: int, y: int, grid: Dict[Tuple[int, int], str]
) -> Optional[Tuple[int, int]]:
    w = grid[x - 1, y]
    nw = grid[x - 1, y - 1]
    sw = grid[x - 1, y + 1]
    if all([w == ".", nw == ".", sw == "."]):
        return x - 1, y

    return None


def propose_east(
    x: int, y: int, grid: Dict[Tuple[int, int], str]
) -> Optional[Tuple[int, int]]:
    e = grid[x + 1, y]
    ne = grid[x + 1, y - 1]
    se = grid[x + 1, y + 1]
    if all([e == ".", ne == ".", se == "."]):
        return x + 1, y

    return None


def print_grid(grid: Dict[Tuple[int, int], str]):
    minx = min([x for x, y in grid.keys()])
    maxx = max([x for x, y in grid.keys()])
    miny = min([y for x, y in grid.keys()])
    maxy = max([y for x, y in grid.keys()])
    for y in range(miny, maxy + 1):
        for x in range(minx, maxx + 1):
            print(grid[x, y], end="")

        print()


class Solution:
    def __init__(self, filename: str):
        with open(filename, "r") as f:
            self.input = f.read()
            self.input_lines = self.input.splitlines()

        self.grid = defaultdict(lambda: ".")
        self.elves = []
        for y, line in enumerate(self.input_lines):
            for x, c in enumerate(line):
                self.grid[x, y] = c
                if c == "#":
                    self.elves.append((x, y))

    def solve_part1(self) -> int:
        proposal_queue = [
            propose_north, propose_south, propose_west, propose_east
        ]

        for _ in range(10):
            proposal_counts = defaultdict(int)
            actions = {}
            for i, (x, y) in enumerate(self.elves):
                if not elf_nearby(x, y, self.grid):
                    continue

                for proposal in proposal_queue:
                    p = proposal(x, y, self.grid)
                    if p is not None:
                        proposal_counts[p] += 1
                        actions[p] = i
                        break

            copy_grid = defaultdict(lambda: ".")
            actioned = set()
            for p, count in proposal_counts.items():
                if count == 1:
                    eindex = actions[p]
                    copy_grid[p] = "#"
                    self.elves[eindex] = p
                    actioned.add(eindex)

            for i, (x, y) in enumerate(self.elves):
                if i not in actioned:
                    copy_grid[x, y] = "#"

            proposal_queue = proposal_queue[1:] + proposal_queue[:1]
            self.grid = copy_grid

        minx = min([x for x, y in self.elves])
        maxx = max([x for x, y in self.elves])
        miny = min([y for x, y in self.elves])
        maxy = max([y for x, y in self.elves])
        return (maxx - minx + 1) * (maxy - miny + 1) - len(self.elves)

    def solve_part2(self) -> int:
        proposal_queue = [
            propose_north, propose_south, propose_west, propose_east
        ]

        r = 1
        while True:
            proposal_counts = defaultdict(int)
            actions = {}
            for i, (x, y) in enumerate(self.elves):
                if not elf_nearby(x, y, self.grid):
                    continue

                for proposal in proposal_queue:
                    p = proposal(x, y, self.grid)
                    if p is not None:
                        proposal_counts[p] += 1
                        actions[p] = i
                        break

            copy_grid = defaultdict(lambda: ".")
            actioned = set()
            for p, count in proposal_counts.items():
                if count == 1:
                    eindex = actions[p]
                    copy_grid[p] = "#"
                    self.elves[eindex] = p
                    actioned.add(eindex)

            if not actioned:
                return r

            for i, (x, y) in enumerate(self.elves):
                if i not in actioned:
                    copy_grid[x, y] = "#"

            proposal_queue = proposal_queue[1:] + proposal_queue[:1]
            self.grid = copy_grid
            r += 1


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
