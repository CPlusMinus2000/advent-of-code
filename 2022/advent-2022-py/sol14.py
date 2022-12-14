
import argparse as ap
import re
import sys
import pyperclip
import random
from datetime import datetime
from typing import List, Tuple
from tqdm import tqdm

import numpy as np
import cv2


def print_grid(grid: List[List[str]], printout: bool=True) -> None:
    txt = ""
    for row in grid:
        if printout:
            print("".join(row))

        txt += "".join(row) + '\n'

    return txt


FIDELITY = 8
FPS = 960

class Encoder:
    def __init__(
        self,
        filename: str,
        codec: str = "mp4v",
        fps: int = FPS,
        grid: List[List[str]] = None
    ):
        fourcc = cv2.VideoWriter_fourcc(*codec)
        self.grid = grid
        self.width = len(grid[0]) * FIDELITY
        self.height = len(grid) * FIDELITY
        self.out = cv2.VideoWriter(
            filename, fourcc, fps, (self.width, self.height))

        self.frame = np.zeros((self.height, self.width, 3), np.uint8)

        # Draw the grid
        for j in range(len(self.grid)):
            for i in range(len(self.grid[0])):
                if self.grid[j][i] == '#':
                    # Draw in grey
                    self.draw((i, j), rgb=(100, 100, 100))

    def draw(self, pixel: Tuple[int], rgb: Tuple[int]=(245, 220, 0)):
        # Convert the pixel to a 1x1 yellow image
        rgb = list(rgb)
        rgb[0] += random.randint(-20, 10)
        rgb[1] += random.randint(-20, 20)
        image = np.array([[rgb[::-1]]], dtype=np.uint8)
        image = cv2.resize(image, (FIDELITY, FIDELITY), interpolation=cv2.INTER_NEAREST)
        x, y = pixel[0] * FIDELITY, pixel[1] * FIDELITY
        self.frame[y:y+image.shape[0], x:x+image.shape[1], 0:3] = image
        self.out.write(np.copy(self.frame))

    def save(self):
        self.out.release()


class Solution:
    def __init__(self, filename: str, part: int, video: str="sol14.mp4"):
        with open(filename, "r") as f:
            self.input = f.read()
            self.input_lines = self.input.splitlines()

        self.points = []
        self.rocks = []
        for line in self.input_lines:
            points = re.findall(r"(\d+),(\d+)", line)
            points = [(int(x), int(y)) for x, y in points]
            self.points.extend(points)
            self.rocks.append(points)

        if part == 1:
            self.left = min(x for x, y in self.points)
        elif part == 2:
            self.left = min(x for x, y in self.points) // 3 * 2

        self.right = max(x for x, y in self.points)
        self.bottom = max(y for x, y in self.points)

        for line in self.rocks:
            for i in range(len(line)):
                line[i] = (line[i][0] - self.left, line[i][1])

        self.right -= self.left
        self.grid = [['.'] * (part * self.right + 1) for _ in range(self.bottom + 3)]
        for line in self.rocks:
            sx, sy = line[0]
            for x, y in line[1:]:
                for i in range(min(sx, x), max(sx, x) + 1):
                    for j in range(min(sy, y), max(sy, y) + 1):
                        print(i, j, self.left, self.right)
                        self.grid[j][i] = '#'

                sx, sy = x, y

        if part == 2:
            self.grid[self.bottom + 2] = ['#'] * (2 * self.right + 1)

        self.sand = 500 - self.left
        self.encoder = Encoder(f"../sillyXD/{video}", grid=self.grid)


    def place_sand(self) -> bool:
        sx, sy = self.sand, 0
        while sy < self.bottom:
            if self.grid[sy + 1][sx] != '.':
                if self.grid[sy + 1][sx - 1] != '.':
                    if self.grid[sy + 1][sx + 1] != '.':
                        self.grid[sy][sx] = 'o'
                        return sx, sy
                    else:
                        sx += 1
                else:
                    sx -= 1

            sy += 1

        return 500 - self.left, 0


    def place_sand2(self) -> bool:
        sx, sy = self.sand, 0
        while self.grid[0][500 - self.left] == '.':
            if self.grid[sy + 1][sx] != '.':
                if self.grid[sy + 1][sx - 1] != '.':
                    if self.grid[sy + 1][sx + 1] != '.':
                        self.grid[sy][sx] = 'o'
                        return sx, sy
                    else:
                        sx += 1
                else:
                    sx -= 1

            sy += 1

        return 500 - self.left, 0


    def solve_part1(self) -> int:
        count = 0
        sx, sy = self.place_sand()
        for _ in tqdm(range(888)):
            self.encoder.draw((sx, sy))
            count += 1
            sx, sy = self.place_sand()

        self.encoder.save()
        return count


    def solve_part2(self) -> int:
        count = 0
        sx, sy = self.place_sand2()
        for _ in tqdm(range(26460)):
            self.encoder.draw((sx, sy))

            count += 1
            sx, sy = self.place_sand2()

        self.encoder.save()
        return count


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

    sol = Solution(filename, part=1, video="sol14a.mp4")
    x = sol.solve_part1()
    print(f"Part 1: {x}")
    if x is not None:
        pyperclip.copy(x)

    sol = Solution(filename, part=2, video="sol14v4.mp4")
    x = sol.solve_part2()
    print(f"Part 2: {x}")
    if x is not None:
        pyperclip.copy(x)
