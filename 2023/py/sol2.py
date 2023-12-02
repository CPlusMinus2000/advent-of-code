import argparse as ap
import re
import sys
import pyperclip
from datetime import datetime
from typing import List, Dict, Set, Callable, Tuple, Union, Optional, Any
from tqdm import tqdm, trange
from collections import defaultdict


RGB = {"R": 12, "G": 13, "B": 14}


def get_ints_from_game(line: str) -> Dict[str, int]:
    base = {"R": 0, "G": 0, "B": 0}
    for res in line.split(", "):
        if res.endswith("red"):
            base["R"] = int(res.split(" ")[0])
        elif res.endswith("green"):
            base["G"] = int(res.split(" ")[0])
        elif res.endswith("blue"):
            base["B"] = int(res.split(" ")[0])

    return base


class Solution:
    def __init__(self, filename: str):
        with open(filename, "r") as f:
            self.input = f.read()
            self.input_lines = self.input.splitlines()

    def solve_part1(self) -> int:
        total = 0
        for line in self.input_lines:
            gnum = int(line.split(":")[0].split(" ")[-1])
            games = line.split(":")[1].split("; ")
            for game in games:
                rgb = get_ints_from_game(game.strip())
                if not all([rgb[k] <= RGB[k] for k in RGB]):
                    break
            else:
                total += gnum

        return total

    def solve_part2(self) -> int:
        total = 0
        for line in self.input_lines:
            gnum = int(line.split(":")[0].split(" ")[-1])
            games = line.split(":")[1].split("; ")
            min_rgb = {"R": 0, "G": 0, "B": 0}
            for game in games:
                rgb = get_ints_from_game(game.strip())
                min_rgb["R"] = max(min_rgb["R"], rgb["R"])
                min_rgb["G"] = max(min_rgb["G"], rgb["G"])
                min_rgb["B"] = max(min_rgb["B"], rgb["B"])

            total += min_rgb["R"] * min_rgb["G"] * min_rgb["B"]

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
    if x is not None:
        pyperclip.copy(x)

    sol = Solution(filename)
    x = sol.solve_part2()
    print(f"Part 2: {x}")
    if x is not None:
        pyperclip.copy(x)
