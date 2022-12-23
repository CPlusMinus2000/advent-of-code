
# Advent of Code, day 14

from collections import Counter, defaultdict
from functools import reduce

class Solution:
    def __init__(self, filename: str):
        with open(filename, 'r') as f:
            self.input = f.read()
        
        self.lines = self.input.splitlines()
        self.polymer = self.lines[0]
        self.equations = {
            e.split(' -> ')[0]: e.split(" -> ")[1]
            for e in self.lines if " -> " in e
        }
    
    def polymerize(self, steps: int) -> str:
        curr = self.polymer
        for _ in range(steps):
            res = curr[0]
            for i in range(len(curr) - 1):
                pair = curr[i:i+2]
                if pair in self.equations:
                    res += self.equations[pair] + pair[1]
            
            curr = res
        
        return res
    
    def part1(self) -> int:
        s = self.polymerize(10)
        c = Counter(s)
        return max(c.values()) - min(c.values())

    def part2(self) -> int:
        pairs = [self.polymer[i:i+2] for i in range(len(self.polymer) - 1)]
        counts = defaultdict(int)
        chars = Counter(self.polymer)
        for p in pairs:
            counts[p] = self.polymer.count(p)
 
        for _ in range(40):
            # print(counts)
            curr = counts.copy()
            for p in counts:
                if p in self.equations:
                    temp = counts[p]
                    curr[p] -= temp
                    p1, p2 = p[0] + self.equations[p], self.equations[p] + p[1]
                    # print(p, p1, p2, temp)
                    curr[p1] += temp
                    curr[p2] += temp
                    chars[self.equations[p]] += temp
                
            counts = curr

        return max(chars.values()) - min(chars.values())
    
    def pair_evolve(self, pair: str, depth: int) -> str:
        if depth == 0:
            return pair
        elif (pair, depth) in self.memo:
            return self.memo[pair, depth]
        
        elif pair in self.equations:
            s = pair[0] + self.equations[pair] + pair[1]
            d = depth - 1
            ret = self.pair_evolve(s[:2], d) + self.pair_evolve(s[1:], d)[1:]
            self.memo[pair, depth] = ret
            return ret
        
        else:
            return pair
    
    def recursive_solve(self) -> str:
        self.memo = {}
        pairs = [self.polymer[i:i+2] for i in range(len(self.polymer) - 1)]
        try:
            evolved = [
                self.pair_evolve(p, 40) for p in pairs
            ]
        except KeyboardInterrupt:
            with open("memo.txt", "w") as f:
                f.write(str(self.memo))
            
            raise

        s = reduce(lambda x, y: x + y[1:], evolved)
        # print(evolved, s)
        c = Counter(s)
        return max(c.values()) - min(c.values())


sol = Solution("inputs/d14ex.txt")
# print(sol.part1())
# print(sol.part2())

print(sol.recursive_solve())
