"use strict";
exports.__esModule = true;
var fs_1 = require("fs");
var Solution = /** @class */ (function () {
    function Solution(filename) {
        this.input = (0, fs_1.readFileSync)(filename, "utf8");
        this.lines = this.input.split("\r\n");
        this.graph = {};
        for (var i = 0; i < this.lines.length; i++) {
            var line = this.lines[i];
            var _a = line.split("-"), a = _a[0], b = _a[1];
            if (!this.graph[a]) {
                this.graph[a] = [];
            }
            if (!this.graph[b]) {
                this.graph[b] = [];
            }
            this.graph[a].push(b);
            this.graph[b].push(a);
        }
    }
    Solution.prototype.dfs = function (graph, v, currPath, smallVisited, except) {
        if (except === void 0) { except = false; }
        if ((!except && smallVisited[v]) || (except && smallVisited[v] && (smallVisited.except || v === "start"))) {
            return 0;
        }
        else if (v === "end") {
            return 1;
        }
        if (v === v.toLowerCase()) {
            if (except && smallVisited[v]) {
                smallVisited.except = v;
            }
            smallVisited[v] = true;
        }
        currPath.push(v);
        var total = 0;
        for (var i = 0; i < graph[v].length; i++) {
            var successor = graph[v][i];
            total += this.dfs(graph, successor, currPath, smallVisited, except);
        }
        currPath.pop();
        if (except && smallVisited.except === v) {
            delete smallVisited.except;
        }
        else {
            smallVisited[v] = false;
        }
        return total;
    };
    Solution.prototype.solvePart1 = function () {
        var currPath = [];
        var smallVisited = {};
        return this.dfs(this.graph, "start", currPath, smallVisited);
    };
    Solution.prototype.solvePart2 = function () {
        var currPath = [];
        var smallVisited = {};
        return this.dfs(this.graph, "start", currPath, smallVisited, true);
    };
    return Solution;
}());
var sol = new Solution("inputs/d12ex.txt");
console.log("Part 1: ".concat(sol.solvePart1()));
console.log("Part 2: ".concat(sol.solvePart2()));
