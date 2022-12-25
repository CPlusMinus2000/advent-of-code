import argparse as ap
import re
import sys
import pyperclip
from datetime import datetime
from tqdm import tqdm, trange
from collections import defaultdict


class Solution:
    def __init__(self, filename: str):
        with open(filename, "r") as f:
            self.input = f.read()
            self.input_lines = self.input.splitlines()

        # For each line, read out the x= and y= values for the sensors
        # and the beacons. Then, for each sensor, find the Manhattan
        # distance to its nearest beacon.
        self.sensors = []
        self.beacons = []
        self.dists = []
        for line in self.input_lines:
            sx, sy, bx, by = re.findall(r"-?\d+", line)
            self.sensors.append((int(sx), int(sy)))
            self.beacons.append((int(bx), int(by)))
            dist = abs(int(sx) - int(bx)) + abs(int(sy) - int(by))
            self.dists.append(dist)

        self.grid = {}
        for sx, sy in self.sensors:
            self.grid[(sx, sy)] = "S"

        for bx, by in self.beacons:
            self.grid[(bx, by)] = "B"

    def solve_part1(self) -> int:
        LINE = 2000000
        ranges = []
        for i in range(len(self.sensors)):
            sx, sy = self.sensors[i]
            bx, by = self.beacons[i]
            dist = abs(sx - bx) + abs(sy - by)

            # How much of the line y = 2000000 is covered by this sensor?
            # We can find the x values of the endpoints of the line
            if abs(sy - LINE) > dist:
                # The line is completely outside the sensor's range
                continue
            else:
                xn = sx - (dist - abs(sy - LINE))
                xp = sx + (dist - abs(sy - LINE))
                ranges.append((xn, xp))

        covered = set()
        for r in ranges:
            for x in range(r[0], r[1] + 1):
                covered.add(x)

        for bx, by in self.beacons:
            if by == LINE and bx in covered:
                covered.remove(bx)

        return len(covered)

    def solve_part2(self) -> int:
        edges = {}
        grid = defaultdict(int)
        candidates = set()
        BOX = 4000000
        THRESHOLD = 3
        for i in trange(len(self.sensors)):
            sx, sy = self.sensors[i]
            bx, by = self.beacons[i]
            dist = abs(sx - bx) + abs(sy - by)
            edges[sx, sy] = set()
            # Add all positions exactly dist + 1 away from the sensor
            x, y = sx - dist - 1, sy
            loops = [
                (lambda x, y, sx, sy: x != sx, 1, 1),
                (lambda x, y, sx, sy: y != sy, 1, -1),
                (lambda x, y, sx, sy: x != sx, -1, -1),
                (lambda x, y, sx, sy: y != sy, -1, 1),
            ]

            for loop in loops:
                while loop[0](x, y, sx, sy):
                    if 0 <= x <= BOX and 0 <= y <= BOX:
                        edges[sx, sy].add((x, y))
                        grid[x, y] += 1
                        if grid[x, y] >= THRESHOLD:
                            candidates.add((x, y))

                    x += loop[1]
                    y += loop[2]

        for cx, cy in tqdm(candidates):
            for l, (sx, sy) in enumerate(self.sensors):
                if abs(cx - sx) + abs(cy - sy) <= self.dists[l]:
                    break
            else:
                print(cx, cy)
                return cx * 4000000 + cy


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
