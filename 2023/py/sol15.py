import argparse as ap
import re
import sys
import pyperclip
from datetime import datetime
from typing import List, Dict, Set, Callable, Tuple, Union, Optional, Any
from tqdm import tqdm, trange
from collections import defaultdict


class Solution:
    def __init__(self, filename: str):
        with open(filename, "r") as f:
            self.input = f.read()
            self.input_lines = self.input.splitlines()

        self.steps = self.input.split(",")

    def step_hash(self, step: str) -> int:
        h = 0
        for c in step:
            h = ((h + ord(c)) * 17) % 256

        return h

    def solve_part1(self) -> int:
        sum = 0
        for step in self.steps:
            sum += self.step_hash(step)

        return sum

    def solve_part2(self) -> int:
        boxes: Dict[int, List[Tuple[str, int]]] = defaultdict(list)

        for step in self.steps:
            i = re.search(r"[-=]", step).start()
            label = step[:i]
            h = self.step_hash(label)

            ind = next((j for j, x in enumerate(boxes[h]) if x[0] == label), None)
            if step[i] == "-" and ind is not None:
                boxes[h].pop(ind)
            elif step[i] == "=":
                focal = int(step[i + 1 :])
                if ind is not None:
                    boxes[h][ind] = (label, focal)
                else:
                    boxes[h].append((label, focal))

        res = 0
        for h in boxes:
            for s, lens in enumerate(boxes[h]):
                res += (h + 1) * (s + 1) * lens[1]

        return res


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
