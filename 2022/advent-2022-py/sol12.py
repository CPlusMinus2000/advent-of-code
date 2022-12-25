import argparse as ap
import re
import sys
import pyperclip
from datetime import datetime
from collections import deque


class Solution:
    def __init__(self, filename: str):
        with open(filename, "r") as f:
            self.input = f.read()
            self.input_lines = self.input.splitlines()

        self.start = (0, 0)
        self.end = (0, 0)
        for i, line in enumerate(self.input_lines):
            for j, c in enumerate(line):
                if c == "S":
                    self.start = (j, i)
                elif c == "E":
                    self.end = (j, i)

        self.input = self.input.replace("S", "a")
        self.input = self.input.replace("E", "z")
        self.input_lines = self.input.splitlines()
        self.grid = [[ord(c) - ord("a") for c in line] for line in self.input_lines]

    def solve_part1(self) -> int:
        # Do BFS on the grid, but can only move to adjacent cells
        # that are less than one unit bigger than the current cell
        # Try to reach self.end

        # BFS, return shortest path length
        visited = set()
        queue = deque([self.start])
        previous = {}
        while queue:
            x, y = queue.popleft()
            if (x, y) in visited:
                continue

            visited.add((x, y))
            if (x, y) == self.end:
                # Found it!
                # Trace back to find path length
                path = []
                while (x, y) != self.start:
                    path.append((x, y))
                    x, y = previous[(x, y)]

                path.append(self.start)
                path.reverse()
                return len(path) - 1

            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                if 0 <= x + dx < len(self.grid[0]) and 0 <= y + dy < len(self.grid):
                    if (
                        self.grid[y + dy][x + dx] - self.grid[y][x] <= 1
                        and (x + dx, y + dy) not in visited
                    ):
                        queue.append((x + dx, y + dy))
                        previous[(x + dx, y + dy)] = (x, y)

    def solve_part2(self) -> int:
        # Grab all grid indices equal to a
        a_indices = []
        for i, line in enumerate(self.grid):
            for j, c in enumerate(line):
                if c == 0:
                    a_indices.append((j, i))

        lengths = []
        for a_index in a_indices:
            self.start = a_index
            lengths.append(self.solve_part1())

        print(lengths)
        return min([l for l in lengths if l is not None])


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
    pyperclip.copy(x)
