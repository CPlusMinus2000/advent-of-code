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

    def feed_seed_through(self, seed: int, maps: List[Dict[range, range]]) -> int:
        for map in maps:
            for source, dest in map.items():
                if seed in source:
                    seed = dest[seed - source.start]
                    break

        return seed

    def feed_ranges_through(
        self, r_list: List[range], maps: List[Dict[range, range]]
    ) -> List[range]:
        curr = r_list
        for map in maps:
            succ = []
            for source, dest in map.items():
                passover = []
                while curr:
                    r = curr.pop()
                    if r.start in source and r.stop in source:
                        succ.append(
                            range(
                                dest.start + r.start - source.start,
                                dest.start + r.stop - source.start,
                            )
                        )
                    elif r.start in source:
                        succ.append(
                            range(
                                dest.start + r.start - source.start,
                                dest.start + len(source),
                            )
                        )
                        passover.append(range(source.stop, r.stop))
                    elif r.stop in source:
                        succ.append(
                            range(dest.start, dest.start + r.stop - source.start)
                        )
                        passover.append(range(r.start, source.start))
                    elif r.start < source.start and r.stop > source.stop:
                        succ.append(range(dest.start, dest.start + len(source)))
                        passover.append(range(r.start, source.start))
                        passover.append(range(source.stop, r.stop))
                    else:
                        passover.append(r)

                curr = passover

            succ.extend(passover)
            curr = succ

        return curr

    def solve_part1(self) -> int:
        seeds = map(int, self.input_lines[0].split(":")[1].strip().split())
        maps_rough = "\n".join(self.input_lines[2:]).split("\n\n")
        maps = []
        for mapr in maps_rough:
            mapr = mapr.splitlines()
            maps.append({})
            for cor in mapr[1:]:
                dest, source, length = map(int, cor.split())
                maps[-1][range(source, source + length)] = range(dest, dest + length)

        return min([self.feed_seed_through(seed, maps) for seed in seeds])

    def solve_part2(self) -> int:
        seeds_nums = list(map(int, self.input_lines[0].split(":")[1].strip().split()))
        i = 0
        seed_ranges = []
        while i < len(seeds_nums):
            seed_ranges.append(range(seeds_nums[i], seeds_nums[i] + seeds_nums[i + 1]))
            i += 2

        maps_rough = "\n".join(self.input_lines[2:]).split("\n\n")
        maps = []
        for mapr in maps_rough:
            mapr = mapr.splitlines()
            maps.append({})
            for cor in mapr[1:]:
                dest, source, length = map(int, cor.split())
                maps[-1][range(source, source + length)] = range(dest, dest + length)

        result_ranges = self.feed_ranges_through(seed_ranges, maps)
        return min([r.start for r in result_ranges])


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
