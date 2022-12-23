// Day 8, Advent of Code.

import { readFileSync } from 'fs';

type pattern = string[];
type output = string[];
type entry = [pattern, output];

interface permutation {
    [key: string]: string;
}

const unique = [2, 3, 4, 7];
const letters = ["a", "b", "c", "d", "e", "f", "g"];

let parser = new Map<string, number>();
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

class Solution {
    public input: string;
    public lines: string[];
    public entries: entry[];

    constructor(filepath: string) {
        this.input = readFileSync(filepath, 'utf-8');
        this.lines = this.input.split('\n').map(line => line.trim());
        this.entries = this.lines.map(line => {
            const [pattern, output] = line.split(' | ').map(part => part.split(' '));
            if (pattern.length !== 10) {
                throw new Error('Invalid pattern length');
            } else if (output.length !== 4) {
                throw new Error('Invalid output length');
            }

            return [pattern, output];
        });
    }
    
    public solvePart1(): number {
        let count = 0;
        let otherCount = 0;
        for (const ent of this.entries) {
            const [pattern, output] = ent;
            for (const out of output) {
                if (unique.includes(out.length)) {
                    count++;
                } else {
                    otherCount++;
                }
            }
        }

        console.log(otherCount);
        return count;
    }

    public solvePart2(): number {
        let total = 0;
        for (const ent of this.entries) {
            const [pattern, output] = ent;
            const one = pattern.filter(p => p.length === 2)[0];
            const sev = pattern.filter(p => p.length === 3)[0];
            const fur = pattern.filter(p => p.length === 4)[0];
            const eit = pattern.filter(p => p.length === 7)[0];

            let perm: permutation = {};

            // There should only be one line in sev that's not in one
            perm.a = sev.split('').filter(c => !one.includes(c))[0];

            // Get the
            //   |
            //  -
            // |
            // from the pattern using 8, 6, 0, and 9
            const sixes = pattern.filter(p => p.length === 6).map(p => {
                for (const l of letters) {
                    if (!p.includes(l)) {
                        return l;
                    }
                }
            });

            // c should be the intersection with sixes and one
            perm.c = one.split('').filter(c => sixes.includes(c))[0];

            // d should be the other one
            perm.d = fur.split('').filter(c => {
                return !one.includes(c) && sixes.includes(c);
            })[0];

            // e should be the last one
            let e = sixes.filter(c => {
                return c !== perm.c && c !== perm.d;
            })[0];

            if (e === undefined) {
                throw new Error('No e');
            }

            perm.e = e;

            // b should be the only one in fur not in sixes or one
            perm.b = fur.split('').filter(c => {
                return !sixes.includes(c) && !one.includes(c);
            })[0];

            // f should be the only one in one not in sixes
            perm.f = one.split('').filter(c => {
                return !sixes.includes(c);
            })[0];

            // g should be the last
            perm.g = letters.filter(c => {
                return !Object.values(perm).includes(c);
            })[0];

            // Invert perm, because I am not very smart
            let inv: permutation = {};
            for (const key in perm) {
                inv[perm[key]] = key;
            }

            perm = inv;

            // Now we can finally decode the output
            let decoded = output.map(out => {
                return out.split('').map(c => {
                    return perm[c];
                }).sort().join('');
            });

            let partial = decoded.map(d => parser.get(d));
            let num = +partial.join('');
            console.log(perm);
            console.log(decoded, partial, num);
            total += num;

        }

        return total;
    }
}

let sol = new Solution("inputs/d8.txt");
console.log(`Part 1: ${sol.solvePart1()}`);
console.log(`Part 2: ${sol.solvePart2()}`);
