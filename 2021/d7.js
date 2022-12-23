"use strict";
exports.__esModule = true;
var fs_1 = require("fs");
var Solution = /** @class */ (function () {
    function Solution(filepath) {
        var input = (0, fs_1.readFileSync)(filepath, "utf-8");
        this.crabs = input.split(',').map(Number);
        this.minCrab = Math.min.apply(Math, this.crabs);
        this.maxCrab = Math.max.apply(Math, this.crabs);
    }
    Solution.prototype.solvePart1 = function () {
        var best = Infinity;
        var bestPos = 0;
        for (var i = this.minCrab; i <= this.maxCrab; i++) {
            var dist = 0;
            for (var _i = 0, _a = this.crabs; _i < _a.length; _i++) {
                var c = _a[_i];
                dist += Math.abs(c - i);
            }
            if (dist < best) {
                best = dist;
                bestPos = i;
            }
        }
        console.log("Bestpos: " + bestPos);
        return best;
    };
    Solution.prototype.solvePart1Fast = function () {
        var crabSum = this.crabs.reduce(function (a, b) { return a + b; }, 0);
        var bestPos = Math.round(crabSum / this.crabs.length);
        console.log("Bestpos: " + bestPos);
        return this.crabs.reduce(function (a, b) { return a + Math.abs(b - bestPos); }, 0);
    };
    Solution.prototype.solvePart2 = function () {
        var best = Infinity;
        for (var i = this.minCrab; i <= this.maxCrab; i++) {
            var dist = 0;
            for (var _i = 0, _a = this.crabs; _i < _a.length; _i++) {
                var c = _a[_i];
                var d = Math.abs(c - i);
                dist += d * (d + 1) / 2;
            }
            if (dist < best) {
                best = dist;
            }
        }
        return best;
    };
    return Solution;
}());
var sol = new Solution('inputs/d7.txt');
console.log(sol.solvePart1());
console.log(sol.solvePart1Fast());
console.log(sol.solvePart2());
