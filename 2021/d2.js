"use strict";
exports.__esModule = true;
var fs_1 = require("fs");
function twoOne() {
    var input = (0, fs_1.readFileSync)("inputs/d2.txt", "utf8");
    var pos = 0, depth = 0;
    for (var _i = 0, _a = input.split("\n"); _i < _a.length; _i++) {
        var line = _a[_i];
        var _b = line.split(" "), a = _b[0], b = _b[1];
        if (a === "forward") {
            pos += +b;
        }
        else if (a === "up") {
            depth -= +b;
        }
        else if (a === "down") {
            depth += +b;
        }
    }
    console.log(pos * depth);
}
function twoTwo() {
    var input = (0, fs_1.readFileSync)("inputs/d2.txt", "utf8");
    var pos = 0, depth = 0, aim = 0;
    for (var _i = 0, _a = input.split("\n"); _i < _a.length; _i++) {
        var line = _a[_i];
        var _b = line.split(" "), a = _b[0], b = _b[1];
        if (a === "forward") {
            pos += +b;
            depth += +b * aim;
        }
        else if (a === "up") {
            aim -= +b;
        }
        else if (a === "down") {
            aim += +b;
        }
    }
    console.log(pos * depth);
}
twoOne();
twoTwo();
