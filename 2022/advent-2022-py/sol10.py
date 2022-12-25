import argparse as ap
import re
import sys
import pyperclip
from datetime import datetime


class Solution:
    def __init__(self, filename: str):
        with open(filename, "r") as f:
            self.input = f.read()
            self.input_lines = self.input.splitlines()

    def calculate_signal_strength(self, register, cycle):
        if cycle % 40 == 20:
            return register * cycle
        else:
            return 0

    def solve_part1(self) -> int:
        instr = 0
        cycle = 1
        X = 1
        total = 0
        while instr < len(self.input_lines):
            print(cycle, X)
            if self.input_lines[instr] == "noop":
                cycle += 1
                total += self.calculate_signal_strength(X, cycle)
            elif self.input_lines[instr].startswith("addx"):
                cycle += 1
                total += self.calculate_signal_strength(X, cycle)
                val = int(self.input_lines[instr].split()[1])
                X += val
                cycle += 1
                total += self.calculate_signal_strength(X, cycle)

            instr += 1

        return total

    def pixel(self, register, cycle):
        cycle -= 1
        c = "#" if abs((cycle % 40) - register) <= 1 else " "
        if cycle % 40 == 39:
            c += "\n"

        return c

    def solve_part2(self) -> int:
        instr = 0
        cycle = 1
        X = 1
        total = self.pixel(X, cycle)
        while instr < len(self.input_lines):
            if self.input_lines[instr] == "noop":
                cycle += 1
                total += self.pixel(X, cycle)
            elif self.input_lines[instr].startswith("addx"):
                cycle += 1
                total += self.pixel(X, cycle)
                val = int(self.input_lines[instr].split()[1])
                X += val
                cycle += 1
                total += self.pixel(X, cycle)

            instr += 1

        return total


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
    pyperclip.copy(x)

    x = sol.solve_part2()
    print(f"Part 2: \n{x}")
    # pyperclip.copy(x)
