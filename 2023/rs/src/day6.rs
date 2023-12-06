use std::fs::File;
use std::io::{BufRead, BufReader};

pub fn part1() {
    let fname = "../data/day6.txt";
    let file = File::open(fname).expect("Failed to open file");
    let reader = BufReader::new(file);
    let mut lines = reader.lines();

    // Turn all the numbers in the first line into a 'times' vector
    let mut times = Vec::new();
    let first_line = lines.next().unwrap().expect("Failed to read line");
    for num in first_line.split_whitespace() {
        // Check if num is a number
        if num.parse::<u32>().is_err() {
            continue;
        }

        times.push(num.parse::<u32>().unwrap());
    }

    let mut records = Vec::new();
    let second_line = lines.next().unwrap().expect("Failed to read line");
    for num in second_line.split_whitespace() {
        if num.parse::<u32>().is_err() {
            continue;
        }

        records.push(num.parse::<u32>().unwrap());
    }

    // How many ways are there to beat the record?
    let mut ways = Vec::new();
    for i in 0..times.len() {
        let mut wins = 0;
        for j in 0..times[i] + 1 {
            if j * (times[i] - j) > records[i] {
                wins += 1;
            }
        }

        ways.push(wins);
    }

    let res = ways.iter().fold(1, |acc, x| acc * x);
    println!("Part 1: {}", res);
}

pub fn part2() {
    let fname = "../data/day6.txt";
    let file = File::open(fname).expect("Failed to open file");
    let reader = BufReader::new(file);
    let mut lines = reader.lines();

    // Turn all the numbers in the first line into a 'times' vector
    let first_line = lines.next().unwrap().expect("Failed to read line");

    // Convert all the numbers in first_line into one big number
    let mut time: u64 = 0;
    for char in first_line.chars() {
        if char.is_digit(10) {
            time = time * 10 + char.to_digit(10).map(u64::from).unwrap();
        }
    }

    let mut record: u64 = 0;
    let second_line = lines.next().unwrap().expect("Failed to read line");
    for char in second_line.chars() {
        if char.is_digit(10) {
            record = record * 10 + char.to_digit(10).map(u64::from).unwrap();
        }
    }

    // How many ways are there to beat the record?
    let mut wins = 0;
    for j in 0..time + 1 {
        if j * (time - j) > record {
            wins += 1;
        }
    }

    println!("Part 2: {}", wins);
}
