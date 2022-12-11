
import { readFileSync } from "fs";

type Point = {
    x: number;
    y: number;
}

class Solution {
    public input: string;
    public lines: string[];
    public heightMap: number[][];
    public width: number;
    public length: number;

    constructor(filename: string) {
        this.input = readFileSync(filename, "utf-8");
        this.lines = this.input.split("\n").map(line => line.trim());
        this.heightMap = this.lines.map(line => line.split("").map(Number));
        this.width = this.heightMap[0].length;
        this.length = this.heightMap.length;
    }

    private getAdjacent(p: Point): Point[] {
        let points: Point[] = [];
        if (p.x > 0) {
            points.push({ x: p.x - 1, y: p.y });
        }

        if (p.x < this.width - 1) {
            points.push({ x: p.x + 1, y: p.y });
        }

        if (p.y > 0) {
            points.push({ x: p.x, y: p.y - 1 });
        }

        if (p.y < this.length - 1) {
            points.push({ x: p.x, y: p.y + 1 });
        }

        return points;

    }

    public findLowests(): Point[] {
        let lowests = [];
        for (let y = 0; y < this.length; y++) {
            for (let x = 0; x < this.width; x++) {
                let current = this.heightMap[y][x];
                let adjacent = this.getAdjacent({ x, y }).map(p => this.heightMap[p.y][p.x]);
                if (adjacent.every(a => a > current)) {
                    lowests.push({ x, y });
                }
            }
        }

        return lowests;
    }

    public solvePart1(): number {
        let lowests = this.findLowests();
        let lowSum = lowests.reduce((sum, p) => sum + this.heightMap[p.y][p.x], 0);
        return lowests.length + lowSum;
    }

    public solvePart2(): number {
        let basinSizes: number[] = [];
        let lowests = this.findLowests();
        for (let lowest of lowests) {
            let stack = [lowest];
            let visited = new Set<string>([`${lowest.x},${lowest.y}`]);
            let size = 1;
            while (stack.length > 0) {
                let current = stack.pop();
                if (current === undefined) {
                    continue;
                }

                let adjacent = this.getAdjacent(current);
                for (let adj of adjacent) {
                    let adjHeight = this.heightMap[adj.y][adj.x];
                    if (adjHeight > this.heightMap[current.y][current.x] &&
                        adjHeight !== 9 && !visited.has(`${adj.x},${adj.y}`)) {
                        stack.push(adj);
                        visited.add(`${adj.x},${adj.y}`);
                        size++;
                    }
                }
            }

            basinSizes.push(size);
        }

        basinSizes.sort((a, b) => b - a);
        return basinSizes[0] * basinSizes[1] * basinSizes[2];
    }


}

let sol = new Solution("inputs/d9.txt");
console.log(`Part 1: ${sol.solvePart1()}`);
console.log(`Part 2: ${sol.solvePart2()}`);