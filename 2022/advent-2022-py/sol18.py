import argparse as ap
import re
import sys
import pyperclip
import json
from datetime import datetime
from typing import List, Dict, Set, Callable, Tuple, Union, Optional, Any
from tqdm import tqdm, trange
from collections import defaultdict


def print_grid(grid: List[List[List[str]]]):
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            for z in range(len(grid[x][y])):
                print(grid[x][y][z], end="")
            print()
        print()


class Solution:
    def __init__(self, filename: str):
        with open(filename, "r") as f:
            self.input = f.read()
            self.input_lines = self.input.splitlines()

        self.cubes = []
        for line in self.input_lines:
            cube = tuple(int(x) for x in line.split(","))
            self.cubes.append(cube)

        self.insides = defaultdict(int)
        self.max_x = max(x for x, _, _ in self.cubes)
        self.max_y = max(y for _, y, _ in self.cubes)
        self.max_z = max(z for _, _, z in self.cubes)
        self.grid = [
            [["."] * (self.max_z + 1) for _ in range(self.max_y + 1)]
            for _ in range(self.max_x + 1)
        ]

    def solve_part1(self) -> int:
        cube_set = set()
        sides = 0
        for cube in self.cubes:
            for offset in [-1, 1]:
                for i in range(3):
                    c_offset = [0, 0, 0]
                    c_offset[i] = offset
                    dx, dy, dz = c_offset
                    if (cube[0] + dx, cube[1] + dy, cube[2] + dz) not in cube_set:
                        sides += 1
                    else:
                        sides -= 1

            cube_set.add(cube)

        return sides

    def solve_part2(self) -> int:
        # Okay, we have to construct a 3D grid for this
        for x, y, z in self.cubes:
            self.grid[x][y][z] = "#"

        # Now construct a stack representing the "outside"
        outside = []
        for x in range(self.max_x + 1):
            for y in range(self.max_y + 1):
                for z in range(self.max_z + 1):
                    if (
                        (x == 0 or x == self.max_x)
                        or (y == 0 or y == self.max_y)
                        or (z == 0 or z == self.max_z)
                    ):
                        if self.grid[x][y][z] == ".":
                            outside.append((x, y, z))

        visited = set()
        while outside:
            x, y, z = outside.pop()
            if (x, y, z) in visited:
                continue

            visited.add((x, y, z))
            self.grid[x][y][z] = "o"
            for offset in [-1, 1]:
                for i in range(3):
                    c_offset = [0, 0, 0]
                    c_offset[i] = offset
                    dx, dy, dz = c_offset
                    if (
                        0 <= x + dx <= self.max_x
                        and 0 <= y + dy <= self.max_y
                        and 0 <= z + dz <= self.max_z
                    ):
                        if self.grid[x + dx][y + dy][z + dz] == ".":
                            outside.append((x + dx, y + dy, z + dz))

        # Now grab all the coords of the '.'s and use them
        # to calculate inside faces
        count = 0
        for x in range(self.max_x + 1):
            for y in range(self.max_y + 1):
                for z in range(self.max_z + 1):
                    if self.grid[x][y][z] == ".":
                        for offset in [-1, 1]:
                            for i in range(3):
                                c_offset = [0, 0, 0]
                                c_offset[i] = offset
                                dx, dy, dz = c_offset
                                if (
                                    0 <= x + dx <= self.max_x
                                    and 0 <= y + dy <= self.max_y
                                    and 0 <= z + dz <= self.max_z
                                ):
                                    if self.grid[x + dx][y + dy][z + dz] == "#":
                                        count += 1

        return self.solve_part1() - count


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
