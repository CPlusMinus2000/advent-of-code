
import argparse as ap
import re
import sys
import pyperclip
import functools
from datetime import datetime
from typing import List, Dict, Set, Callable, Tuple, Union, Optional, Any
from tqdm import tqdm, trange
from collections import defaultdict


LIMIT = 24


class Solution:
    def __init__(self, filename: str):
        with open(filename, "r") as f:
            self.input = f.read()
            self.input_lines = self.input.splitlines()
        
        self.blueprints = {}
        for line in self.input_lines:
            nums = re.findall(r"\d+", line)
            self.blueprints[int(nums[0])] = [int(n) for n in nums[1:]]

    def solve_part1(self) -> int:
        results = {}
        for num, blueprint in self.blueprints.items():
            orcost, ccost, obcosto, obcostc, gcosto, gcostob = blueprint
            @functools.lru_cache(maxsize=None)
            def rxd(
                t: int,
                ore: int,
                clay: int,
                obsidian: int,
                ore_robots: int,
                clay_robots: int,
                obsidian_robots: int,
                geode_robots: int,
                orcost: int=orcost,
                ccost: int=ccost,
                obcosto: int=obcosto,
                obcostc: int=obcostc,
                gcosto: int=gcosto,
                gcostob: int=gcostob,
            ) -> int:
                """
                Returns the maximum number of geodes openable at the given time
                with the given resources and robots.
                """

                if t == LIMIT:
                    return geode_robots

                options = [
                    (
                        t + 1,
                        ore + ore_robots,
                        clay + clay_robots,
                        obsidian + obsidian_robots,
                        ore_robots,
                        clay_robots,
                        obsidian_robots,
                        geode_robots
                    )
                ]

                if ore >= orcost:
                    options.append((
                        t + 1,
                        ore + ore_robots - orcost,
                        clay + clay_robots,
                        obsidian + obsidian_robots,
                        ore_robots + 1,
                        clay_robots,
                        obsidian_robots,
                        geode_robots,
                    ))
                
                if ore >= ccost:
                    options.append((
                        t + 1,
                        ore + ore_robots - ccost,
                        clay + clay_robots,
                        obsidian + obsidian_robots,
                        ore_robots,
                        clay_robots + 1,
                        obsidian_robots,
                        geode_robots,
                    ))
                
                if ore >= obcosto and clay >= obcostc:
                    options.append((
                        t + 1,
                        ore + ore_robots - obcosto,
                        clay + clay_robots - obcostc,
                        obsidian + obsidian_robots,
                        ore_robots,
                        clay_robots,
                        obsidian_robots + 1,
                        geode_robots,
                    ))
                
                if ore >= gcosto and obsidian >= gcostob:
                    options = [(
                        t + 1,
                        ore + ore_robots - gcosto,
                        clay + clay_robots,
                        obsidian + obsidian_robots - gcostob,
                        ore_robots,
                        clay_robots,
                        obsidian_robots,
                        geode_robots + 1,
                    )]
                
                return geode_robots + max([rxd(*o) for o in options])
            
            results[num] = rxd(1, 0, 0, 0, 1, 0, 0, 0)

        print(results)
        return sum(num * val for num, val in results.items())


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
