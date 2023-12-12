import argparse as ap
import re
import sys
import pyperclip
import itertools as it
from datetime import datetime
from typing import List, Dict, Set, Callable, Tuple, Union, Optional, Any
from tqdm import tqdm, trange
from collections import defaultdict
from functools import lru_cache


@lru_cache(maxsize=None)
def backtrack(springs: str, records) -> int:
    if not springs and not records:
        return 1
    elif not springs and records:
        return 0
    elif springs and not records:
        if "#" in springs:
            return 0
        else:
            return 1
    elif sum(records) + len(records) - 1 > len(springs):
        return 0
    else:
        if records[0] > len(springs):
            return 0
        elif records[0] == len(springs):
            if all(s in "#?" for s in springs):
                return 1
            else:
                return 0

        if springs[0] == "#":
            # Check if this is possible
            if (
                all(s in "#?" for s in springs[: records[0]])
                and springs[records[0]] != "#"
            ):
                return backtrack(springs[records[0] + 1 :], records[1:])
            else:
                return 0

        elif springs[0] == ".":
            i = 1
            while i < len(springs) and springs[i] == ".":
                i += 1

            return backtrack(springs[i:], records)

        else:
            # Question mark. Try both possibilities.
            ret = backtrack(springs[1:], records)
            if (
                all(s in "#?" for s in springs[: records[0]])
                and springs[records[0]] != "#"
            ):
                return ret + backtrack(springs[records[0] + 1 :], records[1:])
            else:
                return ret


class Solution:
    def __init__(self, filename: str):
        with open(filename, "r") as f:
            self.input = f.read()
            self.input_lines = self.input.splitlines()

        self.arrs = []

    def solve_part1(self) -> int:
        arrangements = 0
        for line in tqdm(self.input_lines):
            springs, record = line.split()
            springs = list(springs)
            records = [int(r) for r in record.split(",")]

            unknown = springs.count("?")
            curr = 0
            for combo in it.product(".#", repeat=unknown):
                sc = springs.copy()
                for i, c in enumerate(combo):
                    sc[sc.index("?")] = c

                rejoined = "".join(sc).replace(".", " ")
                groups = rejoined.split()
                if len(groups) != len(records):
                    continue

                for j, group in enumerate(groups):
                    if j >= len(records) or len(group) != records[j]:
                        break
                else:
                    curr += 1

            self.arrs.append(curr)
            arrangements += curr

        return arrangements

    def solve_part2(self) -> int:
        """
        This is going to be far too slow.
        Let's try backtracking search instead.
        """

        # okay let's do some unit testing
        assert backtrack("?", (1,)) == 1
        assert backtrack("?", (2,)) == 0
        assert backtrack("??", (1,)) == 2
        assert backtrack("??", (2,)) == 1
        assert backtrack("???.###", (1, 1, 3)) == 1
        assert backtrack("??.###", (1, 3)) == 2
        assert backtrack("#?#?#?#?#?", (3, 6)) == 1
        assert backtrack("????.#...#...", (4, 1, 1)) == 1
        assert backtrack("????.######..#####.", (1, 6, 5)) == 4
        assert backtrack("?????", (2, 1)) == 3
        assert backtrack("???.???", (2, 1)) == 6

        arrangements = 0
        for line in tqdm(self.input_lines):
            springs, record = line.split()
            springs = "?".join([springs] * 5)
            records = [int(r) for r in record.split(",")]
            records = tuple(records * 5)

            curr = backtrack(springs, tuple(records))
            self.arrs.append(curr)
            arrangements += curr

        return arrangements


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

    sol1 = Solution(filename)
    x = sol1.solve_part1()
    print(f"Part 1: {x}")
    if x is not None:
        pyperclip.copy(x)

    sol2 = Solution(filename)
    x = sol2.solve_part2()
    print(f"Part 2: {x}")
    if x is not None:
        pyperclip.copy(x)
