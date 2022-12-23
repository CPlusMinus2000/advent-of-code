
import { readFileSync } from "fs";

type Point = {
    x: number;
    y: number;
};

class Solution {
    public input: string;
    public octopi: number[][];
    public width: number;
    public height: number;

    constructor(filename: string) {
        this.input = readFileSync(filename, "utf8");
        this.octopi = this.input.split("\r\n").map(line => {
            return line.split("").map(Number);
        });

        this.width = this.octopi[0].length;
        this.height = this.octopi.length;
    }

    private printOctopi(s: string = ""): void {
        console.log(this.octopi.map(line => line.join("")).join("\n") + s);
    }

    private getNeighbors(x: number, y: number): Point[] {
        let neighbors = [];
        for (let i = -1; i <= 1; i++) {
            for (let j = -1; j <= 1; j++) {
                if (i == 0 && j == 0) {
                    continue;
                }
                if (this.octopi[y + i] && this.octopi[y + i][x + j]) {
                    neighbors.push({ x: x + j, y: y + i });
                }
            }
        }
        return neighbors;
    }

    private simulate(cycles: number): number {
        let count = 0;
        for (let i = 0; i < cycles; i++) {
            // this.printOctopi("\n");

            // First: increment all octopi
            for (let y = 0; y < this.height; y++) {
                for (let x = 0; x < this.width; x++) {
                    if (this.octopi[y][x] > 9) {
                        // Error catcher
                        throw new Error(`Octopus ${x},${y} has too much energy`);
                    } else {
                        this.octopi[y][x]++;
                    }
                }
            }

            // Second: find the flashers
            let flashStack = [];
            for (let y = 0; y < this.height; y++) {
                for (let x = 0; x < this.width; x++) {
                    if (this.octopi[y][x] > 9) {
                        flashStack.push({ x: x, y: y });
                        this.octopi[y][x] = 0;
                    }
                }
            }

            // Third: flash
            // let flashed = new Set(flashStack);
            while (flashStack.length > 0) {
                let flash = flashStack.pop();
                if (flash === undefined) {
                    throw new Error("Flash stack is empty");
                }

                count++;
                for (let neighbor of this.getNeighbors(flash.x, flash.y)) {
                    if (this.octopi[neighbor.y][neighbor.x] !== 0) {
                        this.octopi[neighbor.y][neighbor.x]++;
                    }

                    if (this.octopi[neighbor.y][neighbor.x] > 9 /* && !flashed.has(neighbor) */) {
                        flashStack.push(neighbor);
                        this.octopi[neighbor.y][neighbor.x] = 0;
                        // flashed.add(neighbor);
                    }
                }
            }
        }

        return count;
    }

    public solvePart1(): number {
        return this.simulate(100);
    }

    public solvePart2(): number {
        let cycles = 0;
        while (this.simulate(1) != this.width * this.height) {
            cycles++;
        }

        return cycles + 1;
    }
}

let sol = new Solution("inputs/d11.txt");
// console.log(`Part 1: ${sol.solvePart1()}`);
console.log(`Part 2: ${sol.solvePart2()}`);