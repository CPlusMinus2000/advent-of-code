
from collections import Counter

CYCLE_LENGTH = 6
TIMER_START = 9


class Lanternfish:
    def __init__(self, timer):
        self.timer = timer
    
    def next_day(self):
        if self.timer == 0:
            self.timer = CYCLE_LENGTH
            return True
        else:
            self.timer -= 1
            return False

class Solution:
    def __init__(self, file: str):
        self.file = file
        with open(file, 'r') as f:
            self.data = f.read().split(',')
        
        self.fish = [Lanternfish(int(x)) for x in self.data]
    
    def simulate(self, cycles: int):
        for _ in range(cycles):
            for fish in self.fish:
                res = fish.next_day()
                if res:
                    self.fish.append(Lanternfish(TIMER_START))

            # print(','.join([str(f.timer) for f in self.fish]))
        
        return len(self.fish)
    
    def fast_sim(self, cycles: int):
        counts = Counter([f.timer for f in self.fish])
        for _ in range(cycles):
            buffer = Counter()
            buffer[6] = buffer[8] = counts[0]
            for i in range(1, TIMER_START):
                buffer[i - 1] += counts[i]
            
            counts = buffer
        
        return sum(counts.values())


sol = Solution('inputs/d6.txt')
print(sol.fast_sim(256))