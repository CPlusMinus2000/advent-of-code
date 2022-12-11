
import { readFileSync } from "fs";

function twoOne() {
    const input = readFileSync("inputs/d2.txt", "utf8");
    let pos = 0, depth = 0;
    for (const line of input.split("\n")) {
        const [a, b] = line.split(" ");
        if (a === "forward") {
            pos += +b;
        } else if (a === "up") {
            depth -= +b;
        } else if (a === "down") {
            depth += +b;
        }
    }

    console.log(pos * depth);
}

function twoTwo() {
    const input = readFileSync("inputs/d2.txt", "utf8");
    let pos = 0, depth = 0, aim = 0;
    for (const line of input.split("\n")) {
        const [a, b] = line.split(" ");
        if (a === "forward") {
            pos += +b;
            depth += +b * aim;
        } else if (a === "up") {
            aim -= +b;
        } else if (a === "down") {
            aim += +b;
        }
    }

    console.log(pos * depth);
}

twoOne();
twoTwo();
