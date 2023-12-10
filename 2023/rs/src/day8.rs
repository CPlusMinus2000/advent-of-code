use num_integer;
use std::collections::HashMap;
use std::fs::File;
use std::io::{BufRead, BufReader};

fn read_input(fname: &str) -> Vec<String> {
    let file = File::open(fname).expect("Failed to open file");
    let reader = BufReader::new(file);
    let mut lines = reader.lines();
    let mut input = Vec::new();

    while let Some(line) = lines.next() {
        input.push(line.expect("Failed to read line"));
    }

    input
}

fn parse_input(input: Vec<String>) -> (Vec<char>, HashMap<String, HashMap<char, String>>) {
    let mut turns = Vec::new();
    let mut rules = HashMap::new();

    for char in input[0].chars() {
        turns.push(char);
    }

    for rule in input[2..].iter() {
        let mut dir_map = HashMap::new();
        let mut split = rule.split(" = ");
        let key = split.next().unwrap().to_string();
        let rest = split.next().unwrap().to_string();
        let left = rest
            .split(", ")
            .next()
            .unwrap()
            .replace("(", "")
            .to_string();
        let right = rest
            .split(", ")
            .last()
            .unwrap()
            .replace(")", "")
            .to_string();

        let ll: char = 'L';
        let rr: char = 'R';
        dir_map.insert(ll, left);
        dir_map.insert(rr, right);
        rules.insert(key, dir_map);
    }

    (turns, rules)
}

fn dist_to_end(
    node: &str,
    turns: Vec<char>,
    rules: &HashMap<String, HashMap<char, String>>,
) -> usize {
    let mut curr = node.to_string();
    let mut steps = 0;
    while !curr.ends_with("Z") {
        let turn = turns[steps % turns.len()];
        curr = rules.get(&curr).unwrap().get(&turn).unwrap().to_string();
        steps += 1;
    }

    steps
}

pub fn part1() {
    let fname = "../data/day8.txt";
    let input = read_input(fname);
    let (turns, rules) = parse_input(input);

    let steps = dist_to_end("AAA", turns, &rules);
    println!("Part 1: {}", steps);
}

pub fn part2_long() {
    let fname = "../data/day8.txt";
    let input = read_input(fname);
    let (turns, rules) = parse_input(input);

    // Try running this by brute force?
    let mut nodes = Vec::new();
    for start_node in rules.keys().filter(|k| k.ends_with("A")) {
        nodes.push(start_node.clone());
    }

    let mut steps = 0;
    while !nodes.iter().all(|n: &String| n.ends_with("Z")) {
        let mut next_nodes = Vec::new();
        let turn = turns[steps % turns.len()];
        for node in &nodes[..] {
            next_nodes.push(rules.get(node).unwrap().get(&turn).unwrap().to_string());
        }

        steps += 1;
        if steps % 1000000 == 0 {
            println!("Finished running {} steps...", steps);
        }

        nodes = next_nodes;
    }

    println!("Part 2: {}", steps);
}

// pub fn part2_insane() {
//     let fname = "../data/day8.txt";
//     let input = read_input(fname);
//     let (turns, rules) = parse_input(input);

//     // Alright, this is going to be really complicated. Basically,
//     // for every possible "agent", we need to figure out three quantities:
//     // 1. Distance to the first 'Z' node,
//     // 2. Number of steps until they end up back at that node
//     //  AT the same step in the step list, and
//     // 3. Distances to Z nodes encountered along the way.
//     // Ready? Let's go crazy.
//     let start_nodes = rules.keys().filter(|k| k.ends_with("A"));
//     let mut cycle_sizes: HashMap<String, usize> = HashMap::new();
//     let mut distances_to_ends: HashMap<String, HashSet<usize, bool>> = HashMap::new();
//     for start in start_nodes {
//         let mut visited: HashSet<(String, bool)> = HashSet::new();
//         let mut steps = 0;
//         let mut curr = start.clone();
//         while !curr.ends_with("Z") {
//             let turn = turns[steps % turns.len()];
//             curr = rules.get(&curr).unwrap().get(&turn).unwrap().to_string();
//             steps += 1;
//         }
//     }
// }

/*
 * Apparently, the distance to the first Z is the same as any loop containing
 * Z nodes. Therefore, all we need to do is find the distance to the first Z,
 * then take the LCM over all distances. imo really dumb but let's try it.
 */
pub fn part2() {
    let fname = "../data/day8.txt";
    let input = read_input(fname);
    let (turns, rules) = parse_input(input);

    let mut distances_to_ends = Vec::new();
    for start_node in rules.keys().filter(|k| k.ends_with("A")) {
        let steps = dist_to_end(start_node, turns.clone(), &rules);
        distances_to_ends.push(steps);
    }

    let mut lcm: u64 = 1;
    for dist in distances_to_ends {
        lcm = num_integer::lcm(lcm, dist as u64);
    }

    println!("Part 2: {}", lcm);
}
