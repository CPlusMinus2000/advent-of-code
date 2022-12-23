import argparse as ap
import re
import sys
import time

from typing import Optional, List
from collections import defaultdict

ON = 1
OFF = 0
END = 420

class Prism:
    def __init__(self, xi, xf, yi, yf, zi, zf, state=1):
        self.xr = [xi, xf]
        self.yr = [yi, yf]
        self.zr = [zi, zf]
        self.state = state
    
    def __str__(self):
        return f"Prism: {self.xr}, {self.yr}, {self.zr}, {self.state}"
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        return self.xr == other.xr and self.yr == other.yr and self.zr == other.zr
    
    def __hash__(self):
        return hash(self.__str__())
    
    def intersection(self, other: "Prism") -> Optional["Prism"]:
        if self.xr[0] > other.xr[1] or self.xr[1] < other.xr[0]:
            return None
        if self.yr[0] > other.yr[1] or self.yr[1] < other.yr[0]:
            return None
        if self.zr[0] > other.zr[1] or self.zr[1] < other.zr[0]:
            return None

        return Prism(
            max(self.xr[0], other.xr[0]),
            min(self.xr[1], other.xr[1]),
            max(self.yr[0], other.yr[0]),
            min(self.yr[1], other.yr[1]),
            max(self.zr[0], other.zr[0]),
            min(self.zr[1], other.zr[1]),
            -self.state
        )
    
    def volume(self) -> int:
        dx = self.xr[1] - self.xr[0] + 1
        dy = self.yr[1] - self.yr[0] + 1
        dz = self.zr[1] - self.zr[0] + 1
        return dx * dy * dz * self.state

class Volume:
    def __init__(self, prisms: List[Prism]):
        self.prisms = prisms
    
    def __len__(self) -> int:
        return len(self.prisms)
    
    def intersect(self, other: Prism) -> None:
        new_prisms = []
        for p in self.prisms:
            new_prism = p.intersection(other)
            if new_prism is not None:
                new_prisms.append(new_prism)
        
        self.prisms += new_prisms
    
    def volume(self) -> int:
        return sum(p.volume() for p in self.prisms)
    
    def append(self, prism: Prism):
        self.prisms.append(prism)

class Solution:
    def __init__(self, filename: str):
        with open(filename, "r") as f:
            self.input = f.read()
        
        self.lines = self.input.splitlines()
        self.instructions = []
        for line in self.lines:
            state = ON if line.split()[0] == "on" else OFF
            nums = re.findall(r"-?\d+", line)
            xrange = [int(nums[0]), int(nums[1])]
            yrange = [int(nums[2]), int(nums[3])]
            zrange = [int(nums[4]), int(nums[5])]
            self.instructions.append((state, xrange, yrange, zrange))
        
        self.better_instrs = []
        for state, xrange, yrange, zrange in self.instructions:
            self.better_instrs.append((state, Prism(
                xrange[0], xrange[1],
                yrange[0], yrange[1],
                zrange[0], zrange[1]
            )))

    def solve_part1(self) -> int:
        reactor = [[[OFF] * 101 for _ in range(101)] for _ in range(101)]
        for state, xrange, yrange, zrange in self.instructions[:END]:
            for x in range(xrange[0], xrange[1] + 1):
                for y in range(yrange[0], yrange[1] + 1):
                    for z in range(zrange[0], zrange[1] + 1):
                        reactor[x + 50][y + 50][z + 50] = state
        
        return sum(sum(sum(row) for row in col) for col in reactor)

    def solve_part2(self) -> int:
        total = 0
        maxlen = 0
        total_len = defaultdict(int)
        # 3D cube overlap calculations
        a = time.time()
        for i, instr in enumerate(self.better_instrs[:END]):
            state, prism = instr
            if state == OFF:
                continue

            v = Volume([prism])
            for _, other_prism in self.better_instrs[i + 1:END]:
                v.intersect(other_prism)
            
            maxlen = max(maxlen, len(v))
            total_len[len(v)] += 1
            total += v.volume()

        # print(maxlen, total_len)
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
    day = re.search(r"\d+", sys.argv[0]).group(0)
    filename = f"inputs/d{day}.txt"
    if args.example:
        filename = f"inputs/d{day}ex.txt"

    sol = Solution(filename)
    # print(f"Part 1: {sol.solve_part1()}")
    print(f"Part 2: {sol.solve_part2()}")
