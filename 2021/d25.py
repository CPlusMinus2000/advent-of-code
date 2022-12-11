import argparse as ap
import re
import sys

from copy import deepcopy


class Solution:
    def __init__(self, filename: str):
        with open(filename, "r") as f:
            self.input = f.read()
        
        self.lines = self.input.splitlines()
        self.seafloor = [[c for c in line] for line in self.lines]
        self.length = len(self.seafloor)
        self.width = len(self.seafloor[0])
    
    def at(self, x: int, y: int) -> str:
        return self.seafloor[y % self.length][x % self.width]
    
    def simulate(self) -> bool:
        moved = False
        seacopy = deepcopy(self.seafloor)
        for i in range(self.length):
            for j in range(self.width):
                if self.at(j, i) == '>' and self.at(j + 1, i) == '.':
                    seacopy[i][j] = '.'
                    seacopy[i][(j + 1) % self.width] = '>' 
                    moved = True
        
        self.seafloor = seacopy
        seacopy = deepcopy(self.seafloor)
        for i in range(self.length):
            for j in range(self.width):
                if self.at(j, i) == 'v' and self.at(j, i + 1) == '.':
                    seacopy[i][j] = '.'
                    seacopy[(i + 1) % self.length][j] = 'v'
                    moved = True
        
        self.seafloor = seacopy
        return moved
    
    def print_seafloor(self):
        for line in self.seafloor:
            print(''.join(line))

    def solve_part1(self) -> int:
        step = 0
        while self.simulate():
            step += 1
        
        return step + 1

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
    day = re.search(r"\d+", sys.argv[0]).group(0)
    filename = f"inputs/d{day}.txt"
    if args.example:
        filename = f"inputs/d{day}ex.txt"

    sol = Solution(filename)
    print(f"Part 1: {sol.solve_part1()}")
    # print(f"Part 2: {sol.solve_part2()}")
