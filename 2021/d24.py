import argparse as ap
import re
import sys

from typing import Dict, List, Iterable


INIT = {
    'w': 0,
    'x': 0,
    'y': 0,
    'z': 0
}


class ALU:
    def __init__(self, inputs: str) -> None:
        self.inputs = inputs
        self.input_index = 0
        self.vars = INIT.copy()
    
    def __str__(self) -> str:
        return f"{self.vars}"
    
    def __repr__(self) -> str:
        return f"ALU({self.vars})"
    
    def __hash__(self) -> int:
        return hash(str(self))
    
    def __input(self, var: str) -> None:
        self.vars[var] = int(self.inputs[self.input_index])
        self.input_index += 1
    
    def __add(self, var: str, val: str) -> None:
        if re.match("-?\d+", val):
            self.vars[var] += int(val)
        else:
            self.vars[var] += self.vars[val]
    
    def __mul(self, var: str, val: str) -> None:
        if re.match("-?\d+", val):
            self.vars[var] *= int(val)
        else:
            self.vars[var] *= self.vars[val]
    
    def __div(self, var: str, val: str) -> None:
        if re.match("-?\d+", val):
            self.vars[var] //= int(val)
        else:
            self.vars[var] //= self.vars[val]
    
    def __mod(self, var: str, val: str) -> None:
        if re.match("-?\d+", val):
            self.vars[var] %= int(val)
        else:
            self.vars[var] %= self.vars[val]
    
    def __eql(self, var: str, val: str) -> None:
        if re.match("-?\d+", val):
            self.vars[var] = int(self.vars[var] == int(val))
        else:
            self.vars[var] = int(self.vars[var] == self.vars[val])

    
    def read(self, instructions: List[str]) -> None:
        for instr in instructions:
            op, args = instr.split(' ')[0], instr.split(' ')[1:]
            if instr.startswith("inp"):
                self.__input(*args)
            elif instr.startswith("add"):
                self.__add(*args)
            elif instr.startswith("mul"):
                self.__mul(*args)
            elif instr.startswith("div"):
                self.__div(*args)
            elif instr.startswith("mod"):
                self.__mod(*args)
            elif instr.startswith("eql"):
                self.__eql(*args)
            else:
                raise ValueError(f"Unknown instruction: {instr}")
    

class Solution:
    def __init__(self, filename: str = "inputs/d24.txt"):
        with open(filename, "r") as f:
            self.input = f.read()
        
        self.instrs = self.input.splitlines()
        self.chunks = []
        for i in range(0, len(self.instrs), 18):
            self.chunks.append(self.instrs[i:i+18])
    
    def run_chunks(
        self,
        chunk_indices: List[int],
        vals: Iterable = range(10)
    ) -> Dict[int, int]:
        f = {}
        instrs = []
        for i in chunk_indices:
            instrs += self.chunks[i]
        
        for i in vals:
            if '0' in str(i).zfill(len(chunk_indices)):
                continue

            alu = ALU(str(i).zfill(len(chunk_indices)))
            alu.read(instrs)
            f[i] = alu.vars['z']
        
        return f
    
    def run_input(self, input_strs: List[str]) -> Dict[str, int]:
        f = {}
        for istr in input_strs:
            alu = ALU(istr)
            instrs = []
            for i in range(len(istr)):
                instrs += self.chunks[i]
            
            alu.read(instrs)
            f[istr] = alu.vars['z']
        
        return f


    def solve_part1(self) -> int:
        for i in range(99999999999999, 11111111111110, -1):
            s = str(i)
            if '0' in s:
                continue
                
            alu = ALU(s)
            alu.read(self.instrs)
            if alu.vars['z'] == 0:
                return i
            elif i % 1000 == 111:
                print(i)

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
