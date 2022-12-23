import argparse as ap
import re
import sys
import pyperclip
import pdb
from datetime import datetime
from typing import List, Dict, Set, Callable, Tuple, Union, Optional, Any
from tqdm import tqdm, trange
from collections import defaultdict
from copy import deepcopy


R = (1, 0)
L = (-1, 0)
D = (0, 1)
U = (0, -1)
DIRECTIONS = [R, D, L, U]
DIR_VAL = {R: 0, D: 1, L: 2, U: 3}

DIR_CHARS = {R: ">", D: "v", L: "<", U: "^"}

SIDE = 50

NEXT_FACE = {
    # (1, R): lambda x, y: (x, y, R),
    # (1, D): lambda x, y: (x, y, D),
    (1, L): lambda x, y: (0, (3 * SIDE - 1) - y, R),
    (1, U): lambda x, y: (0, x + 100, R),
    (2, R): lambda x, y: (2 * SIDE - 1, (3 * SIDE - 1) - y, L),
    (2, D): lambda x, y: (2 * SIDE - 1, x - 50, L),
    # (2, L): lambda x, y: (x, y, L),
    (2, U): lambda x, y: (x - 100, 4 * SIDE - 1, U),
    (3, R): lambda x, y: (y + 50, 49, U),
    # (3, D): lambda x, y: (x, y, D),
    (3, L): lambda x, y: (y - 50, 100, D),
    # (3, U): lambda x, y: (x, y, U),
    # (4, R): lambda x, y: (x, y, R),
    # (4, D): lambda x, y: (x, y, D),
    (4, L): lambda x, y: (50, (3 * SIDE - 1) - y, R),
    (4, U): lambda x, y: (50, x + 50, R),
    (5, R): lambda x, y: ((3 * SIDE - 1), (3 * SIDE - 1) - y, L),
    (5, D): lambda x, y: (49, x + 100, L),
    # (5, L): lambda x, y: (x, y, L),
    # (5, U): lambda x, y: (x, y, U),
    (6, R): lambda x, y: (y - 100, 3 * SIDE - 1, U),
    (6, D): lambda x, y: (x + 100, 0, D),
    (6, L): lambda x, y: (y - 100, 0, D),
    # (6, U): lambda x, y: (x, y, U)
}


def find_face(x: int, y: int) -> int:
    if x < 100 and y < 50:
        return 1
    elif x >= 100 and y < 50:
        return 2
    elif y < 100:
        return 3
    elif x < 50 and y < 150:
        return 4
    elif y < 150:
        return 5
    else:
        return 6


def next_direction(direction: int, turn: str) -> int:
    ind = DIRECTIONS.index(direction)
    if turn == "L":
        return DIRECTIONS[(ind - 1) % 4]
    elif turn == "R":
        return DIRECTIONS[(ind + 1) % 4]
    else:
        raise ValueError(f"Invalid turn: {turn}")


class Solution:
    def __init__(self, filename: str):
        with open(filename, "r") as f:
            self.input = f.read()
            self.input_lines = self.input.splitlines()

        instructions = self.input_lines[-1]
        # instructions look like 10R5L5R..., so use regex to find all
        # the numbers plus letters
        instructions = re.findall(r"\d+[LR]", instructions)
        self.instructions = []
        for instr in instructions:
            self.instructions.append((int(instr[:-1]), instr[-1]))

        self.last = int(re.findall(r"\d+", self.input_lines[-1])[-1])

        self.grid = []
        for line in self.input_lines[:-2]:
            self.grid.append(list(line))

        self.path = deepcopy(self.grid)

        self.widths = [sum(1 for r in row if r != " ") for row in self.grid]
        self.heights = []
        max_x = max(len(row) for row in self.grid)
        for i in range(max_x):
            self.heights.append(
                sum(1 for row in self.grid if i < len(row) and row[i] != " ")
            )

        x = 0
        while self.grid[0][x] == " ":
            x += 1

        self.start = (x, 0)

    def next_pos(
        self, curr: Tuple[int, int], direction: Tuple[int, int]
    ) -> Tuple[int, int]:
        x, y = curr
        dx, dy = direction
        x += dx
        y += dy
        if dx:
            if x < 0:
                return (x + self.widths[y], y)
            elif x >= len(self.grid[y]):
                return (x - self.widths[y], y)
            elif self.grid[y][x] == " ":
                return (x + self.widths[y], y)
            else:
                return (x, y)

        elif dy:
            if y < 0:
                return (x, y + self.heights[x])
            elif y >= len(self.grid):
                return (x, y - self.heights[x])
            elif dy < 0 and (x >= len(self.grid[y]) or self.grid[y][x] == " "):
                return (x, y + self.heights[x])
            elif dy > 0 and (x >= len(self.grid[y]) or self.grid[y][x] == " "):
                return (x, y - self.heights[x])
            else:
                return (x, y)

        raise ValueError(f"Invalid direction: {direction}")

    def next_pos2(
        self, curr: Tuple[int, int], direction: Tuple[int, int]
    ) -> Tuple[int, int, Tuple[int, int]]:
        x, y = curr
        dx, dy = direction
        x += dx
        y += dy
        face = find_face(*curr)
        # print(f"next_pos2: {x=}, {y=}, {face=}")
        if dx:
            if x < 0:
                return NEXT_FACE[face, direction](x, y)
            elif x >= len(self.grid[y]):
                return NEXT_FACE[face, direction](x, y)
            elif self.grid[y][x] == " ":
                return NEXT_FACE[face, direction](x, y)
            else:
                return x, y, direction

        elif dy:
            if y < 0:
                return NEXT_FACE[face, direction](x, y)
            elif y >= len(self.grid):
                return NEXT_FACE[face, direction](x, y)
            elif dy < 0 and (x >= len(self.grid[y]) or self.grid[y][x] == " "):
                return NEXT_FACE[face, direction](x, y)
            elif dy > 0 and (x >= len(self.grid[y]) or self.grid[y][x] == " "):
                return NEXT_FACE[face, direction](x, y)
            else:
                return x, y, direction

        raise ValueError(f"Invalid direction: {direction}")

    def solve_part1(self) -> int:
        curr = self.start
        direction = (1, 0)
        for dist, turn in self.instructions:
            for _ in range(dist):
                x, y = self.next_pos(curr, direction)
                if self.grid[y][x] == "#":
                    break

                curr = (x, y)

            direction = next_direction(direction, turn)

        for _ in range(self.last):
            x, y = self.next_pos(curr, direction)
            if self.grid[y][x] == "#":
                break

            curr = (x, y)

        return 1000 * (curr[1] + 1) + 4 * (curr[0] + 1) + DIR_VAL[direction]

    def solve_part2(self) -> int:
        curr = self.start
        direction = (1, 0)
        for i, (dist, turn) in enumerate(self.instructions):
            for _ in range(dist):
                x, y, d = self.next_pos2(curr, direction)
                if self.grid[y][x] == "#":
                    break

                self.path[curr[1]][curr[0]] = DIR_CHARS[direction]
                curr, direction = (x, y), d

            direction = next_direction(direction, turn)

        for _ in range(self.last):
            x, y, direction = self.next_pos2(curr, direction)
            if self.grid[y][x] == "#":
                break

            self.path[curr[1]][curr[0]] = DIR_CHARS[direction]
            curr = (x, y)

        with open("path.txt", "w") as f:
            for row in self.path:
                f.write("".join(row) + "\n")

        return 1000 * (curr[1] + 1) + 4 * (curr[0] + 1) + DIR_VAL[direction]


def test() -> Solution:
    sol = Solution("../data/day22.txt")
    return sol


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
