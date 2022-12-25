import argparse as ap
import re
import sys
import pyperclip
from datetime import datetime
from typing import List, Dict, Callable
from tqdm import trange


class Monkey:
    def __init__(
        self,
        items: List[str],
        operation: Callable[[int], int],
        op_parts: List[str],
        test: Callable[[int], int],
        test_ints: List[int],
    ):
        self.items = [int(x) for x in items]
        self.operation = operation
        self.op_parts = op_parts
        self.test = test
        self.test_ints = test_ints
        self.inspections = 0

    def __repr__(self):
        return f"Monkey({self.items}, {self.op_parts}, {self.test_ints})"

    def __str__(self):
        return f"Monkey({self.items}, {self.op_parts}, {self.test_ints})"

    def inspect(self, divide: bool = True):
        for i in range(len(self.items)):
            self.items[i] = self.operation(self.items[i])
            if divide:
                self.items[i] = self.items[i] // 3

            self.inspections += 1

    def throw(self, monkeys: List["Monkey"], mod: int = 0):
        while self.items:
            item = self.items.pop(0)
            if mod:
                item = item % mod

            index = self.test(item)
            monkeys[index].items.append(item)


class Solution:
    def __init__(self, filename: str):
        with open(filename, "r") as f:
            self.input = f.read()
            self.input_monkeys = self.input.split("\n\n")

        self.monkeys = []
        for monkey in self.input_monkeys:
            lines = monkey.splitlines()
            items = lines[1].split(": ")[1].split(", ")
            op = lines[2].split(": ")[1].replace("new = ", "")
            x, y, z = op.split()
            operation = lambda x, op=op: eval(op.replace("old", str(x)))
            a, b, c = [int(li.split()[-1]) for li in lines[3:]]
            test = lambda x, a=a, b=b, c=c: b if x % a == 0 else c
            self.monkeys.append(Monkey(items, operation, [x, y, z], test, [a, b, c]))

            print(self.monkeys[0].operation(1))

    def inspections(self) -> Dict[int, int]:
        return {i: m.inspections for i, m in enumerate(self.monkeys)}

    def solve_part1(self) -> int:
        for _ in trange(20):
            for i, monkey in enumerate(self.monkeys):
                monkey.inspect()
                monkey.throw(self.monkeys)

        # Grab two most active monkeys
        m = sorted(self.monkeys, key=lambda x: x.inspections, reverse=True)
        return m[0].inspections * m[1].inspections

    def solve_part2(self, iterations: int = 10000) -> int:
        # Product of all test values
        prod = 1
        for monkey in self.monkeys:
            prod *= monkey.test_ints[0]

        print(prod)
        for i in trange(iterations):
            for monkey in self.monkeys:
                monkey.inspect(divide=False)
                monkey.throw(self.monkeys, mod=prod)

        # Grab two most active monkeys
        m = sorted(self.monkeys, key=lambda x: x.inspections, reverse=True)
        return m[0].inspections * m[1].inspections


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

    sol = Solution(filename)
    x = sol.solve_part2()
    print(f"Part 2: {x}")
    pyperclip.copy(x)
