"use strict";
exports.__esModule = true;
var fs_1 = require("fs");
/**
 * Class for a hydrothermal line.
 */
var Hydrothermal = /** @class */ (function () {
    /**
     * Constructor for a hydrothermal line.
     * @param {Point} start The start point of the line.
     * @param {Point} end The end point of the line.
     */
    function Hydrothermal(start, end) {
        this.start = start;
        this.end = end;
        this.length = Math.sqrt(Math.pow(end.x - start.x, 2) + Math.pow(end.y - start.y, 2));
        if (end.x === start.x) {
            this.orientation = "V";
        }
        else if (end.y === start.y) {
            this.orientation = "H";
        }
        else {
            this.orientation = "D";
        }
    }
    return Hydrothermal;
}());
/**
 * Solution class for Day 5 of AoC.
 */
var Solution = /** @class */ (function () {
    /**
     * Constructor for the solution.
     * @param {string} input The input filename.
     */
    function Solution(input) {
        /**
         * The field of the lines.
         * @type {number[][]}
         */
        this.field = [];
        this.input = input;
        this.lines = (0, fs_1.readFileSync)(input, "utf8").split("\n").map(function (line) { return line.trim(); });
        this.hydrothermalLines = [];
        var maxX = 0, maxY = 0;
        for (var i = 0; i < this.lines.length; i++) {
            var line = this.lines[i];
            var parts = line.split(" -> ").map(function (part) { return part.split(','); });
            var start = { x: 0, y: 0 };
            var end = { x: 0, y: 0 };
            if (+parts[0][0] === +parts[1][0] || +parts[0][1] === +parts[1][1]) {
                var startX = Math.min(+parts[0][0], +parts[1][0]);
                var startY = Math.min(+parts[0][1], +parts[1][1]);
                var endX = Math.max(+parts[0][0], +parts[1][0]);
                var endY = Math.max(+parts[0][1], +parts[1][1]);
                start = { x: startX, y: startY };
                end = { x: endX, y: endY };
                maxX = Math.max(maxX, end.x);
                maxY = Math.max(maxY, end.y);
            }
            else if (+parts[0][0] < +parts[1][0] && +parts[0][1] < +parts[1][1]) {
                start = { x: +parts[0][0], y: +parts[0][1] };
                end = { x: +parts[1][0], y: +parts[1][1] };
                maxX = Math.max(maxX, end.x);
                maxY = Math.max(maxY, end.y);
            }
            else if (+parts[0][0] > +parts[1][0] && +parts[0][1] > +parts[1][1]) {
                start = { x: +parts[1][0], y: +parts[1][1] };
                end = { x: +parts[0][0], y: +parts[0][1] };
                maxX = Math.max(maxX, end.x);
                maxY = Math.max(maxY, end.y);
            }
            else {
                var startX = Math.min(+parts[0][0], +parts[1][0]);
                var startY = Math.max(+parts[0][1], +parts[1][1]);
                var endX = Math.max(+parts[0][0], +parts[1][0]);
                var endY = Math.min(+parts[0][1], +parts[1][1]);
                start = { x: startX, y: startY };
                end = { x: endX, y: endY };
                maxX = Math.max(maxX, end.x);
                maxY = Math.max(maxY, end.y);
            }
            this.hydrothermalLines.push(new Hydrothermal(start, end));
        }
        this.field = new Array(maxX + 1);
        for (var i = 0; i < this.field.length; i++) {
            this.field[i] = new Array(maxY + 1);
            for (var j = 0; j < this.field[i].length; j++) {
                this.field[i][j] = 0;
            }
        }
    }
    /**
     *
     * @returns {string} The field as a string.
     */
    Solution.prototype.fieldString = function () {
        var s = "";
        for (var i = 0; i < this.field.length; i++) {
            for (var j = 0; j < this.field[i].length; j++) {
                if (this.field[i][j] > 1) {
                    s += "X";
                }
                else {
                    s += this.field[i][j];
                }
            }
            s += "\n";
        }
        return s;
    };
    /**
     * Solve part 1.
     * @return {number} The solution to part 1.
     */
    Solution.prototype.part1 = function () {
        for (var i = 0; i < this.hydrothermalLines.length; i++) {
            var line = this.hydrothermalLines[i];
            if (line.orientation !== "D") {
                for (var j = line.start.y; j <= line.end.y; j++) {
                    for (var k = line.start.x; k <= line.end.x; k++) {
                        this.field[j][k] += 1;
                    }
                }
            }
        }
        var count = 0;
        for (var i = 0; i < this.field.length; i++) {
            for (var j = 0; j < this.field[i].length; j++) {
                if (this.field[i][j] > 1) {
                    count++;
                }
            }
        }
        return count;
    };
    /**
     * Solve part 2.
     * @return {number} The solution to part 2.
     */
    Solution.prototype.part2 = function () {
        for (var i = 0; i < this.hydrothermalLines.length; i++) {
            var line = this.hydrothermalLines[i];
            if (line.orientation === "D") {
                if (line.end.x > line.start.x && line.end.y > line.start.y) {
                    for (var j = 0; j <= line.end.y - line.start.y; j++) {
                        this.field[line.start.y + j][line.start.x + j] += 1;
                    }
                }
                else {
                    for (var j = 0; j <= line.start.y - line.end.y; j++) {
                        this.field[line.start.y - j][line.start.x + j] += 1;
                    }
                }
            }
        }
        var count = 0;
        for (var i = 0; i < this.field.length; i++) {
            for (var j = 0; j < this.field[i].length; j++) {
                if (this.field[i][j] > 1) {
                    count++;
                }
            }
        }
        return count;
    };
    return Solution;
}());
var sol = new Solution("inputs/d5ex.txt");
console.log("Part 1: " + sol.part1());
console.log("Part 2: " + sol.part2());
