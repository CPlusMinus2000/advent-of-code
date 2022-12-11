
const fs = require('fs');


type Open = '{' | '[' | '(' | '<';
type Close = '}' | ']' | ')' | '>';
type Bracket = Open | Close;

const OPEN = new Set<string>([ '{', '[', '(', '<' ]);
const scores = new Map<string, number>([
    [ ')', 3 ],
    [ ']', 57 ],
    [ '}', 1197 ],
    [ '>', 25137 ]
]);

const twoScores = new Map<string, number>([
    [ '(', 1 ],
    [ '[', 2 ],
    [ '{', 3 ],
    [ '<', 4 ]
]);


function bracketPair(bracket: string): string {
    switch (bracket) {
        case '}': return '{';
        case ']': return '[';
        case ')': return '(';
        case '>': return '<';
        default: return '';
    }
}

class Solution {
    public input: string;
    public lines: string[];

    constructor(filename: string) {
        this.input = fs.readFileSync(filename, 'utf-8');
        this.lines = this.input.split('\r\n');
    }

    public solvePart1(): number {
        let sum = 0;
        for (const line of this.lines) {
            let brackStack: string[] = [];
            for (const bracket of line) {

                if (OPEN.has(bracket)) {
                    brackStack.push(bracket);
                } else if (OPEN.has(bracketPair(bracket))) {
                    let b = brackStack.pop();
                    if (b !== bracketPair(bracket)) {
                        let score = scores.get(bracket);
                        if (score) {
                            sum += score;
                        }

                        break;
                    }
                }
            }
        }

        return sum;
    }

    public solvePart2(): number {
        let autocompletes: number[] = [];
        for (const line of this.lines) {
            let brackStack: string[] = [];
            for (const bracket of line) {
                if (OPEN.has(bracket)) {
                    brackStack.push(bracket);
                } else if (OPEN.has(bracketPair(bracket))) {
                    let b = brackStack.pop();
                    if (b !== bracketPair(bracket)) {
                        brackStack = [];
                        break;
                    }
                }
            }

            if (brackStack.length !== 0) {
                let score = 0;
                while (brackStack.length !== 0) {
                    score *= 5;
                    let b = brackStack.pop();
                    if (b) {
                        let val = twoScores.get(b);
                        if (val) {
                            score += val;
                        }
                    }
                }

                autocompletes.push(score);
            }
        }

        autocompletes.sort((a, b) => a - b);
        return autocompletes[(autocompletes.length - 1) / 2];
    }
}

let sol = new Solution('inputs/d10.txt');
console.log(`Part 1: ${sol.solvePart1()}`);
console.log(`Part 2: ${sol.solvePart2()}`);