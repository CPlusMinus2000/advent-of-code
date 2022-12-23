
import { readFileSync } from "fs";

type Point = {
    x: number;
    y: number;
}

type orientation = "H" | "V" | "D";

/**
 * Class for a hydrothermal line.
 */
class Hydrothermal {
    /**
     * The start point of the line.
     * @type {Point}
     */
    start: Point;

    /**
     * The end point of the line.
     * @type {Point}
     */
    end: Point;

    /**
     * The length of the line.
     * @type {number}
     */
    length: number;

    /**
     * The orientation of the line.
     * @type {orientation}
     */
    orientation: orientation;

    /**
     * Constructor for a hydrothermal line.
     * @param {Point} start The start point of the line.
     * @param {Point} end The end point of the line.
     */
    constructor(start: Point, end: Point) {
        this.start = start;
        this.end = end;
        this.length = Math.sqrt(Math.pow(end.x - start.x, 2) + Math.pow(end.y - start.y, 2));
        if (end.x === start.x) {
            this.orientation = "V";
        } else if (end.y === start.y) {
            this.orientation = "H";
        } else {
            this.orientation = "D";
        }
    }
}

/**
 * Solution class for Day 5 of AoC.
 */
class Solution {
    /**
     * The input file.
     * @type {string}
     */
    private input: string;

    /**
     * The list of lines.
     * @type {string}
     */
    private lines: string[];

    /**
     * The list of hydrothermal lines.
     * @type {Hydrothermal[]}
     */
    private hydrothermalLines: Hydrothermal[];

    /**
     * The field of the lines.
     * @type {number[][]}
     */
    private field: number[][] = [];

    /**
     * Constructor for the solution.
     * @param {string} input The input filename.
     */
    constructor(input: string) {
        this.input = input;
        this.lines = readFileSync(input, "utf8").split("\n").map(line => line.trim());
        this.hydrothermalLines = [];

        let maxX = 0, maxY = 0;
        for (let i = 0; i < this.lines.length; i++) {
            let line = this.lines[i];
            let parts = line.split(" -> ").map(part => part.split(','));
            let start = { x: 0, y: 0 };
            let end = { x: 0, y: 0 };

            if (+parts[0][0] === +parts[1][0] || +parts[0][1] === +parts[1][1]) {
                let startX = Math.min(+parts[0][0], +parts[1][0]);
                let startY = Math.min(+parts[0][1], +parts[1][1]);
                let endX = Math.max(+parts[0][0], +parts[1][0]);
                let endY = Math.max(+parts[0][1], +parts[1][1]);
                start = { x: startX, y: startY };
                end = { x: endX, y: endY };

                maxX = Math.max(maxX, end.x);
                maxY = Math.max(maxY, end.y);
            } else if (+parts[0][0] < +parts[1][0] && +parts[0][1] < +parts[1][1]) {
                start = { x: +parts[0][0], y: +parts[0][1] };
                end = { x: +parts[1][0], y: +parts[1][1] };
                
                maxX = Math.max(maxX, end.x);
                maxY = Math.max(maxY, end.y);
            } else if (+parts[0][0] > +parts[1][0] && +parts[0][1] > +parts[1][1]) {
                start = { x: +parts[1][0], y: +parts[1][1] };
                end = { x: +parts[0][0], y: +parts[0][1] };

                maxX = Math.max(maxX, end.x);
                maxY = Math.max(maxY, end.y);
            } else {
                let startX = Math.min(+parts[0][0], +parts[1][0]);
                let startY = Math.max(+parts[0][1], +parts[1][1]);
                let endX = Math.max(+parts[0][0], +parts[1][0]);
                let endY = Math.min(+parts[0][1], +parts[1][1]);

                start = { x: startX, y: startY };
                end = { x: endX, y: endY };

                maxX = Math.max(maxX, end.x);
                maxY = Math.max(maxY, end.y);
            }

            this.hydrothermalLines.push(new Hydrothermal(start, end));
        }

        this.field = new Array(maxX + 1);
        for (let i = 0; i < this.field.length; i++) {
            this.field[i] = new Array(maxY + 1);
            for (let j = 0; j < this.field[i].length; j++) {
                this.field[i][j] = 0;
            }
        } 
    }

    /**
     * 
     * @returns {string} The field as a string.
     */
    fieldString(): string {
        let s = "";
        for (let i = 0; i < this.field.length; i++) {
            for (let j = 0; j < this.field[i].length; j++) {
                if (this.field[i][j] > 1) {
                    s += "X";
                } else {
                    s += this.field[i][j];
                }
            }
            s += "\n";
        }
        return s;
    }

    /**
     * Solve part 1.
     * @return {number} The solution to part 1.
     */
    part1(): number {
        for (let i = 0; i < this.hydrothermalLines.length; i++) {
            let line = this.hydrothermalLines[i];
            if (line.orientation !== "D") {
                for (let j = line.start.y; j <= line.end.y; j++) {
                    for (let k = line.start.x; k <= line.end.x; k++) {
                        this.field[j][k] += 1;
                    }
                }
            }
        }

        let count = 0;
        for (let i = 0; i < this.field.length; i++) {
            for (let j = 0; j < this.field[i].length; j++) {
                if (this.field[i][j] > 1) {
                    count++;
                }
            }
        }

        return count;
    }

    /**
     * Solve part 2.
     * @return {number} The solution to part 2.
     */
    part2(): number {
        for (let i = 0; i < this.hydrothermalLines.length; i++) {
            let line = this.hydrothermalLines[i];
            if (line.orientation === "D") {
                if (line.end.x > line.start.x && line.end.y > line.start.y) {
                    for (let j = 0; j <= line.end.y - line.start.y; j++) {
                        this.field[line.start.y + j][line.start.x + j] += 1;
                    }
                } else {
                    for (let j = 0; j <= line.start.y - line.end.y; j++) {
                        this.field[line.start.y - j][line.start.x + j] += 1;
                    }
                }
            }
        }

        let count = 0;
        for (let i = 0; i < this.field.length; i++) {
            for (let j = 0; j < this.field[i].length; j++) {
                if (this.field[i][j] > 1) {
                    count++;
                }
            }
        }

        return count;
    }
}

let sol = new Solution("inputs/d5.txt");
console.log("Part 1: " + sol.part1());
console.log("Part 2: " + sol.part2());