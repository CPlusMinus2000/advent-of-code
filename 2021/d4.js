"use strict";
exports.__esModule = true;
var fs_1 = require("fs");
/**
 * Bingo card class.
 */
var BingoCard = /** @class */ (function () {
    function BingoCard(input) {
        this.squares = [];
        var parsedInput = input.split("\r\n").map(function (row) {
            return row.split(" ").filter(function (x) { return x !== ""; });
        });
        this.width = parsedInput[0].length;
        this.height = parsedInput.length;
        for (var i = 0; i < this.height; i++) {
            this.squares[i] = [];
            for (var j = 0; j < this.width; j++) {
                this.squares[i][j] = [+parsedInput[i][j], false];
            }
        }
    }
    /**
     * Tries to find a square with the given number, and marks it true if found.
     * @param {number} number The number to find.
     * @returns {void}
     */
    BingoCard.prototype.markSquare = function (number) {
        for (var i = 0; i < this.height; i++) {
            for (var j = 0; j < this.width; j++) {
                if (this.squares[i][j][0] === number) {
                    this.squares[i][j][1] = true;
                }
            }
        }
    };
    /**
     *
     * @returns {boolean} True if any of the columns have won, false otherwise.
     */
    BingoCard.prototype.checkColumns = function () {
        var _loop_1 = function (i) {
            var column = this_1.squares.map(function (row) { return row[i]; });
            if (column.every(function (x) { return x[1]; })) {
                return { value: true };
            }
        };
        var this_1 = this;
        for (var i = 0; i < this.width; i++) {
            var state_1 = _loop_1(i);
            if (typeof state_1 === "object")
                return state_1.value;
        }
        return false;
    };
    /**
     *
     * @returns {boolean} True if any of the rows have won, false otherwise.
     */
    BingoCard.prototype.checkRows = function () {
        for (var i = 0; i < this.height; i++) {
            var row = this.squares[i];
            if (row.every(function (x) { return x[1]; })) {
                return true;
            }
        }
        return false;
    };
    /**
     *
     * @returns {boolean} True if the card has won diagonally, false otherwise.
     */
    BingoCard.prototype.checkDiagonals = function () {
        var _this = this;
        var leftToRight = this.squares.map(function (row, i) { return row[i]; });
        var rightToLeft = this.squares.map(function (row, i) { return row[_this.width - i - 1]; });
        return leftToRight.every(function (x) { return x[1]; }) || rightToLeft.every(function (x) { return x[1]; });
    };
    /**
     * Checks if the bingo card has won.
     * @returns {boolean} True if the card has won, false otherwise.
     */
    BingoCard.prototype.hasWon = function () {
        return this.checkRows() || this.checkColumns();
    };
    /**
     * Returns the sum of unmarked values.
     * @returns {number} The sum of unmarked values.
     */
    BingoCard.prototype.getUnmarkedSum = function () {
        return this.squares.reduce(function (sum, row) {
            return sum + row.reduce(function (sum, square) {
                return sum + (square[1] ? 0 : square[0]);
            }, 0);
        }, 0);
    };
    /**
     * Returns the string representation of the card.
     * @returns {string} The string representation of the card.
     */
    BingoCard.prototype.toString = function () {
        var output = "";
        for (var i = 0; i < this.height; i++) {
            output += this.squares[i].map(function (x) {
                var num = x[0] >= 10 ? String(x[0]) : " " + x[0];
                var mark = x[1] ? "X" : " ";
                return num + mark;
            }).join(" ") + "\n";
        }
        return output;
    };
    return BingoCard;
}());
/**
 * Solution class for Day 4 of Advent of Code
 */
var Solution = /** @class */ (function () {
    /**
     * Constructor for the solution.
     * @param {string} path Path to the input file.
     */
    function Solution(path) {
        this.input = (0, fs_1.readFileSync)(path, "utf-8");
        this.lines = this.input.split("\r\n\r\n");
        this.draws = this.lines[0].split(',').map(function (x) { return +x; });
        this.cards = this.lines.slice(1).map(function (x) { return new BingoCard(x); });
    }
    /**
     *
     * @returns {number} The number of winning boards.
     */
    Solution.prototype.numWins = function () {
        return this.cards.filter(function (x) { return x.hasWon(); }).length;
    };
    /**
     * Plays out the bingo for part 1.
     * @returns {number} The score of the winning board.
     * @throws {Error} If the bingo has not been won by the end of the draws.
     */
    Solution.prototype.part1 = function () {
        for (var i = 0; i < this.draws.length; i++) {
            var draw = this.draws[i];
            for (var j = 0; j < this.cards.length; j++) {
                this.cards[j].markSquare(draw);
                if (this.cards[j].hasWon()) {
                    return draw * this.cards[j].getUnmarkedSum();
                }
            }
        }
        throw new Error("Bingo has not been won.");
    };
    /**
     * Plays out all the bingo cards, for part 2.
     * @returns {number} The score of the board which will win last.
     * @throws {Error} If there is more than one card by the end of the draws.
     */
    Solution.prototype.part2 = function () {
        var numCards = this.cards.length;
        var numWins = 0;
        for (var i = 0; i < this.draws.length; i++) {
            var draw = this.draws[i];
            for (var j = 0; j < this.cards.length; j++) {
                if (this.cards[j].hasWon()) {
                    continue;
                }
                this.cards[j].markSquare(draw);
                if (this.numWins() === numCards) {
                    return draw * this.cards[j].getUnmarkedSum();
                }
            }
        }
        console.log(this.numWins());
        throw new Error("Bingo has not been won.");
    };
    return Solution;
}());
var sol = new Solution("inputs/d4.txt");
console.log("Part 1:", sol.part1());
console.log("Part 2:", sol.part2());
