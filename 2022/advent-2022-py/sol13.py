
import argparse as ap
import re
import sys
import pyperclip
from datetime import datetime
from typing import List, Union


class Packet:
    def __init__(self, val: Union[int, List["Packet"]]):
        if isinstance(val, int):
            self.val = val
        elif isinstance(val, list):
            for i in range(len(val)):
                val[i] = Packet(val[i])

            self.val = val

    def __repr__(self):
        return "P(" + str(self.val) + ")"

    def __str__(self):
        return "P(" + str(self.val) + ")"

    def __len__(self):
        if isinstance(self.val, int):
            return 1
        else:
            return len(self.val)

    def __getitem__(self, key):
        return self.val[key]

    def __eq__(self, other):
        sval, oval = self.val, other.val
        if isinstance(self.val, int) and isinstance(other.val, int):
            return self.val == other.val
        elif isinstance(self.val, list) and isinstance(other.val, int):
            return len(self.val) == 1 and self.val[0] == other
        elif isinstance(self.val, int) and isinstance(other.val, list):
            return len(other.val) == 1 and other.val[0] == self

        if len(sval) != len(oval):
            return False
        else:
            for i in range(len(sval)):
                if not sval[i] == oval[i]:
                    return False

            return True

    def __lt__(self, other):
        sval, oval = self.val, other.val
        if isinstance(self.val, int) and isinstance(other.val, int):
            return self.val < other.val
        elif isinstance(self.val, list) and isinstance(other.val, int):
            oval = Packet([other.val])
        elif isinstance(self.val, int) and isinstance(other.val, list):
            sval = Packet([self.val])

        for i in range(len(oval)):
            if i >= len(sval):
                return True
            elif not sval[i] == oval[i]:
                return sval[i] < oval[i]

        return False  # equal


class Solution:
    def __init__(self, filename: str):
        with open(filename, "r") as f:
            self.input = f.read()
            self.packets = self.input.split("\n\n")

        self.all_packets = []
        for packets in self.packets:
            p1, p2 = packets.splitlines()
            p1 = Packet(eval(p1))
            p2 = Packet(eval(p2))
            self.all_packets.extend([p1, p2])

        self.all_packets.extend([Packet([[2]]), Packet([[6]])])

    def solve_part1(self) -> int:
        total = 0
        for i, packets in enumerate(self.packets):
            p1, p2 = packets.splitlines()
            p1 = Packet(eval(p1))
            p2 = Packet(eval(p2))
            print(p1, p2)
            if p1 < p2:
                total += i + 1

        return total

    def solve_part2(self) -> int:
        # Sort all the packets
        self.all_packets.sort()
        i, j = 0, 0
        for k, packet in enumerate(self.all_packets):
            if packet == Packet([[2]]):
                i = k
            elif packet == Packet([[6]]):
                j = k

        return (i + 1) * (j + 1)


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
    pyperclip.copy(x)

    sol = Solution(filename)
    x = sol.solve_part2()
    print(f"Part 2: {x}")
    pyperclip.copy(x)
