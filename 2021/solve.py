import argparse as ap
import re
import sys


class Solution:
    def __init__(self, filename: str):
        with open(filename, "r") as f:
            self.input = f.read()

    def solve_part1(self) -> int:
        pass

    def solve_part2(self) -> int:
        pass


if __name__ == "__main__":
    parser = ap.ArgumentParser()
    parser.add_argument(
        "-e",
        "--example",
        help="Use the example file for input instead of main",
        action="store_true",
    )

    args = parser.parse_args()
    day = re.search(r"\d+", sys.argv[0]).group(0)
    filename = f"inputs/d{day}.txt"
    if args.example:
        filename = f"inputs/d{day}ex.txt"

    sol = Solution(filename)
    print(f"Part 1: {sol.solve_part1()}")
    # print(f"Part 2: {sol.solve_part2()}")
