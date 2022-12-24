import argparse as ap
import re
import sys
import pyperclip
from datetime import datetime
from typing import List, Dict, Tuple
from collections import defaultdict, deque


R = (1, 0)
L = (-1, 0)
D = (0, 1)
U = (0, -1)
DIR_CHARS = {R: ">", D: "v", L: "<", U: "^"}
CHAR_DIRS = {v: k for k, v in DIR_CHARS.items()}


class Blizzard:
    def __init__(
        self,
        x: int,
        y: int,
        d: Tuple[int, int],
        obstacles: Dict[Tuple[int, int], int],
        overflow: Dict[Tuple[int, int], Tuple[int, int]] = None,
    ):
        self.x = x
        self.y = y
        self.d = d
        self.obstacles = obstacles
        self.overflow = overflow

    def move(self):
        dx, dy = self.d
        self.obstacles[self.x, self.y] -= 1
        self.x += dx
        self.y += dy
        if (self.x, self.y) in self.overflow:
            self.x, self.y = self.overflow[self.x, self.y]

        self.obstacles[self.x, self.y] += 1

    def unmove(self):
        dx, dy = self.d
        self.obstacles[self.x, self.y] -= 1
        self.x -= dx
        self.y -= dy
        if (self.x, self.y) in self.overflow:
            self.x, self.y = self.overflow[self.x, self.y]

        self.obstacles[self.x, self.y] += 1


class Solution:
    def __init__(self, filename: str):
        with open(filename, "r") as f:
            self.input = f.read()
            self.input_lines = self.input.splitlines()

        self.step = 0
        self.obstacles = defaultdict(int)
        self.map: List[List[str]] = []
        self.blizzards: List[Blizzard] = []
        for y, line in enumerate(self.input_lines):
            row = []
            for x, c in enumerate(line):
                row.append(c)
                if c in CHAR_DIRS:
                    d = CHAR_DIRS[c]
                    self.blizzards.append(Blizzard(x, y, d, self.obstacles))
                    self.obstacles[x, y] += 1
                elif c == "#":
                    self.obstacles[x, y] += 1

            self.map.append(row)

        # Calculate overflow values
        self.overflow = {}
        for j, row in enumerate(self.map):
            if j > 0 and j < len(self.map) - 1:
                self.overflow[0, j] = (len(row) - 2, j)
                self.overflow[len(row) - 1, j] = (1, j)

        for i in range(len(self.map[0])):
            if i > 0 and i < len(self.map[0]) - 1:
                self.overflow[i, 0] = (i, len(self.map) - 2)
                self.overflow[i, len(self.map) - 1] = (i, 1)

        for blizz in self.blizzards:
            blizz.overflow = self.overflow

        self.start = next(
            (x, 0) for x in range(len(self.map[0])) if self.map[0][x] == "."
        )

        self.obstacles[self.start[0], -1] += 1
        self.end = next(
            (x, len(self.map) - 1)
            for x in range(len(self.map[0]))
            if self.map[len(self.map) - 1][x] == "."
        )

        self.obstacles[self.end[0], len(self.map)] += 1

    def __str__(self) -> str:
        s = ""
        for row in self.map:
            for x, c in enumerate(row):
                if c == "#":
                    continue

                row[x] = "."

        for blizz in self.blizzards:
            x, y = blizz.x, blizz.y
            self.map[y][x] = DIR_CHARS[blizz.d]

        for y, row in enumerate(self.map):
            for x, c in enumerate(row):
                if self.obstacles[x, y] > 1:
                    s += str(self.obstacles[x, y])
                else:
                    s += c

            s += "\n"

        return s

    def __repr__(self) -> str:
        return str(self)

    def move_all(self) -> None:
        for blizz in self.blizzards:
            blizz.move()

    def unmove_all(self) -> None:
        for blizz in self.blizzards:
            blizz.unmove()

    def move_to_step(self, step: int) -> None:
        if step > self.step:
            for _ in range(step - self.step):
                self.move_all()
        else:
            for _ in range(self.step - step):
                self.unmove_all()

        self.step = step

    def next_steps(self, curr: Tuple[int, int]):
        self.move_all()
        options = []
        for pos in [(0, 0), R, L, U, D]:
            dx, dy = pos
            x, y = curr
            if self.obstacles[x + dx, y + dy] == 0:
                options.append(((x + dx, y + dy), self.step + 1))

        self.unmove_all()
        return options

    def solve_part1(self) -> int:
        queue = deque([(self.start, 654)])
        visited = set()
        while queue:
            curr, step = queue.popleft()
            if (curr, step) in visited:
                continue

            visited.add((curr, step))
            if curr == self.end:
                return step

            self.move_to_step(step)
            queue.extend(self.next_steps(curr))

    def solve_part2(self) -> int:
        queue = deque([(self.end, 326)])
        visited = set()
        while queue:
            curr, step = queue.popleft()
            if (curr, step) in visited:
                continue

            visited.add((curr, step))
            if curr == self.start:
                return step

            self.move_to_step(step)
            queue.extend(self.next_steps(curr))


def test():
    return Solution("../data/day24ex.txt")


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
