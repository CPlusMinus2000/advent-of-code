import argparse as ap
import re
import sys
import pyperclip
import uuid
from datetime import datetime
from typing import List, Dict, Set, Callable, Tuple, Union, Optional, Any
from tqdm import tqdm, trange
from collections import defaultdict
from copy import deepcopy


class Point:
    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y}, {self.z})"

    def __str__(self) -> str:
        return f"{self.x},{self.y},{self.z}"

    @staticmethod
    def from_tuple(t: Tuple[int, int, int]) -> "Point":
        return Point(*t)

    @staticmethod
    def from_str(s: str) -> "Point":
        return Point(*map(int, s.split(",")))

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __le__(self, other):
        return self.x <= other.x and self.y <= other.y and self.z <= other.z

    def __ge__(self, other):
        return self.x >= other.x and self.y >= other.y and self.z >= other.z


class Brick:
    def __init__(self, p1: Point, p2: Point, iden: Optional[str] = None):
        self.p1 = p1
        self.p2 = p2
        self.iden = iden if iden is not None else uuid.uuid4().hex

    def __hash__(self):
        return hash((self.p1, self.p2))

    def __eq__(self, other):
        return self.p1 == other.p1 and self.p2 == other.p2

    def __repr__(self) -> str:
        return f"Brick({self.p1}, {self.p2}, {self.iden})"

    def __str__(self) -> str:
        return f"{self.p1}~{self.p2}"

    def is_vertical(self) -> bool:
        return self.p1.x == self.p2.x and self.p1.y == self.p2.y

    def coords(self) -> List[Point]:
        coords = []
        for x in range(self.p1.x, self.p2.x + 1):
            for y in range(self.p1.y, self.p2.y + 1):
                for z in range(self.p1.z, self.p2.z + 1):
                    coords.append(Point(x, y, z))

        return coords

    def underneath(self) -> List[Point]:
        under = []
        for x in range(self.p1.x, self.p2.x + 1):
            for y in range(self.p1.y, self.p2.y + 1):
                under.append(Point(x, y, self.p1.z - 1))

        return under

    def top_cubes(self) -> List[Point]:
        top = []
        for x in range(self.p1.x, self.p2.x + 1):
            for y in range(self.p1.y, self.p2.y + 1):
                top.append(Point(x, y, self.p2.z))

        return top

    def overlapping(self, space: List[Point]) -> bool:
        for p in space:
            if self.p1 <= p <= self.p2:
                return True

        return False


class Space:
    def __init__(self, max_x: int, max_y: int, max_z: int):
        self.max_x = max_x
        self.max_y = max_y
        self.max_z = max_z
        self.space = [[[None] * max_x for _ in range(max_y)] for _ in range(max_z)]
        self.bricks = []

    def __getitem__(self, key: Point) -> Optional[Brick]:
        return self.space[key.z][key.y][key.x]

    def __setitem__(self, key: Point, value: Optional[Brick]):
        self.space[key.z][key.y][key.x] = value

    def add_brick(self, brick: Brick) -> None:
        self.bricks.append(brick)
        for p in brick.coords():
            self[p] = brick

    def remove_brick(self, brick: Brick) -> None:
        self.bricks.remove(brick)
        for p in brick.coords():
            self[p] = None

    def can_brick_fall(self, brick: Brick) -> bool:
        for p in brick.underneath():
            if p.z <= 0 or self[p] is not None:
                return False

        return True

    def fall_brick(self, brick: Brick) -> str:
        if not self.can_brick_fall(brick):
            raise ValueError("Brick cannot fall")

        for p in brick.top_cubes():
            self[p] = None

        for p in brick.underneath():
            self[p] = brick

        brick.p1.z -= 1
        brick.p2.z -= 1
        return brick.iden

    def can_any_fall(self) -> bool:
        for brick in self.bricks:
            if self.can_brick_fall(brick):
                return True

        return False

    def fall_all(self) -> Set[str]:
        fallen = set()
        while self.can_any_fall():
            for brick in self.bricks:
                if self.can_brick_fall(brick):
                    fallen.add(self.fall_brick(brick))

        return fallen

    def which_would_fall(self) -> Set[str]:
        backup_space = deepcopy(self.space)
        backup_bricks = deepcopy(self.bricks)
        fallen = self.fall_all()
        self.space = backup_space
        self.bricks = backup_bricks
        return fallen


class Solution:
    def __init__(self, filename: str):
        with open(filename, "r") as f:
            self.input = f.read()
            self.input_lines = self.input.splitlines()

        self.bricks = []
        self.name = 1
        max_x = max_y = max_z = 0
        for line in self.input_lines:
            p1, p2 = map(Point.from_str, line.split("~"))
            self.bricks.append(Brick(p1, p2, str(self.name)))
            max_x = max(max_x, p1.x, p2.x)
            max_y = max(max_y, p1.y, p2.y)
            max_z = max(max_z, p1.z, p2.z)
            self.name += 1

        self.space = Space(max_x + 1, max_y + 1, max_z + 1)
        for brick in self.bricks:
            self.space.add_brick(brick)

    def solve_part1(self) -> int:
        self.space.fall_all()
        total = 0
        for brick in tqdm(self.bricks):
            self.space.remove_brick(brick)
            if not self.space.can_any_fall():
                total += 1

            self.space.add_brick(brick)

        return total

    def solve_part2(self) -> int:
        self.space.fall_all()
        total = 0
        copy_bricks = deepcopy(self.bricks)
        for brick in tqdm(copy_bricks):
            backup = deepcopy(self.space)
            self.space.remove_brick(brick)
            total += len(self.space.fall_all())
            self.space = backup

        return total


if __name__ == "__main__":
    parser = ap.ArgumentParser()
    parser.add_argument(
        "-e",
        "--example",
        help="Use the example file for input instead of main",
        action="store_true",
    )

    parser.add_argument(
        "-m",
        "--mike",
        help="Use Mike's input instead of mine",
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
    elif args.mike:
        filename = f"../data/day{day}m.txt"

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
