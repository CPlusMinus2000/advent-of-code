use std::collections::HashMap;
use std::fs::File;
use std::io::{BufRead, BufReader};

pub fn part1() {
    let file_path = "../data/day1.txt";
    let file = File::open(file_path).expect("Failed to open file");
    let reader = BufReader::new(file);

    let mut sum = 0;
    for line in reader.lines() {
        if let Ok(line) = line {
            let first_digit = line.chars().find(|c| c.is_digit(10));
            let last_digit = line.chars().rev().find(|c| c.is_digit(10));

            if let (Some(first), Some(last)) = (first_digit, last_digit) {
                let combined_number = format!("{}{}", first, last);
                let value = combined_number.parse::<u32>().unwrap_or(0);
                sum += value;
            }
        }
    }

    println!("Sum of combined numbers: {}", sum);
}

fn create_number_map() -> HashMap<String, u32> {
    let mut number_map = HashMap::new();
    number_map.insert(String::from("one"), 1);
    number_map.insert(String::from("two"), 2);
    number_map.insert(String::from("three"), 3);
    number_map.insert(String::from("four"), 4);
    number_map.insert(String::from("five"), 5);
    number_map.insert(String::from("six"), 6);
    number_map.insert(String::from("seven"), 7);
    number_map.insert(String::from("eight"), 8);
    number_map.insert(String::from("nine"), 9);

    number_map
}

fn digits_from_line(line: &str) -> u32 {
    let number_map = create_number_map();
    let mut start = 0;
    let mut end = 0;
    let mut breakout = false;

    for (i, c) in line.chars().enumerate() {
        if c.is_digit(10) {
            start = c.to_digit(10).unwrap();
            break;
        }

        // check if any of the words in the number map are in the line
        // starting from index i
        for (word, value) in number_map.iter() {
            if line[i..].starts_with(word) {
                start = *value;
                breakout = true;
                break;
            }
        }

        if breakout {
            break;
        }
    }

    breakout = false;
    for (i, c) in line.chars().rev().enumerate() {
        if c.is_digit(10) {
            end = c.to_digit(10).unwrap();
            break;
        }

        // check if any of the words in the number map are in the line
        // starting from index i, but reversed
        for (word, value) in number_map.iter() {
            if line[0..line.len() - i].ends_with(word) {
                end = *value;
                breakout = true;
                break;
            }
        }

        if breakout {
            break;
        }
    }

    start * 10 + end
}

pub fn part2() {
    let file_path = "../data/day1.txt";
    let file = File::open(file_path).expect("Failed to open file");
    let reader = BufReader::new(file);

    let mut sum = 0;
    for line in reader.lines() {
        if let Ok(line) = line {
            let combined_number = digits_from_line(&line);
            sum += combined_number;
        }
    }

    println!("Sum of combined numbers: {}", sum);
}
