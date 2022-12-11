"use strict";
exports.__esModule = true;
var fs_1 = require("fs");
var Solution = /** @class */ (function () {
    function Solution(filename) {
        this.input = (0, fs_1.readFileSync)(filename, "utf-8");
        this.lines = this.input.split("\n").map(function (line) { return line.trim(); });
        this.heightMap = this.lines.map(function (line) { return line.split("").map(Number); });
        this.width = this.heightMap[0].length;
        this.length = this.heightMap.length;
    }
    Solution.prototype.getAdjacent = function (p) {
        var points = [];
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
    };
    Solution.prototype.findLowests = function () {
        var _this = this;
        var lowests = [];
        for (var y = 0; y < this.length; y++) {
            var _loop_1 = function (x) {
                var current = this_1.heightMap[y][x];
                var adjacent = this_1.getAdjacent({ x: x, y: y }).map(function (p) { return _this.heightMap[p.y][p.x]; });
                if (adjacent.every(function (a) { return a > current; })) {
                    lowests.push({ x: x, y: y });
                }
            };
            var this_1 = this;
            for (var x = 0; x < this.width; x++) {
                _loop_1(x);
            }
        }
        return lowests;
    };
    Solution.prototype.solvePart1 = function () {
        var _this = this;
        var lowests = this.findLowests();
        var lowSum = lowests.reduce(function (sum, p) { return sum + _this.heightMap[p.y][p.x]; }, 0);
        return lowests.length + lowSum;
    };
    Solution.prototype.solvePart2 = function () {
        var basinSizes = [];
        var lowests = this.findLowests();
        for (var _i = 0, lowests_1 = lowests; _i < lowests_1.length; _i++) {
            var lowest = lowests_1[_i];
            var stack = [lowest];
            var visited = new Set(["".concat(lowest.x, ",").concat(lowest.y)]);
            var size = 1;
            while (stack.length > 0) {
                var current = stack.pop();
                if (current === undefined) {
                    continue;
                }
                var adjacent = this.getAdjacent(current);
                for (var _a = 0, adjacent_1 = adjacent; _a < adjacent_1.length; _a++) {
                    var adj = adjacent_1[_a];
                    var adjHeight = this.heightMap[adj.y][adj.x];
                    if (adjHeight > this.heightMap[current.y][current.x] &&
                        adjHeight !== 9 && !visited.has("".concat(adj.x, ",").concat(adj.y))) {
                        stack.push(adj);
                        visited.add("".concat(adj.x, ",").concat(adj.y));
                        size++;
                    }
                }
            }
            basinSizes.push(size);
        }
        basinSizes.sort(function (a, b) { return b - a; });
        return basinSizes[0] * basinSizes[1] * basinSizes[2];
    };
    return Solution;
}());
var sol = new Solution("inputs/d9.txt");
console.log("Part 1: ".concat(sol.solvePart1()));
console.log("Part 2: ".concat(sol.solvePart2()));
