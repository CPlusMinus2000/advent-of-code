def GetInput(_):
    with open("../data/day17.txt", 'r') as f:
        return f.read()

# This is @MikeXander's code, go follow him

ans = 0

ROCKS = [
    [
        [1,1,1,1]
    ],
    [
        [0,1,0],
        [1,1,1],
        [0,1,0]
    ],
    [
        [0,0,1],
        [0,0,1],
        [1,1,1]
    ],
    [
        [1],
        [1],
        [1],
        [1]
    ],
    [
        [1,1],
        [1,1]
    ]
]

from collections import defaultdict as DD

class Rock:
    def __init__(self, type, floor_y):
        self.block = ROCKS[type]
        self.height = len(self.block)
        self.width = len(self.block[0])
        self.pos = [2, floor_y + self.height + 3]
        self.prev_move = [0, 0]

        """
        x,y=self.pos
        for i in range(self.height):
            for j in range(self.width):
                print(f"({x+j},{y-i})[{self.block[i][j]}]", end=' ')
            print()
        """
        
    def __repr__(self):
        return f"{self.pos} {self.width}x{self.height}\n"

    # returns true if it fits in the board
    def valid(self, grid):
        x, y = self.pos
        if x < 0 or 7 <= x + self.width - 1: # rightmost coord
            return False
        if y - self.height + 1 < 0:
            return False
        for i in range(self.height):
            for j in range(self.width):
                if self.block[i][j] == 0:
                    continue
                if grid[x+j, y-i]:
                    return False
        return True

    def move(self, dx, dy):
        self.pos[0] += dx
        self.pos[1] += dy
        self.prev_move = [dx, dy]

    def undo_move(self):
        self.pos[0] -= self.prev_move[0]
        self.pos[1] -= self.prev_move[1]
        self.prev_move = [-x for x in self.prev_move]




class Board:
    def __init__(self, jet_pattern):
        self.grid = DD(bool)
        self.highest_floor = -1
        self.floor = -1
        self.jet_pattern = jet_pattern
        self.jpi = 0 # jet pattern index
        self.cached_states = [[] for _ in jet_pattern]

    def __repr__(self):
        s = ""
        width = len(str(self.highest_floor+6)) + 2
        for y in range(self.highest_floor+3, self.floor - 1, -1):
            s += f"{y} |".rjust(width)
            for x in range(7):
                s += '#' if self.grid[x, y] else '.'
            s += '|\n'
        return s + '+'.rjust(width) + '-------+\n'

    def topology(self): # return relevant default dictionary
        search = [(0, self.highest_floor+1)]
        new_grid = DD(bool)
        visited = DD(bool)
        visited[search[0]] = True
        floor = search[0][1]
        while search: # dfs is fine
            x,y = search.pop()
            if y < floor:
                floor = y
            neighbours = [(x-1, y), (x+1, y), (x, y-1)]
            if y != self.highest_floor + 1: # don't search up from here
                neighbours.append((x, y+1)) # need to search up for "caves"
            for i,j in neighbours:
                if visited[i, j] or i < 0 or 7 <= i or j < 0:
                    continue
                elif self.grid[i, j]:
                    new_grid[i, j] = True
                else:
                    search.append((i, j))
                visited[i,j] = True
        #print(new_grid)
        # read the columns as numbers (this is easier to compare for caching)
        hash_rep = []
        for x in range(7):
            hash_rep.append(0)
            for y in range(self.highest_floor+1, floor-1,-1):
                hash_rep[-1] = (hash_rep[-1] << 1) + int(new_grid[x, y])
        #print(hash_rep)
        return new_grid, hash_rep, floor-1

    # returns if this pattern has been seen before or not
    # if it hasnt, it will remember it
    def cache(self, rock_type, num_rocks): 
        new_grid, hash_rep, new_floor = self.topology()
        self.grid = new_grid
        self.floor = new_floor

        for type, hashed_grid, rocks_that_fell, old_height in self.cached_states[self.jpi]:
            if type == rock_type and hash_rep == hashed_grid:
                return rocks_that_fell, old_height
        self.cached_states[self.jpi].append(
            (rock_type, hash_rep, num_rocks, self.highest_floor)
        )
        return False, None

    def place(self, rock):
        x,y = rock.pos
        for i in range(rock.height):
            for j in range(rock.width):
                if rock.block[i][j] == 0:
                    continue
                self.grid[x+j, y-i] = True

    def remove(self, rock):
        x,y = rock.pos
        for i in range(rock.height):
            for j in range(rock.width):
                if rock.block[i][j] == 0:
                    continue
                self.grid[x+j, y-i] = False

    def drop_rock(self, type):
        r = Rock(type, self.highest_floor)
        #print("floor", self.highest_floor)
        while True:
            #self.place(r)
            #print(r)
            #print(self)
            #self.remove(r)

            i = self.jet_pattern[self.jpi]
            self.jpi = (self.jpi+1)%len(self.jet_pattern)
            if i == '>':
                r.move(1,0)
            else:
                r.move(-1,0)
            if not r.valid(self.grid):
                r.undo_move()
            
            r.move(0,-1)
            if not r.valid(self.grid):
                r.undo_move()
                self.place(r)
                #print(self)
                if self.highest_floor < r.pos[1]:
                    self.highest_floor = r.pos[1]
                break

sample = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"
"""b = Board(sample)
for i in range(2022):
    b.drop_rock(i%len(ROCKS))
    #print(b)
assert(b.highest_floor + 1 == 3068)
"""
b = Board(GetInput(17))
#b = Board(sample)

N = 1000000000000
#N = 2022 # part 1
#from tqdm import tqdm as ProgressBar
#for i in ProgressBar(range(N)):
i = 0
seen_height = 0
seen_something = False
ans = 0
while i < N:
    type = i % len(ROCKS)
    b.drop_rock(type)
    rocks_that_fell_to_get_here, old_height = b.cache(type, i+1)
    if not seen_something and rocks_that_fell_to_get_here:
        seen_something = True
        print("SEEN", i, i%len(b.jet_pattern), type, b.highest_floor)
        print(b)
        """
        N = 100
        i = 21
        rocks_that_fell_to_get_here = 3
        b.highest_floor = 4
        old_height = 1
        """
        # jump to new index (num rocks that fell)
        diff = i - rocks_that_fell_to_get_here + 1 # num rocks that fell to repeat
        times_repeated = (N-i)//diff
        print(i, diff, times_repeated * diff)
        i += times_repeated * diff

        # track height
        repeated_height = b.highest_floor - old_height
        ans = (b.highest_floor + 1) + repeated_height * times_repeated
        seen_height = b.highest_floor

        print(i, rocks_that_fell_to_get_here, times_repeated, ans)

    i += 1
    #print(b)
ans += b.highest_floor - seen_height
print(b)

#assert(ans == 1514285714288)

"""
i = 0
cached = False
while i < N:
    type = i % len(ROCKS)
    b.drop_rock(type)
    if not cached and b.cache(type):
        print("SEEN", i, i%len(b.jet_pattern), type)
        repeat = N//i
        b.highest_floor = repeat * (b.highest_floor+1) - 1
        N %= i
        i = 0
        cached = True
    i += 1
    #print(b)
ans = b.highest_floor + 1
"""

print(ans)
