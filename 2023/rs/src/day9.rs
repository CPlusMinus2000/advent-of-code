use std::fs::File;
use std::io::{BufRead, BufReader};

fn _read_input(fname: &str) -> Vec<Vec<i32>> {
    let file = File::open(fname).expect("Failed to open file");
    let reader = BufReader::new(file);
    let mut lines = reader.lines();
    let mut input = Vec::new();

    while let Some(line) = lines.next() {
        let mut nums = Vec::new();
        for num in line.unwrap().split_whitespace() {
            nums.push(num.parse::<i32>().unwrap());
        }

        input.push(nums);
    }

    input
}

pub fn part1() {
    let fname = "../data/day9.txt";
    let sequences = _read_input(fname);
    let mut extrapolation_sum = 0;

    for seq in sequences.iter() {
        let mut diff_stack = Vec::new();
        diff_stack.push(seq.clone());
        loop {
            let mut diffs = Vec::new();
            let prev_seq = diff_stack.last().unwrap().clone();
            for i in 0..prev_seq.len() - 1 {
                diffs.push(prev_seq[i + 1] - prev_seq[i]);
            }

            if diffs.iter().all(|&x| x == 0) {
                break;
            } else {
                diff_stack.push(diffs);
            }
        }

        let mut next_diff = 0;
        for diffs in diff_stack.iter().rev() {
            next_diff += diffs.last().unwrap();
        }

        extrapolation_sum += next_diff;
    }

    println!("Part 1: {}", extrapolation_sum);
}

pub fn part2() {
    let fname = "../data/day9.txt";
    let sequences = _read_input(fname);
    let mut extrapolation_sum = 0;

    for seq in sequences.iter() {
        let mut diff_stack = Vec::new();
        diff_stack.push(seq.clone());
        loop {
            let mut diffs = Vec::new();
            let prev_seq = diff_stack.last().unwrap().clone();
            for i in 0..prev_seq.len() - 1 {
                diffs.push(prev_seq[i + 1] - prev_seq[i]);
            }

            if diffs.iter().all(|&x| x == 0) {
                break;
            } else {
                diff_stack.push(diffs);
            }
        }

        let mut next_diff = 0;
        for diffs in diff_stack.iter().rev() {
            next_diff = diffs[0] - next_diff;
        }

        extrapolation_sum += next_diff;
    }

    println!("Part 2: {}", extrapolation_sum);
}
