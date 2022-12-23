
import { readFileSync} from "fs";
import cyan from "chalk";

type Point = {
    x: number;
    y: number;
};

type Fold = {
    dir: string;
    at: number;
};

class Solution {
    public input: string;
    public lines: string[];
    public points: Point[];
    public folds: Fold[];

    constructor(filename: string) {
        this.input = readFileSync(filename, "utf8");
        this.lines = this.input.split("\r\n");
        this.points = this.lines.filter(line => line.includes(',')).map(line => {
            const [x, y] = line.split(",").map(Number);
            return { x, y };
        });

        this.folds = this.lines.filter(line => line.includes("fold")).map(line => {
            const [dir, at] = line.split(" ")[2].split("=");
            return { dir, at: Number(at) };
        });
    }

    private foldOver(times: number | undefined): Set<string> {
        let pointSet = new Set<string>(this.points.map(point => point.x + "," + point.y));
        for (let fold of this.folds.slice(0, times)) {
            let dir = fold.dir;
            let at = fold.at;
            for (let point of Array.from(pointSet)) {
                const [x, y] = point.split(",").map(Number);
                let p = { x: x, y: y };
                pointSet.delete(point);

                if (dir === "x" && p.x > at) {
                    p.x = 2 * at - p.x;
                } else if (dir === "y" && p.y > at) {
                    p.y = 2 * at - p.y;
                }

                pointSet.add(p.x + "," + p.y);

            }
        }

        return pointSet;
    }

    public solvePart1(): number {
        return this.foldOver(1).size;
    }

    public solvePart2(): string {
        let pointSet = this.foldOver(undefined);
        let maxX = 0, maxY = 0;
        for (let point of Array.from(pointSet)) {
            const [x, y] = point.split(",").map(Number);
            maxX = Math.max(maxX, x);
            maxY = Math.max(maxY, y);
        }

        let grid = new Array(maxY + 1).fill(0).map(() => new Array(maxX + 1).fill(0));
        for (let point of Array.from(pointSet)) {
            const [x, y] = point.split(",").map(Number);
            grid[y][x] = 1;
        }

        let result = "";
        for (let row of grid) {
            for (let cell of row) {
                result += cell === 1 ? cyan("#") : " ";
            }
            result += "\n";
        }

        return result;
    }
}

let sol = new Solution("inputs/d13.txt");
console.log(`Part 1: ${sol.solvePart1()}`);
console.log(`Part 2:\n${sol.solvePart2()}`);