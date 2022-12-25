import argparse as ap
import re
import sys
from datetime import datetime


def emax(l):
    return max(l) if l else -1


class Solution:
    def __init__(self, filename: str):
        with open(filename, "r") as f:
            self.input = f.read()
            self.input_lines = self.input.splitlines()

        self.trees = [[int(c) for c in line] for line in self.input_lines]

    def solve_part1(self) -> int:
        count = 0
        for y in range(len(self.trees)):
            for x in range(len(self.trees[y])):
                # Check up, down, left, right for higher trees
                lmax = emax(self.trees[y][:x])
                rmax = emax(self.trees[y][x + 1 :])
                umax = emax([row[x] for row in self.trees[:y]])
                dmax = emax([row[x] for row in self.trees[y + 1 :]])
                if (
                    self.trees[y][x] > lmax
                    or self.trees[y][x] > rmax
                    or self.trees[y][x] > umax
                    or self.trees[y][x] > dmax
                ):
                    count += 1

        return count

    def solve_part2(self) -> int:
        best = 0
        for y in range(len(self.trees)):
            for x in range(len(self.trees[y])):
                # If we're on the edge, skip
                if (
                    x == 0
                    or x == len(self.trees[y]) - 1
                    or y == 0
                    or y == len(self.trees) - 1
                ):
                    continue

                # Starting from x, y, check all directions for trees
                # that are the same height or higher
                up = left = down = right = 1
                height = self.trees[y][x]
                while up < y and self.trees[y - up][x] < height:
                    up += 1

                while left < x and self.trees[y][x - left] < height:
                    left += 1

                while (
                    down < len(self.trees) - y - 1 and self.trees[y + down][x] < height
                ):
                    down += 1

                while (
                    right < len(self.trees[y]) - x - 1
                    and self.trees[y][x + right] < height
                ):
                    right += 1

                score = up * left * down * right
                if score > best:
                    best = score

        return best


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
