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
NEW_LIMIT = 32


class Solution:
    def __init__(self, filename: str):
        with open(filename, "r") as f:
            self.input = f.read()
            self.input_lines = self.input.splitlines()

        self.time_limit = LIMIT
        self.blueprints = {}
        for line in self.input_lines:
            nums = re.findall(r"\d+", line)
            self.blueprints[int(nums[0])] = [int(n) for n in nums[1:]]

    def max_geodes_obtainable(self, t: int, n_geode_robots: int) -> int:
        """
        Pruning heuristic. An idealized maximum of the number of geodes
        producible from a given timestep with a certain amount of robots.

        Basically, how many geodes can we open with the amount of robots
        we have, assuming we make a new one every timestep after now?
        """

        secured = (self.time_limit - 2) * n_geode_robots
        potential = (self.time_limit - t) * (self.time_limit - t + 1) // 2
        return secured + potential

    def solve_part1(self, res: bool = False) -> int:
        results = {}
        prev_iterations = 0
        iterations = 0
        for num, blueprint in self.blueprints.items():
            orcost, ccost, obcosto, obcostc, gcosto, gcostob = blueprint
            best_so_far = 0

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
                orcost: int = orcost,
                ccost: int = ccost,
                obcosto: int = obcosto,
                obcostc: int = obcostc,
                gcosto: int = gcosto,
                gcostob: int = gcostob,
            ) -> int:
                """
                Returns the maximum number of geodes openable at the given time
                with the given resources and robots.
                """

                nonlocal best_so_far, iterations
                iterations += 1
                if t == self.time_limit:
                    return geode_robots
                elif self.max_geodes_obtainable(t, geode_robots) <= best_so_far:
                    return 0

                if ore >= gcosto and obsidian >= gcostob:
                    return geode_robots + rxd(
                        t + 1,
                        ore + ore_robots - gcosto,
                        clay + clay_robots,
                        obsidian + obsidian_robots - gcostob,
                        ore_robots,
                        clay_robots,
                        obsidian_robots,
                        geode_robots + 1,
                    )

                best = rxd(
                    t + 1,
                    ore + ore_robots,
                    clay + clay_robots,
                    obsidian + obsidian_robots,
                    ore_robots,
                    clay_robots,
                    obsidian_robots,
                    geode_robots,
                )

                if ore >= orcost:
                    score = rxd(
                        t + 1,
                        ore + ore_robots - orcost,
                        clay + clay_robots,
                        obsidian + obsidian_robots,
                        ore_robots + 1,
                        clay_robots,
                        obsidian_robots,
                        geode_robots,
                    )

                    if score > best:
                        best = score

                if ore >= ccost:
                    score = rxd(
                        t + 1,
                        ore + ore_robots - ccost,
                        clay + clay_robots,
                        obsidian + obsidian_robots,
                        ore_robots,
                        clay_robots + 1,
                        obsidian_robots,
                        geode_robots,
                    )

                    if score > best:
                        best = score

                if ore >= obcosto and clay >= obcostc:
                    score = rxd(
                        t + 1,
                        ore + ore_robots - obcosto,
                        clay + clay_robots - obcostc,
                        obsidian + obsidian_robots,
                        ore_robots,
                        clay_robots,
                        obsidian_robots + 1,
                        geode_robots,
                    )

                    if score > best:
                        best = score

                if geode_robots + best > best_so_far:
                    best_so_far = geode_robots + best

                return geode_robots + best

            results[num] = rxd(1, 0, 0, 0, 1, 0, 0, 0)
            diff = iterations - prev_iterations
            prev_iterations = iterations
            print(f"Blueprint {num} done after {diff} iterations!")

        if res:
            return results

        print(results)
        return sum(num * val for num, val in results.items())

    def solve_part2(self) -> int:
        self.time_limit = NEW_LIMIT
        self.blueprints = {k: v for k, v in self.blueprints.items() if k <= 3}
        results = self.solve_part1(res=True)
        print(results)
        return functools.reduce(lambda x, y: x * y, results.values())


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

    start = datetime.now()

    sol = Solution(filename)
    x = sol.solve_part1()
    print(f"Part 1: {x}")
    if x is not None:
        pyperclip.copy(x)

    diff = datetime.now() - start
    print(f"Part 1 took {diff.total_seconds()} seconds.")
    start = datetime.now()

    sol = Solution(filename)
    x = sol.solve_part2()
    print(f"Part 2: {x}")
    if x is not None:
        pyperclip.copy(x)

    diff = datetime.now() - start
    print(f"Part 2 took {diff.total_seconds()} seconds.")
