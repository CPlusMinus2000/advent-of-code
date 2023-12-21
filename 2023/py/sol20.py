import argparse as ap
import re
import abc
import sys
import enum
import pyperclip
import itertools
import math
from datetime import datetime
from typing import List, Dict, Set, Callable, Tuple, Union, Optional, Any
from tqdm import tqdm, trange
from collections import defaultdict, deque


# Enum for ON and OFF
class State(enum.Enum):
    ON = enum.auto()
    OFF = enum.auto()


# Enum for LOW and HIGH
class Pulse(enum.Enum):
    LOW = enum.auto()
    HIGH = enum.auto()


# base class for modules
class Module(abc.ABC):
    def __init__(self, name: str, outputs: List):
        self.name = name
        self.outputs = outputs

    def __repr__(self) -> str:
        return f"{self.name} -> {self.outputs}"

    @abc.abstractmethod
    def recv(self, mname: str, pulse: Pulse) -> List[Tuple[str, str, Pulse]]:
        pass

    @abc.abstractmethod
    def reset(self) -> None:
        pass


class FlipFlop(Module):
    def __init__(self, name: str, outputs: List):
        super().__init__(name, outputs)
        self.state = State.OFF

    def __repr__(self) -> str:
        return f"%{self.name} -> {self.outputs} ({self.state})"

    def recv(self, mname: str, pulse: Pulse) -> List[Tuple[str, str, Pulse]]:
        if pulse == Pulse.LOW:
            if self.state == State.OFF:
                self.state = State.ON
                return [(self.name, output, Pulse.HIGH) for output in self.outputs]
            else:
                self.state = State.OFF
                return [(self.name, output, Pulse.LOW) for output in self.outputs]
        else:
            return []

    def reset(self) -> None:
        self.state = State.OFF


class Inverter(Module):
    def __init__(self, name: str, outputs: List):
        super().__init__(name, outputs)
        self.memory: Dict[str, Pulse] = {}

    def __repr__(self) -> str:
        return f"&{self.name} -> {self.outputs}"

    def recv(self, mname: str, pulse: Pulse) -> List[Tuple[str, str, Pulse]]:
        assert mname in self.memory, f"{mname} not in memory of {self.name}"
        self.memory[mname] = pulse
        if all(pulse == Pulse.HIGH for pulse in self.memory.values()):
            return [(self.name, output, Pulse.LOW) for output in self.outputs]
        else:
            return [(self.name, output, Pulse.HIGH) for output in self.outputs]

    def reset(self) -> None:
        self.memory = {k: Pulse.LOW for k in self.memory}


class Solution:
    def __init__(self, filename: str):
        with open(filename, "r") as f:
            self.input = f.read()
            self.input_lines = self.input.splitlines()

        self.modules: Dict[str, Module] = {}
        for line in self.input_lines:
            mname, outputs = line.split(" -> ")
            outputs = outputs.split(", ")
            if mname == "broadcaster":
                self.broadcast_list = [
                    ("broadcaster", output, Pulse.LOW) for output in outputs
                ]
            elif mname.startswith("%"):
                mname = mname[1:]
                self.modules[mname] = FlipFlop(mname, outputs)
            else:  # Inverter
                mname = mname[1:]
                self.modules[mname] = Inverter(mname, outputs)

        for line in self.input_lines:
            mname, outputs = line.split(" -> ")
            outputs = outputs.split(", ")
            if mname != "broadcaster":
                mname = mname[1:]

            for output in outputs:
                if output in self.modules and isinstance(
                    self.modules[output], Inverter
                ):
                    self.modules[output].memory[mname] = Pulse.LOW

    def reset_all(self) -> None:
        for module in self.modules.values():
            module.reset()

    def button(
        self, watch_module: Optional[str] = None, watch_pulse: Optional[Pulse] = None
    ) -> Tuple[int]:
        low, high = 1, 0
        self.pulse_queue = deque(self.broadcast_list)
        watch_count = {Pulse.LOW: 0, Pulse.HIGH: 0}
        while self.pulse_queue:
            sname, mname, pulse = self.pulse_queue.popleft()
            if pulse == Pulse.LOW:
                low += 1
            else:
                high += 1

            if mname not in self.modules:
                continue
            elif watch_module and mname == watch_module and pulse == watch_pulse:
                watch_count[pulse] += 1

            self.pulse_queue.extend(self.modules[mname].recv(sname, pulse))

        if watch_module and watch_count[watch_pulse] == 1:
            raise RuntimeError("watch count is 1")

        return low, high

    def solve_part1(self) -> int:
        low, high = 0, 0
        for _ in range(1000):
            clow, chigh = self.button()
            low += clow
            high += chigh

        return low * high

    def cycles_until_pulse(self, mname: str, pulse: Pulse) -> int:
        self.reset_all()
        for i in tqdm(itertools.count()):
            try:
                self.button(mname, pulse)
            except RuntimeError:
                return i + 1

    def solve_part2(self) -> int:
        # Start a for loop with no end
        # Until we get a RuntimeError
        watch_list = ["bh", "jf", "sh", "mz"]
        watch_counts = []
        for watch in watch_list:
            watch_counts.append(self.cycles_until_pulse(watch, Pulse.LOW))

        return math.lcm(*watch_counts)


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
