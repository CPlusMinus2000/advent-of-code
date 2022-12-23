
import { readFileSync } from "fs";

class Solution {
    public crabs: number[];
    public minCrab: number;
    public maxCrab: number;

    constructor(filepath: string) {
        const input = readFileSync(filepath, "utf-8");
        this.crabs = input.split(',').map(Number);
        this.minCrab = Math.min(...this.crabs);
        this.maxCrab = Math.max(...this.crabs);
    }

    public solvePart1(): number {
        let best = Infinity;
        let bestPos = 0;
        for (let i = this.minCrab; i <= this.maxCrab; i++) {
            let dist = 0;
            for (let c of this.crabs) {
                dist += Math.abs(c - i);
            }

            if (dist < best) {
                best = dist;
                bestPos = i;
            }
        }

        console.log("Bestpos: " + bestPos);
        return best;
    }

    public solvePart1Fast(): number {
        let crabSum = this.crabs.reduce((a, b) => a + b, 0);
        let bestPos = Math.round(crabSum / this.crabs.length);

        console.log("Bestpos: " + bestPos);
        return this.crabs.reduce((a, b) => a + Math.abs(b - bestPos), 0);
    }

    public solvePart2(): number {
        let best = Infinity;
        for (let i = this.minCrab; i <= this.maxCrab; i++) {
            let dist = 0;
            for (let c of this.crabs) {
                let d = Math.abs(c - i);
                dist += d * (d + 1) / 2;
            }

            if (dist < best) {
                best = dist;
            }
        }

        return best;
    }
}

let sol = new Solution('inputs/d7.txt');
console.log(sol.solvePart1());
console.log(sol.solvePart1Fast());
console.log(sol.solvePart2());