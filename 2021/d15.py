# Advent of Code, Day 15

from point import Point
from copy import deepcopy
from collections import defaultdict

import heapq

class Solution:
    def __init__(self, filename: str) -> None:
        with open(filename) as f:
            self.input = f.read()
        
        self.lines = self.input.splitlines()
        self.grid = [
            [int(c) for c in line] for line in self.lines
        ]
    
    def adjacent_points(self, x: int, y: int):
        points = []
        if x > 0:
            points.append(Point(x - 1, y))
        if x < len(self.grid[0]) - 1:
            points.append(Point(x + 1, y))
        if y > 0:
            points.append(Point(x, y - 1))
        if y < len(self.grid) - 1:
            points.append(Point(x, y + 1))

        return points
    
    def graph_from_grid(self):
        # First, turn the grid into a graph
        graph = {}
        for y, line in enumerate(self.grid):
            for x, value in enumerate(line):
                graph[Point(x, y)] = {
                    p: value
                    for p in self.adjacent_points(x, y)
                }
        
        return graph
    
    def print_grid(self):
        for line in self.grid:
            print("".join(str(n) for n in line))

    def dijkstra(self, graph, start, end): 
        # Now, find the shortest path from the start to the end
        shortest_paths = {start: (None, 0)}
        current_node = start
        visited = set()

        while current_node != end:
            visited.add(current_node)
            if len(visited) % 2500 == 0:
                print(len(visited))

            for next_node, value in graph[current_node].items():
                weight = value + shortest_paths[current_node][1]
                if next_node not in shortest_paths or weight < shortest_paths[next_node][1]:
                    shortest_paths[next_node] = (current_node, weight)
        
            next_dests = {
                p: shortest_paths[p] for p in shortest_paths
                if p not in visited
            }

            if not next_dests:
                return "No path found"
            
            current_node = min(next_dests, key=lambda p: next_dests[p][1])
        
        return shortest_paths[end][1]
    
    def better_dijkstra(self, graph, start, end):
        dists = {start: 0}
        unvisited = [(float("inf"), p) for p in graph if p != start]
        unvisited.append((0, start))
        heapq.heapify(unvisited)
        visited = set()

        while unvisited:
            if len(visited) % 2500 == 0:
                print(len(visited))

            _, current_node = heapq.heappop(unvisited)
            if current_node == end:
                return dists[current_node]
            
            for next_node, value in graph[current_node].items():
                if next_node in visited:
                    continue

                weight = value + dists[current_node]
                if next_node not in dists or weight < dists[next_node]:
                    dists[next_node] = weight
                    heapq.heappush(unvisited, (weight, next_node))
            
            visited.add(current_node)
            unvisited = [p for p in unvisited if p[1] not in visited]
            heapq.heapify(unvisited)
        
        raise Exception("No path found")
        
    def even_better_dijkstra(self, graph, start, end):
        dists = {start: 0}
        unvisited = [(0, start)]
        heapq.heapify(unvisited)
        visited = set()

        while unvisited:
            if len(visited) % 2500 == 0:
                print(len(visited))

            _, current_node = heapq.heappop(unvisited)
            if current_node == end:
                return dists[current_node]
            
            for next_node, value in graph[current_node].items():
                if next_node in visited:
                    continue

                weight = value + dists[current_node]
                if next_node not in dists or weight < dists[next_node]:
                    dists[next_node] = weight
                    heapq.heappush(unvisited, (weight, next_node))
            
            visited.add(current_node)
            unvisited = [p for p in unvisited if p[1] not in visited]
            # heapq.heapify(unvisited)
        
        raise Exception("No path found")

    def solve_part1(self) -> int:
        start = Point(0, 0)
        end = Point(len(self.grid[0]) - 1, len(self.grid) - 1)
        return self.dijkstra(self.graph_from_grid(), start, end)
 
    def solve_part2(self) -> int:
        # First I have to duplicate the grid 5 times right and down
        def increment_line(line):
            lc = line.copy()
            for i, n in enumerate(line):
                lc[i] = n % 9 + 1
            
            return lc
        
        for i, line in enumerate(self.grid):
            lc = increment_line(line)
            for _ in range(4):
                self.grid[i].extend(lc)
                lc = increment_line(lc)
        
        grid_copy = deepcopy(self.grid)
        grid_copy = [increment_line(line) for line in grid_copy]
        for _ in range(4):
            self.grid.extend(grid_copy)
            grid_copy = [increment_line(line) for line in grid_copy]

        start = Point(0, 0)
        end = Point(len(self.grid[0]) - 1, len(self.grid) - 1)
        return self.dijkstra(self.graph_from_grid(), start, end)
        # return self.even_better_dijkstra(self.graph_from_grid(), start, end)


sol = Solution("inputs/d15.txt")
g = deepcopy(sol.grid)
# print(f"Part 1: {sol.solve_part1()}")
print(f"Part 2: {sol.solve_part2()}")

def a(grid):
    dists = [[-1 for _ in range(len(grid[0]))] for j in range(len(grid))]
    visited = [defaultdict(bool) for _ in range(len(grid))]
    dists[0][0] = 0
    visited[0][0] = True
    prique = defaultdict(list)
    grid[0][0] = 0 ######
    pt = [0,0]
    last = [-1,-1]
    r=len(grid)
    c=len(grid[0])
    #print(pt[0])
    while pt[0] != r-1 or pt[1] != c-1: # and prique not empty?
        #if pt == last: print(pt)
        #last[0],last[1] = pt[0],pt[1]
        i,j = pt
        for y,x in [[i-1,j],[i,j-1],[i,j+1],[i+1,j]]:
            if 0 <= x < c and 0 <= y < r:
                if visited[y][x]: continue
                val = dists[i][j] + grid[y][x]
                if not val in prique:
                    prique[val] = []
                prique[val].append([y,x])
                
                if dists[y][x] == -1:
                    dists[y][x] = val
                else:
                    dists[y][x] = min(dists[y][x], val)
        visited[i][j] = True
        for k in range(max(0, dists[i][j]-10), dists[i][j]+10):
            while len(prique[k]) > 0 and visited[prique[k][0][0]][prique[k][0][1]]: ### ????
                prique[k].pop(0)
            if len(prique[k]) > 0:
                pt = prique[k].pop(0)
                break


    #for line in dists: print(line)
    return dists[r-1][c-1]

def inc(x,k):
    if x + k >= 10:
        return (x+k)%10+1
    return x+k

def b(x):
    grid = [
        x[i] + list(map(lambda x: inc(x,1), x[i])) + list(map(lambda x: inc(x,2), x[i])) + list(map(lambda x: inc(x,3), x[i]))+list(map(lambda x: inc(x,4), x[i])) for i in range(len(x))
    ]
    r = len(x)
    for k in range(1,5):
        #print(k)
        for i in range(r):
            grid.append(list(map(lambda x:inc(x,k), grid[i])))
    #for line in grid: print(''.join(map(str,line)))#print(grid)
    
    
    return a(grid)

# print(b(g))