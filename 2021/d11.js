"use strict";
exports.__esModule = true;
var fs_1 = require("fs");
var Solution = /** @class */ (function () {
    function Solution(filename) {
        this.input = (0, fs_1.readFileSync)(filename, "utf8");
        this.octopi = this.input.split("\r\n").map(function (line) {
            return line.split("").map(Number);
        });
        this.width = this.octopi[0].length;
        this.height = this.octopi.length;
    }
    Solution.prototype.printOctopi = function (s) {
        if (s === void 0) { s = ""; }
        console.log(this.octopi.map(function (line) { return line.join(""); }).join("\n") + s);
    };
    Solution.prototype.getNeighbors = function (x, y) {
        var neighbors = [];
        for (var i = -1; i <= 1; i++) {
            for (var j = -1; j <= 1; j++) {
                if (i == 0 && j == 0) {
                    continue;
                }
                if (this.octopi[y + i] && this.octopi[y + i][x + j]) {
                    neighbors.push({ x: x + j, y: y + i });
                }
            }
        }
        return neighbors;
    };
    Solution.prototype.simulate = function (cycles) {
        var count = 0;
        for (var i = 0; i < cycles; i++) {
            // this.printOctopi("\n");
            // First: increment all octopi
            for (var y = 0; y < this.height; y++) {
                for (var x = 0; x < this.width; x++) {
                    if (this.octopi[y][x] > 9) {
                        // Error catcher
                        throw new Error("Octopus ".concat(x, ",").concat(y, " has too much energy"));
                    }
                    else {
                        this.octopi[y][x]++;
                    }
                }
            }
            // Second: find the flashers
            var flashStack = [];
            for (var y = 0; y < this.height; y++) {
                for (var x = 0; x < this.width; x++) {
                    if (this.octopi[y][x] > 9) {
                        flashStack.push({ x: x, y: y });
                        this.octopi[y][x] = 0;
                    }
                }
            }
            // Third: flash
            // let flashed = new Set(flashStack);
            while (flashStack.length > 0) {
                var flash = flashStack.pop();
                if (flash === undefined) {
                    throw new Error("Flash stack is empty");
                }
                count++;
                for (var _i = 0, _a = this.getNeighbors(flash.x, flash.y); _i < _a.length; _i++) {
                    var neighbor = _a[_i];
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
    };
    Solution.prototype.solvePart1 = function () {
        return this.simulate(100);
    };
    Solution.prototype.solvePart2 = function () {
        var cycles = 0;
        while (this.simulate(1) != this.width * this.height) {
            cycles++;
        }
        return cycles;
    };
    return Solution;
}());
var sol = new Solution("inputs/d11ex.txt");
// console.log(`Part 1: ${sol.solvePart1()}`);
console.log("Part 2: ".concat(sol.solvePart2()));
