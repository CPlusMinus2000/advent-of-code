import argparse as ap
import re
import sys
import pyperclip
from frozendict import frozendict
from datetime import datetime
from typing import List, Dict, Set, Callable, Tuple, Union, Optional, Any


WIDTH = 7
NUM_ROCKS = 15 * 5 * 10091
BIG_NUM = 10**12
HEIGHT = 4 * NUM_ROCKS
TYPES = 5


ROCKS = [
    "....",
    ["####"],
    [".#.", "###", ".#."],
    ["###", "..#", "..#"],
    ["#", "#", "#", "#"],
    ["##", "##"],
]

WIDTHS = {i: max(len(r) for r in ROCKS[i]) for i in range(1, TYPES + 1)}

HEIGHTS = {i: len(ROCKS[i]) for i in range(1, TYPES + 1)}


class Rock:
    def __init__(self, x: int, y: int, typ: int, chamber: List[List[str]]):
        self.x = x
        self.y = y
        assert typ in range(1, TYPES + 1)
        self.typ = typ
        self.shape = ROCKS[typ]
        self.chamber = chamber

    def __repr__(self) -> str:
        return f"({self.x}, {self.y}) {self.typ}"

    def push_left(self) -> None:
        if self.x == 0:
            return

        if self.typ == 1:
            if self.chamber[self.y][self.x - 1] == ".":
                self.x -= 1
        elif self.typ == 2:
            if (
                self.chamber[self.y][self.x] == "."
                and self.chamber[self.y + 1][self.x - 1] == "."
                and self.chamber[self.y + 2][self.x] == "."
            ):

                self.x -= 1
        elif self.typ == 3:
            if (
                self.chamber[self.y][self.x - 1] == "."
                and self.chamber[self.y + 1][self.x + 1] == "."
                and self.chamber[self.y + 2][self.x + 1] == "."
            ):

                self.x -= 1
        elif self.typ == 4:
            if all(
                self.chamber[self.y + dy][self.x - 1] == "." for dy in range(HEIGHTS[4])
            ):
                self.x -= 1
        elif self.typ == 5:
            if all(
                self.chamber[self.y + dy][self.x - 1] == "." for dy in range(HEIGHTS[5])
            ):
                self.x -= 1

    def push_left_smart(self) -> None:
        if self.x == 0:
            return

        for dy in range(len(self.shape)):
            for dx in range(len(self.shape[dy])):
                if self.shape[dy][dx] == "#" and (
                    dx == 0 or self.shape[dy][dx - 1] == "."
                ):
                    if self.chamber[self.y + dy][self.x + dx - 1] != ".":
                        return

        self.x -= 1

    def push_right(self) -> None:
        if self.x == WIDTH - WIDTHS[self.typ]:
            return

        if self.typ == 1:
            if self.chamber[self.y][self.x + WIDTHS[1]] == ".":
                self.x += 1
        elif self.typ == 2:
            if (
                self.chamber[self.y][self.x + 2] == "."
                and self.chamber[self.y + 1][self.x + WIDTHS[2]] == "."
                and self.chamber[self.y + 2][self.x + 2] == "."
            ):

                self.x += 1
        elif self.typ == 3:
            if all(
                self.chamber[self.y + dy][self.x + WIDTHS[3]] == "."
                for dy in range(HEIGHTS[3])
            ):
                self.x += 1
        elif self.typ == 4:
            if all(
                self.chamber[self.y + dy][self.x + WIDTHS[4]] == "."
                for dy in range(HEIGHTS[4])
            ):
                self.x += 1
        elif self.typ == 5:
            if all(
                self.chamber[self.y + dy][self.x + WIDTHS[5]] == "."
                for dy in range(HEIGHTS[5])
            ):
                self.x += 1

    def push_right_smart(self) -> None:
        if self.x == WIDTH - WIDTHS[self.typ]:
            return

        for dy in range(len(self.shape)):
            for dx in range(len(self.shape[dy])):
                if self.shape[dy][dx] == "#" and (
                    dx == WIDTHS[self.typ] - 1 or self.shape[dy][dx + 1] == "."
                ):
                    if self.chamber[self.y + dy][self.x + dx + 1] != ".":
                        return

        self.x += 1

    def fall(self) -> None:
        self.y -= 1

    def at_bottom(self) -> bool:
        if self.y == 0:
            return True

        if self.typ == 1:
            if all(
                self.chamber[self.y - 1][self.x + dx] == "." for dx in range(WIDTHS[1])
            ):
                return False
        elif self.typ == 2:
            if (
                self.chamber[self.y][self.x] == "."
                and self.chamber[self.y - 1][self.x + 1] == "."
                and self.chamber[self.y][self.x + 2] == "."
            ):

                return False
        elif self.typ == 3:
            if all(
                self.chamber[self.y - 1][self.x + dx] == "." for dx in range(WIDTHS[3])
            ):
                return False
        elif self.typ == 4:
            if self.chamber[self.y - 1][self.x] == ".":
                return False
        elif self.typ == 5:
            if all(
                self.chamber[self.y - 1][self.x + dx] == "." for dx in range(WIDTHS[5])
            ):
                return False

        return True

    def at_bottom_smart(self) -> bool:
        if self.y == 0:
            return True

        for dy in range(len(self.shape)):
            for dx in range(len(self.shape[dy])):
                if self.shape[dy][dx] == "#" and (
                    dy == 0 or self.shape[dy - 1][dx] == "."
                ):
                    if self.chamber[self.y + dy - 1][self.x + dx] != ".":
                        return True

        return False

    def lock(self) -> int:
        # lock the shape into the chamber
        for dy in range(len(self.shape)):
            for dx in range(len(self.shape[dy])):
                if self.shape[dy][dx] == "#":
                    self.chamber[self.y + dy][self.x + dx] = self.shape[dy][dx]

        return self.y + HEIGHTS[self.typ]


class Solution:
    def __init__(self, filename: str):
        with open(filename, "r") as f:
            self.input = f.read()
            self.ilen = len(self.input)

        self.chamber = [["."] * WIDTH for _ in range(HEIGHT)]
        self.max_height = 0
        self.cache = {}

    def __str__(self) -> str:
        base = "+" + "-" * WIDTH + "+"
        for i in range(self.max_height):
            base = "|" + "".join(self.chamber[i]) + "|\n" + base

        return base

    def __repr__(self) -> str:
        return self.__str__()

    def solve_part1(self) -> int:
        dir_index = 0
        for i in range(NUM_ROCKS):
            rock = Rock(2, self.max_height + 3, (i % 5) + 1, self.chamber)
            direction = self.input[dir_index % self.ilen]
            dir_index += 1
            if direction == "<":
                rock.push_left_smart()
            elif direction == ">":
                rock.push_right_smart()

            while not rock.at_bottom_smart():
                rock.fall()
                direction = self.input[dir_index % self.ilen]
                if direction == "<":
                    rock.push_left_smart()
                elif direction == ">":
                    rock.push_right_smart()

                dir_index += 1

            self.max_height = max(self.max_height, rock.lock())

        return self.max_height

    def add_to_cache(self) -> None:
        stack = [(x, self.max_height) for x in range(WIDTH)]
        topology = {}
        visited = set()
        while stack:
            x, y = stack.pop()
            if (x, y) in visited:
                continue

            visited.add((x, y))
            if self.chamber[y][x] == "#":
                continue

    def solve_part2(self) -> int:
        pass


def test() -> Solution:
    sol = Solution("../data/day17ex.txt")
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
