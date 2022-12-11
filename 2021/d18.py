import argparse as ap
import re
import sys

from typing import List, Union, Optional
from math import floor, ceil


class Node:
    def __init__(self, val: Union[int, List[int]], depth: int = 0) -> None:
        self.val = val
        self.parent = None
        self.depth = depth
        if isinstance(val, list):
            self.children = [Node(v, depth + 1) for v in val]
            self.children[0].parent = self
            self.children[1].parent = self
        else:
            self.children = []

    def __str__(self) -> str:
        return str(self.val)

    def __repr__(self) -> str:
        return f"Node({self.val})"

    def __add__(self, other: "Node") -> "Node":
        return Node([self.val, other.val])
    
    def __eq__(self, other: "Node") -> bool:
        if isinstance(self.val, int) and isinstance(other.val, int):
            return self.val == other.val
        else:
            return self.val == other.val and self.children == other.children

    def reevaluate(self) -> None:
        if isinstance(self.val, int):
            return
        else:
            for c in self.children:
                c.reevaluate()

            self.val = [c.val for c in self.children]

    def leftmost_child(self) -> Optional["Node"]:
        if self.children:
            return self.children[0].leftmost_child()
        else:
            return self

    def rightmost_child(self) -> Optional["Node"]:
        if self.children:
            return self.children[-1].rightmost_child()
        else:
            return self

    def left_node(self) -> Optional["Node"]:
        curr = self
        pare = self.parent
        while pare is not None:
            if pare.children[1] is curr:
                return pare.children[0].rightmost_child()
            else:
                curr = pare
                pare = pare.parent

        return None

    def right_node(self) -> Optional["Node"]:
        curr = self
        pare = self.parent
        while pare is not None:
            if pare.children[0] is curr:
                return pare.children[1].leftmost_child()
            else:
                curr = pare
                pare = pare.parent

        return None

    def explosive(self) -> bool:
        if self.depth >= 4 and not isinstance(self.val, int):
            return True
        else:
            return any(c.explosive() for c in self.children)

    def explode(self) -> None:
        if (
            self.depth >= 4
            and self.children
            and all(isinstance(c.val, int) for c in self.children)
        ):
            l = self.children[0].left_node()
            if l is not None:
                l.val += self.children[0].val

            r = self.children[1].right_node()
            if r is not None:
                r.val += self.children[1].val

            self.children = []
            self.val = 0

        else:
            for child in self.children:
                child.explode()

    def splittable(self) -> bool:
        if isinstance(self.val, int) and self.val >= 10:
            return True
        else:
            return any(c.splittable() for c in self.children)

    def split(self) -> bool:
        if not isinstance(self.val, int) or self.val < 10:
            return any(c.split() for c in self.children)
        else:
            self.children = [
                Node(floor(self.val / 2), self.depth + 1),
                Node(ceil(self.val / 2), self.depth + 1),
            ]

            self.children[0].parent = self
            self.children[1].parent = self
            self.val = [c.val for c in self.children]
            return True

    def magnitude(self) -> int:
        if isinstance(self.val, int):
            return self.val
        else:
            magnitudes = [c.magnitude() for c in self.children]
            return 3 * magnitudes[0] + 2 * magnitudes[1]
    
    def reduce(self):
        while True:
            if self.explosive():
                self.explode()
                self.reevaluate()
            elif self.splittable():
                self.split()
                self.reevaluate()
            else:
                break


class Solution:
    def __init__(self, filename: str):
        with open(filename, "r") as f:
            self.input = f.read()

        self.lines = self.input.splitlines()
        self.nodes = [Node(eval(l)) for l in self.lines]

    def solve_part1(self) -> int:
        first = self.nodes[0]
        first.reduce()
        for node in self.nodes[1:]:
            first = first + node
            first.reduce()

        return first.magnitude()

    def solve_part2(self) -> int:
        maximum = 0
        for node1 in self.nodes:
            for node2 in self.nodes:
                if node1 is node2:
                    continue

                first = node1 + node2
                first.reduce()
                maximum = max(first.magnitude(), maximum)
        
        return maximum


if __name__ == "__main__":
    parser = ap.ArgumentParser()
    parser.add_argument(
        "-e",
        "--example",
        help="Use the example file for input instead of main",
        action="store_true",
    )

    parser.add_argument(
        "extension",
        type=str,
        nargs="?",
        default="",
        help="Extra characters to insert into the input file name if -e",
    )

    args = parser.parse_args()
    day = re.search(r"\d+", sys.argv[0]).group(0)
    filename = f"inputs/d{day}.txt"
    if args.example:
        filename = f"inputs/d{day}ex{args.extension}.txt"

    sol = Solution(filename)
    print(f"Part 1: {sol.solve_part1()}")
    print(f"Part 2: {sol.solve_part2()}")
