import argparse as ap
import re
import sys
import pyperclip
from datetime import datetime
from typing import List, Dict, Set, Callable, Tuple, Union, Optional, Any
from tqdm import tqdm, trange
from collections import defaultdict, deque
from decimal import Decimal


class Solution:
    def __init__(self, filename: str):
        with open(filename, "r") as f:
            self.input = f.read()
            self.input_lines = self.input.splitlines()

        self.board = [list(s) for s in self.input_lines]
        self.h = len(self.board)
        self.w = len(self.board[0])
        self.start = None
        for y in range(self.h):
            for x in range(self.w):
                if self.board[y][x] == "S":
                    self.start = (x, y)
                    self.board[y][x] = "7"

    def solve_part1(self) -> int:
        self.dists = [[0] * self.w for _ in range(self.h)]
        queue = deque([(self.start, 0)])
        max_dist = 0
        self.visited = set()
        while queue:
            (x, y), dist = queue.popleft()
            if (x, y) in self.visited:
                continue

            self.visited.add((x, y))
            max_dist = max(max_dist, dist)
            self.dists[y][x] = dist
            pipe = self.board[y][x]
            match pipe:
                case "7":
                    queue.append(((x - 1, y), dist + 1))
                    queue.append(((x, y + 1), dist + 1))
                case "F":
                    queue.append(((x + 1, y), dist + 1))
                    queue.append(((x, y + 1), dist + 1))
                case "J":
                    queue.append(((x - 1, y), dist + 1))
                    queue.append(((x, y - 1), dist + 1))
                case "L":
                    queue.append(((x + 1, y), dist + 1))
                    queue.append(((x, y - 1), dist + 1))
                case "-":
                    queue.append(((x - 1, y), dist + 1))
                    queue.append(((x + 1, y), dist + 1))
                case "|":
                    queue.append(((x, y - 1), dist + 1))
                    queue.append(((x, y + 1), dist + 1))
                case _:
                    print(f"Unknown pipe: {pipe}")

        return max_dist

    def solve_part2(self) -> int:
        """
        Hey sweet, self.visited is important now.
        """

        enclosed = 0
        for y in range(self.h):
            for x in range(self.w):
                if (x, y) in self.visited:
                    continue

                hcross, vcross = 0, 0
                for i in range(x):
                    if (i, y) not in self.visited:
                        continue

                    if self.board[y][i] == "|":
                        hcross += 1
                    elif self.board[y][i] in ["7", "L"]:
                        hcross += Decimal("0.5")
                    elif self.board[y][i] in ["F", "J"]:
                        hcross -= Decimal("0.5")

                for j in range(y):
                    if (x, y) == (10, 4):
                        print((x, j), (x, j) in self.visited, self.board[j][x])

                    if (x, j) not in self.visited:
                        continue

                    if self.board[j][x] == "-":
                        vcross += 1
                    elif self.board[j][x] in ["7", "L"]:
                        vcross += Decimal("0.5")
                    elif self.board[j][x] in ["J", "F"]:
                        vcross -= Decimal("0.5")

                hcross = int(hcross)
                vcross = int(vcross)
                if hcross % 2 == 1 and vcross % 2 == 1:
                    enclosed += 1

        return enclosed


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

    # sol = Solution(filename)
    x = sol.solve_part2()
    print(f"Part 2: {x}")
    if x is not None:
        pyperclip.copy(x)
