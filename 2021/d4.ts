
import { readFileSync } from "fs";


type Square = [number, boolean];

/**
 * Bingo card class.
 */
class BingoCard {
    private squares: Square[][];
    private readonly width: number;
    private readonly height: number;

    constructor(input: string) {
        this.squares = [];

        let parsedInput = input.split("\r\n").map(row => {
            return row.split(" ").filter(x => x !== "");
        });

        this.width = parsedInput[0].length;
        this.height = parsedInput.length;

        for (let i = 0; i < this.height; i++) {
            this.squares[i] = [];
            for (let j = 0; j < this.width; j++) {
                this.squares[i][j] = [+parsedInput[i][j], false];
            }
        }
    }

    /**
     * Tries to find a square with the given number, and marks it true if found.
     * @param {number} number The number to find.
     * @returns {void}
     */
    public markSquare(number: number): void {
        for (let i = 0; i < this.height; i++) {
            for (let j = 0; j < this.width; j++) {
                if (this.squares[i][j][0] === number) {
                    this.squares[i][j][1] = true;
                }
            }
        }
    }

    /**
     * 
     * @returns {boolean} True if any of the columns have won, false otherwise.
     */
    private checkColumns(): boolean {
        for (let i = 0; i < this.width; i++) {
            let column = this.squares.map(row => row[i]);
            if (column.every(x => x[1])) {
                return true;
            }
        }

        return false;
    }

    /**
     * 
     * @returns {boolean} True if any of the rows have won, false otherwise.
     */
    private checkRows(): boolean {
        for (let i = 0; i < this.height; i++) {
            let row = this.squares[i];
            if (row.every(x => x[1])) {
                return true;
            }
        }
        
        return false;
    }

    /**
     * 
     * @returns {boolean} True if the card has won diagonally, false otherwise.
     */
    private checkDiagonals(): boolean {
        let leftToRight = this.squares.map((row, i) => row[i]);
        let rightToLeft = this.squares.map((row, i) => row[this.width - i - 1]);
        return leftToRight.every(x => x[1]) || rightToLeft.every(x => x[1]);
    }

    /**
     * Checks if the bingo card has won.
     * @returns {boolean} True if the card has won, false otherwise.
     */
    public hasWon(): boolean {
        return this.checkRows() || this.checkColumns();
    }

    /**
     * Returns the sum of unmarked values.
     * @returns {number} The sum of unmarked values.
     */
    public getUnmarkedSum(): number {
        return this.squares.reduce((sum, row) => {
            return sum + row.reduce((sum, square) => {
                return sum + (square[1] ? 0 : square[0]);
            }, 0);
        }, 0);
    }

    /**
     * Returns the string representation of the card.
     * @returns {string} The string representation of the card.
     */
    public toString(): string {
        let output = "";

        for (let i = 0; i < this.height; i++) {
            output += this.squares[i].map(x => {
                let num = x[0] >= 10 ? String(x[0]) : " " + x[0];
                let mark = x[1] ? "X" : " ";
                return num + mark;
            }).join(" ") + "\n";
        }

        return output;
    }
}

/**
 * Solution class for Day 4 of Advent of Code
 */
class Solution {
    input: string;
    lines: string[];
    draws: number[];
    cards: BingoCard[];

    /**
     * Constructor for the solution.
     * @param {string} path Path to the input file.
     */
    constructor(path: string) {
        this.input = readFileSync(path, "utf-8");
        this.lines = this.input.split("\r\n\r\n");
        this.draws = this.lines[0].split(',').map(x => +x);
        this.cards = this.lines.slice(1).map(x => new BingoCard(x));
    }

    /**
     * 
     * @returns {number} The number of winning boards.
     */
    public numWins(): number {
        return this.cards.filter(x => x.hasWon()).length;
    }

    /**
     * Plays out the bingo for part 1.
     * @returns {number} The score of the winning board.
     * @throws {Error} If the bingo has not been won by the end of the draws.
     */
    public part1(): number {
        for (let i = 0; i < this.draws.length; i++) {
            let draw = this.draws[i];
            for (let j = 0; j < this.cards.length; j++) {
                this.cards[j].markSquare(draw);
                if (this.cards[j].hasWon()) {
                    return draw * this.cards[j].getUnmarkedSum();
                }
            }
        }

        throw new Error("Bingo has not been won.");
    }

    /**
     * Plays out all the bingo cards, for part 2.
     * @returns {number} The score of the board which will win last.
     * @throws {Error} If there is more than one card by the end of the draws.
     */
    public part2(): number {
        let numCards = this.cards.length;
        let numWins = 0;
        for (let i = 0; i < this.draws.length; i++) {
            let draw = this.draws[i];
            for (let j = 0; j < this.cards.length; j++) {
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
    }
}

let sol = new Solution("inputs/d4.txt");
console.log("Part 1:", sol.part1());
console.log("Part 2:", sol.part2());