import argparse as ap
import re
import sys


COLOURS = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000
}

class Amphipod:
    def __init__(self, x: int, y: int, colour: str):
        self.x = x
        self.y = y
        assert colour in COLOURS
        self.colour = colour
    
    def __str__(self) -> str:
        return f"{self.colour}{self.x}{self.y}"
    
    def __repr__(self) -> str:
        return f"{self.colour}{self.x}{self.y}"
    
    def __hash__(self) -> int:
        return hash(str(self))


class Board:
    def __init__(self):
        pass


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
