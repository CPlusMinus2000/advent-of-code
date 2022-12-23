
import argparse as ap
import re
import sys
import unittest

from point import Point
from typing import List


def sgn(x):
    return (x > 0) - (x < 0)

def triangle_numbers():
    n = 1
    triangle = 0
    while True:
        yield triangle
        triangle += n
        n += 1

class Solution:
    def __init__(self, filename: str):
        with open(filename, 'r') as f:
            self.input = f.read()
        
        nums = [int(n) for n in re.findall(r"-?\d+", self.input)]
        self.xrange = nums[:2]
        self.yrange = nums[2:]
    
    def simulate(self, dx: int, dy: int):
        x, y = 0, 0
        while True:
            x += dx
            y += dy
            dx -= sgn(dx)
            dy -= 1
            yield x, y
    
    def solve_part1(self) -> int:
        maxHeight = dx = 0
        for i, n in enumerate(triangle_numbers()):
            if n in range(*self.xrange):
                dx = i
                break

        for x, y in self.simulate(dx, abs(min(self.yrange)) - 1):
            maxHeight = max(maxHeight, y)
            if x in range(*self.xrange) and y in range(*self.yrange):
                return maxHeight
    
    def all_valid(self) -> List[Point]:
        valid = []
        for i, n in enumerate(triangle_numbers()):
            if n in range(*self.xrange):
                dx_lower = i
                break
        
        dx_upper = max(self.xrange) + 1
        dy_bound = max([abs(yr) for yr in self.yrange])
        for dx in range(dx_lower, dx_upper):
            for dy in range(-dy_bound, dy_bound):
                debug = False
                
                for x, y in self.simulate(dx, dy):
                    debug and print(x, y, dy_bound)
                    hor = range(self.xrange[0], self.xrange[1] + 1)
                    ver = range(self.yrange[0], self.yrange[1] + 1)
                    if x in hor and y in ver:
                        valid.append(Point(dx, dy))
                        break
                    
                    if y < -dy_bound:
                        break
        
        return valid
 

    def solve_part2(self) -> int:
        points = self.all_valid()
        return len(points)


class Tester():
    def test_part2(self):
        ans = """
        23,-10  25,-9   27,-5   29,-6   22,-6   21,-7   9,0     27,-7   24,-5
        25,-7   26,-6   25,-5   6,8     11,-2   20,-5   29,-10  6,3     28,-7
        8,0     30,-6   29,-8   20,-10  6,7     6,4     6,1     14,-4   21,-6
        26,-10  7,-1    7,7     8,-1    21,-9   6,2     20,-7   30,-10  14,-3
        20,-8   13,-2   7,3     28,-8   29,-9   15,-3   22,-5   26,-8   25,-8
        25,-6   15,-4   9,-2    15,-2   12,-2   28,-9   12,-3   24,-6   23,-7
        25,-10  7,8     11,-3   26,-7   7,1     23,-9   6,0     22,-10  27,-6
        8,1     22,-8   13,-4   7,6     28,-6   11,-4   12,-4   26,-9   7,4
        24,-10  23,-8   30,-8   7,0     9,-1    10,-1   26,-5   22,-9   6,5
        7,5     23,-6   28,-10  10,-2   11,-1   20,-9   14,-2   29,-7   13,-3
        23,-5   24,-8   27,-9   30,-7   28,-5   21,-10  7,9     6,6     21,-5
        27,-10  7,2     30,-9   21,-8   22,-7   24,-9   20,-6   6,9     29,-5
        8,-2    27,-8   30,-5   24,-7"""

        ans_points = [
            Point(int(x), int(y)) for x, y in [
                x.split(',') for x in re.findall(r"-?\d+,-?\d+", ans)
            ]
        ]

        sol = Solution("inputs/d17ex.txt")
        points = sol.all_valid()
        for p in ans_points:
            if not any(p == x for x in points):
                print("Failed:", p)


if __name__ == "__main__":
    parser = ap.ArgumentParser()
    parser.add_argument(
        "-e", "--example",
        help="Use the example file for input instead of main",
        action="store_true"
    )

    args = parser.parse_args()
    day = re.search(r"\d+", sys.argv[0]).group(0)
    filename = f"inputs/d{day}.txt"
    if args.example:
        filename = f"inputs/d{day}ex.txt"
    
    sol = Solution(filename)
    print(f"Part 1: {sol.solve_part1()}")
    print(f"Part 2: {sol.solve_part2()}")

    t = Tester()
    t.test_part2()

    # unittest.main()
