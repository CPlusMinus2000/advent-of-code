
import { readFileSync } from "fs";

type Graph = { [key: string]: string[] };
type Visited2 = { [key: string]: boolean | string };

class Solution {
    public input: string;
    public lines: string[];
    public graph: Graph;

    constructor(filename: string) {
        this.input = readFileSync(filename, "utf8");
        this.lines = this.input.split("\r\n");
        this.graph = {};
        for (let i = 0; i < this.lines.length; i++) {
            const line = this.lines[i];
            const [a, b] = line.split("-");
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

    public dfs(
        graph: Graph,
        v: string, currPath: string[],
        smallVisited: Visited2,
        except: boolean = false
    ): number {
        if ((!except && smallVisited[v]) || (except && smallVisited[v] && (smallVisited.except || v === "start"))) {
            return 0;
        } else if (v === "end") {
            return 1;
        }

        if (v === v.toLowerCase()) {
            if (except && smallVisited[v]) {
                smallVisited.except = v;
            }

            smallVisited[v] = true;
        }

        currPath.push(v);
        let total = 0;
        for (let i = 0; i < graph[v].length; i++) {
            const successor = graph[v][i];
            total += this.dfs(graph, successor, currPath, smallVisited, except);
        }

        currPath.pop();
        if (except && smallVisited.except === v) {
            delete smallVisited.except;
        } else {
            smallVisited[v] = false;
        }
        return total;
    } 

    public solvePart1(): number {
        let currPath: string[] = [];
        let smallVisited = {} as Visited2;

        return this.dfs(this.graph, "start", currPath, smallVisited);
    }

    public solvePart2(): number {
        let currPath: string[] = [];
        let smallVisited = {} as Visited2;

        return this.dfs(this.graph, "start", currPath, smallVisited, true);
    }
}

let sol = new Solution("inputs/d12.txt");
console.log(`Part 1: ${sol.solvePart1()}`);
console.log(`Part 2: ${sol.solvePart2()}`);