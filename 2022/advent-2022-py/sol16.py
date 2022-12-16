
import argparse as ap
import re
import sys
import pyperclip
import functools
from datetime import datetime
from typing import List, Dict, Set, Callable, Tuple, Union, Optional, Any
from copy import deepcopy
from tqdm import tqdm
from collections import deque


MINUTES = 30


class Valve:
    def __init__(self, name: str, flow: int, connections: List[str]):
        self.name = name
        self.flow = flow
        self.connections = connections
        self.opened = 0

    def __repr__(self) -> str:
        return f"{self.name} ({self.flow}, {self.opened}) {self.connections}"
    
    def __hash__(self) -> int:
        return hash((self.name, self.opened))

    def is_open(self) -> bool:
        return self.opened > 0

    def open(self, time: int) -> None:
        self.opened = time
    
    def close(self) -> None:
        self.opened = 0

    def total_flow(self) -> int:
        return self.flow * (MINUTES - self.opened) if self.is_open() else 0


class State:
    def __init__(self, t: int, curr: str, valves: Dict[str, Valve]):
        self.t = t
        self.curr = curr
        self.valves = valves
    
    def __repr__(self) -> str:
        s = f"curr: {self.curr}\n"
        for v in self.valves.values():
            s += f"{v}\n"

        return s

    def __hash__(self) -> int:
        return hash((self.t, self.curr, tuple(self.valves.values())))

    def is_done(self) -> bool:
        return self.t > MINUTES

    def total_flow(self) -> int:
        return sum([v.total_flow() for v in self.valves.values()])
    
    def successors(self) -> List["State"]:
        succs = []
        curr_valve = self.valves[self.curr]
        if not curr_valve.is_open() and curr_valve.flow > 0:
            # Open the valve
            new_state = deepcopy(self)
            new_state.valves[self.curr].open(self.t)
            new_state.t += 1
            succs.append(new_state)

        for conn in curr_valve.connections:
            new_state = deepcopy(self)
            new_state.curr = conn
            new_state.t += 1
            succs.append(new_state)

        return succs


class Stepper_State:
    def __init__(
        self,
        valves: Dict[str, Valve],
        graph: Dict[str, Dict[str, int]],
        curr: str="AA",
        t: int=0
    ):
        self.valves = valves
        self.graph = graph
        self.curr = curr
        self.t = t
        self.hist = []

    def __repr__(self) -> str:
        s = f"curr: {self.curr}\n"
        for v in self.valves.values():
            if v.flow > 0:
                s += f"{v}\n"

        return s
    
    def __hash__(self) -> int:
        return hash((self.t, self.curr, tuple(self.valves.values())))
    
    def is_done(self) -> bool:
        remaining = MINUTES - self.t
        return all(
            self.graph[self.curr][vname] >= remaining
            for vname in self.next_steps()
        )
    
    def total_flow(self) -> int:
        return sum([v.total_flow() for v in self.valves.values()])
    
    def step(self, vname: str) -> None:
        tcost = self.graph[self.curr][vname]
        self.hist.append((self.curr, tcost))
        self.t += tcost + 1
        self.curr = vname
        self.valves[vname].open(self.t)
    
    def unstep(self) -> None:
        vname, tcost = self.hist.pop()
        self.t -= tcost + 1
        self.valves[self.curr].close()
        self.curr = vname
    
    def next_steps(self) -> List[str]:
        return [
            vname for vname in self.graph[self.curr]
            if self.graph[self.curr][vname] <= MINUTES - self.t
            and not self.valves[vname].is_open()
        ]


class Solution:
    def __init__(self, filename: str):
        with open(filename, "r") as f:
            self.input = f.read()
            self.input_lines = self.input.splitlines()
        
        self.valves = {}
        for line in self.input_lines:
            name = line.split()[1]
            flow = int(line.split()[4].split('=')[1][:-1])
            connections = [n[:2] for n in line.split()[9:]]
            self.valves[name] = Valve(name, flow, connections)
        
        # For each valve, do a BFS to find the cost of the shortest path
        # to each other node in the graph with positive flow
        self.graph = {}
        for v in self.valves.values():
            if v.flow == 0 and v.name != "AA":
                continue

            self.graph[v.name] = {}
            queue = deque([(v.name, 0)])
            visited = set()
            while queue:
                curr, cost = queue.popleft()
                if curr in visited:
                    continue

                visited.add(curr)
                if curr != v.name and self.valves[curr].flow > 0:
                    self.graph[v.name][curr] = cost

                for conn in self.valves[curr].connections:
                    queue.append((conn, cost + 1))

    def solve_part1_old(self) -> int:
        start = State(1, 'AA', self.valves)
        stack = [start]
        visited = set()
        best = 0
        for _ in tqdm(range(10000000)):
            curr = stack.pop()
            if curr in visited:
                continue
            elif curr.is_done():
                if curr.total_flow() > best:
                    best = curr.total_flow()
                    print(curr, best)
            else:
                stack.extend(curr.successors())

        return best
    
    def solve_part1(self) -> int:
        """
        Run backtracking search to find an optimal end state.
        """

        @functools.lru_cache(maxsize=None)
        def backtrack(curr: Stepper_State) -> int:
            if curr.is_done():
                return curr.total_flow()

            best = 0
            for vname in curr.next_steps():
                curr.step(vname)
                best = max(best, backtrack(curr))
                curr.unstep()

            return best

        start = Stepper_State(self.valves, self.graph)
        return backtrack(start)


    def solve_part2(self) -> int:
        """
        Run backtracking search, but this time, you have an elephant
        working with you in parallel and as such, there is more weirdness.
        """


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
        if isinstance(x, tuple):
            x = x[0]

        pyperclip.copy(x)

    sol = Solution(filename)
    x = sol.solve_part2()
    print(f"Part 2: {x}")
    if x is not None:
        pyperclip.copy(x)
