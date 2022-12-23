import argparse as ap
import re
import sys

from copy import deepcopy

class Solution:
    def __init__(self, filename: str):
        with open(filename, "r") as f:
            self.input = f.read()
        
        convert = {'.': 0, '#': 1}
        self.lines = self.input.splitlines()
        self.algo = [convert[c] for c in self.lines[0]]
        self.image = [[convert[c] for c in line] for line in self.lines[2:]]
        self.background_state = 0
        self.background_convert = {
            0: self.algo[0],
            1: self.algo[-1]
        }
    
    def out_of_bounds(self, x: int, y: int) -> int:
        return (
            x < 0 
            or x >= len(self.image[0])
            or y < 0
            or y >= len(self.image)
        )
    
    def decode_index(self, x: int, y: int) -> int:
        index = 0
        for i in range(y - 1, y + 2):
            for j in range(x - 1, x + 2):
                if self.out_of_bounds(j, i):
                    index = (index << 1) + self.background_state
                else:
                    index = (index << 1) + self.image[i][j]

        return index
    
    def enhance(self) -> None:
        """
        Enhances an image according to the internal algorithm.
        """

        # Start by enlarging the image with a border of background.
        c = self.background_state
        self.image = [
            [c] * (len(self.image[0]) + 2)
        ] + [
            [c] + line + [c] for line in self.image
        ] + [
            [c] * (len(self.image[0]) + 2)
        ]

        image_copy = deepcopy(self.image)

        # Iterate over the image and enhance each pixel.
        for y in range(len(self.image)):
            for x in range(len(self.image[0])):
                ind = self.decode_index(x, y)
                # print(x, y, ind)
                image_copy[y][x] = self.algo[ind]
        
        self.background_state = self.background_convert[self.background_state]
        self.image = image_copy
    
    def lit_pixels(self) -> int:
        return sum(sum(line) for line in self.image)
    
    def print_image(self) -> None:
        devert = {0: '.', 1: '#'}
        for line in self.image:
            print("".join(devert[c] for c in line))
        
        print()

    def solve_part1(self) -> int:
        for _ in range(2):
            self.enhance()
        
        return self.lit_pixels()

    def solve_part2(self) -> int:
        for _ in range(48):
            self.enhance()
        
        return self.lit_pixels()


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
    print(f"Part 2: {sol.solve_part2()}")
