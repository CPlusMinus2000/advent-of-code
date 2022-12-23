"use strict";
exports.__esModule = true;
var fs_1 = require("fs");
/**
 *
 * @param {string} filename     The name of the file to read
 * @returns {number}            The gamma-epsilon product
 */
function threeOne(filename) {
    var input = (0, fs_1.readFileSync)(filename, "utf8");
    var lines = input.split("\n").map(function (line) { return line.trim(); });
    var counts = new Array(lines[0].length).fill(0);
    for (var i = 0; i < lines.length; i++) {
        var line = lines[i];
        for (var j = 0; j < line.length; j++) {
            counts[j] += +line[j];
        }
    }
    var gamma = "", epsilon = "";
    for (var i = 0; i < counts.length; i++) {
        gamma += counts[i] >= lines.length / 2 ? "1" : "0";
        epsilon += counts[i] < lines.length / 2 ? "1" : "0";
    }
    return parseInt(gamma, 2) * parseInt(epsilon, 2);
}
/**
 *
 * @param {string[]} binaryValues   The binary values to keep the most common of
 * @param {number}   index          The index of the value to check
 * @param {boolean}  common         Whether we want the most or least common
 * @returns {string[]}              The binary values with the most common value
 */
function keepValues(binaryValues, index, common) {
    console.assert(binaryValues.length > 0);
    console.assert(index >= 0);
    console.assert(index < binaryValues[0].length);
    var digitSum = binaryValues.map(function (binaryValue) { return +binaryValue[index]; }).reduce(function (sum, digit) { return sum + digit; }, 0);
    var mostCommon;
    if (common) {
        mostCommon = digitSum >= binaryValues.length / 2 ? "1" : "0";
    }
    else {
        mostCommon = digitSum < binaryValues.length / 2 ? "1" : "0";
    }
    return binaryValues.filter(function (binaryValue) { return binaryValue[index] === mostCommon; });
}
function threeTwo(filename) {
    var input = (0, fs_1.readFileSync)(filename, "utf8");
    var lines = input.split("\n").map(function (line) { return line.trim(); });
    var index1 = 0, index2 = 0;
    var oxygen = keepValues(lines, index1, true);
    var co2 = keepValues(lines, index2, false);
    index1++;
    index2++;
    while (oxygen.length > 1) {
        oxygen = keepValues(oxygen, index1, true);
        index1++;
    }
    while (co2.length > 1) {
        co2 = keepValues(co2, index2, false);
        index2++;
    }
    console.log(oxygen, co2);
    return parseInt(oxygen[0], 2) * parseInt(co2[0], 2);
}
console.log(threeOne("inputs/d3.txt"));
console.log(threeTwo("inputs/d3.txt"));
