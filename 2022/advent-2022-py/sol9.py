
import argparse as ap
import re
import sys
from datetime import datetime
from collections import defaultdict


def sgn(x):
    return -1 if x < 0 else 1

class Solution:
    def __init__(self, filename: str):
        with open(filename, "r") as f:
            self.input = f.read()
            self.input_lines = self.input.splitlines()

        self.steps = [
            (l.split()[0], int(l.split()[1]))
            for l in self.input_lines
        ]

    def solve_part1(self) -> int:
        positions = {(0, 0): True}
        hx, hy = 0, 0
        tx, ty = 0, 0
        for direction, n in self.steps:
            for _ in range(n):
                prev = (hx, hy)
                if direction == "R":
                    hx += 1
                elif direction == "L":
                    hx -= 1
                elif direction == "U":
                    hy -= 1
                elif direction == "D":
                    hy += 1

                # Catch the tail up to the head
                if (abs(hx - tx) >= 2 and abs(hy - ty) >= 1) or \
                     (abs(hx - tx) >= 1 and abs(hy - ty) >= 2):

                    tx, ty = prev
                if abs(hx - tx) >= 2:
                    tx += sgn(hx - tx)
                elif abs(hy - ty) >= 2:
                    ty += sgn(hy - ty)

                positions[tx, ty] = True

        # Number of True values in the dict
        return sum(positions.values())

    def solve_part2(self) -> int:
        positions = {(0, 0): True}
        knots = [[0, 0] for _ in range(10)]
        temp = None
        for direction, n in self.steps:
            for _ in range(n):
                if direction == "R":
                    knots[0][0] += 1
                elif direction == "L":
                    knots[0][0] -= 1
                elif direction == "U":
                    knots[0][1] -= 1
                elif direction == "D":
                    knots[0][1] += 1

                # Catch the tails up
                for i in range(1, len(knots)):
                    if (abs(knots[i-1][0] - knots[i][0]) >= 2 and abs(knots[i-1][1] - knots[i][1]) >= 1) or \
                         (abs(knots[i-1][0] - knots[i][0]) >= 1 and abs(knots[i-1][1] - knots[i][1]) >= 2):

                        knots[i][0] += sgn(knots[i-1][0] - knots[i][0])
                        knots[i][1] += sgn(knots[i-1][1] - knots[i][1])
                    elif abs(knots[i-1][0] - knots[i][0]) >= 2:
                        knots[i][0] += sgn(knots[i-1][0] - knots[i][0])
                    elif abs(knots[i-1][1] - knots[i][1]) >= 2:
                        knots[i][1] += sgn(knots[i-1][1] - knots[i][1])

                x, y = knots[-1]
                positions[x, y] = True

        # Number of True values in the dict
        print(positions)
        return sum(positions.values())


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
    print(f"Part 1: {sol.solve_part1()}")
    print(f"Part 2: {sol.solve_part2()}")
