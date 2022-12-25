import argparse as ap
import re
import sys
import pyperclip
from datetime import datetime
from sympy import symbols, solve


eval_calls = 0


class Monkey:
    def __init__(self, name, left=None, right=None, op=None):
        self.name = name
        self.left = left
        self.right = right
        self.op = op

    def __str__(self):
        left = "" if self.left is None else self.left.name + " "
        right = "" if self.right is None else " " + self.right.name
        return f"{self.name}: {left}{self.op}{right}"

    def __repr__(self):
        return self.__str__()

    def evaluate(self, part=1) -> int:
        if self.name == "humn" and part == 2:
            return "x"
        elif isinstance(self.op, int):
            return self.op

        l, r = self.left.evaluate(part), self.right.evaluate(part)
        if isinstance(l, str):
            return f"({l}) {self.op} {r}"
        elif isinstance(r, str):
            return f"{l} {self.op} ({r})"
        elif self.op == "+":
            return l + r
        elif self.op == "*":
            return l * r
        elif self.op == "-":
            return l - r
        elif self.op == "/":
            return l // r


class Solution:
    def __init__(self, filename: str):
        with open(filename, "r") as f:
            self.input = f.read()
            self.input_lines = self.input.splitlines()

        self.monkeys = {}
        for line in self.input_lines:
            name, expr = line.split(": ")
            if expr.isdigit():
                self.monkeys[name] = Monkey(name, op=int(expr))
            else:
                left, op, right = expr.split()
                self.monkeys[name] = Monkey(name, left=left, right=right, op=op)

        for monkey in self.monkeys.values():
            if monkey.op in ["+", "-", "*", "/"]:
                monkey.left = self.monkeys[monkey.left]
                monkey.right = self.monkeys[monkey.right]

    def solve_part1(self) -> int:
        return self.monkeys["root"].evaluate(part=1)

    def solve_part2(self) -> int:
        self.monkeys["root"].op = "-"
        x = symbols("x")
        expr = eval(self.monkeys["root"].evaluate(part=2))
        return int(solve(expr, x)[0])


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
