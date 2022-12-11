"use strict";
// Day 8, Advent of Code.
exports.__esModule = true;
var fs_1 = require("fs");
var unique = [2, 3, 4, 7];
var letters = ["a", "b", "c", "d", "e", "f", "g"];
var parser = new Map();
parser.set("abcefg", 0);
parser.set("cf", 1);
parser.set("acdeg", 2);
parser.set("acdfg", 3);
parser.set("bcdf", 4);
parser.set("abdfg", 5);
parser.set("abdefg", 6);
parser.set("acf", 7);
parser.set("abcdefg", 8);
parser.set("abcdfg", 9);
var Solution = /** @class */ (function () {
    function Solution(filepath) {
        this.input = (0, fs_1.readFileSync)(filepath, 'utf-8');
        this.lines = this.input.split('\n').map(function (line) { return line.trim(); });
        this.entries = this.lines.map(function (line) {
            var _a = line.split(' | ').map(function (part) { return part.split(' '); }), pattern = _a[0], output = _a[1];
            if (pattern.length !== 10) {
                throw new Error('Invalid pattern length');
            }
            else if (output.length !== 4) {
                throw new Error('Invalid output length');
            }
            return [pattern, output];
        });
    }
    Solution.prototype.solvePart1 = function () {
        var count = 0;
        var otherCount = 0;
        for (var _i = 0, _a = this.entries; _i < _a.length; _i++) {
            var ent = _a[_i];
            var pattern = ent[0], output = ent[1];
            for (var _b = 0, output_1 = output; _b < output_1.length; _b++) {
                var out = output_1[_b];
                if (unique.includes(out.length)) {
                    count++;
                }
                else {
                    otherCount++;
                }
            }
        }
        console.log(otherCount);
        return count;
    };
    Solution.prototype.solvePart2 = function () {
        var total = 0;
        var _loop_1 = function (ent) {
            var pattern = ent[0], output = ent[1];
            var one = pattern.filter(function (p) { return p.length === 2; })[0];
            var sev = pattern.filter(function (p) { return p.length === 3; })[0];
            var fur = pattern.filter(function (p) { return p.length === 4; })[0];
            var eit = pattern.filter(function (p) { return p.length === 7; })[0];
            var perm = {};
            // There should only be one line in sev that's not in one
            perm.a = sev.split('').filter(function (c) { return !one.includes(c); })[0];
            // Get the
            //   |
            //  -
            // |
            // from the pattern using 8, 6, 0, and 9
            var sixes = pattern.filter(function (p) { return p.length === 6; }).map(function (p) {
                for (var _i = 0, letters_1 = letters; _i < letters_1.length; _i++) {
                    var l = letters_1[_i];
                    if (!p.includes(l)) {
                        return l;
                    }
                }
            });
            // c should be the intersection with sixes and one
            perm.c = one.split('').filter(function (c) { return sixes.includes(c); })[0];
            // d should be the other one
            perm.d = fur.split('').filter(function (c) {
                return !one.includes(c) && sixes.includes(c);
            })[0];
            // e should be the last one
            var e = sixes.filter(function (c) {
                return c !== perm.c && c !== perm.d;
            })[0];
            if (e === undefined) {
                throw new Error('No e');
            }
            perm.e = e;
            // b should be the only one in fur not in sixes or one
            perm.b = fur.split('').filter(function (c) {
                return !sixes.includes(c) && !one.includes(c);
            })[0];
            // f should be the only one in one not in sixes
            perm.f = one.split('').filter(function (c) {
                return !sixes.includes(c);
            })[0];
            // g should be the last
            perm.g = letters.filter(function (c) {
                return !Object.values(perm).includes(c);
            })[0];
            // Invert perm, because I am not very smart
            var inv = {};
            for (var key in perm) {
                inv[perm[key]] = key;
            }
            perm = inv;
            // Now we can finally decode the output
            var decoded = output.map(function (out) {
                return out.split('').map(function (c) {
                    return perm[c];
                }).sort().join('');
            });
            var partial = decoded.map(function (d) { return parser.get(d); });
            var num = +partial.join('');
            console.log(perm);
            console.log(decoded, partial, num);
            total += num;
        };
        for (var _i = 0, _a = this.entries; _i < _a.length; _i++) {
            var ent = _a[_i];
            _loop_1(ent);
        }
        return total;
    };
    return Solution;
}());
var sol = new Solution("inputs/d8.txt");
console.log("Part 1: ".concat(sol.solvePart1()));
console.log("Part 2: ".concat(sol.solvePart2()));
