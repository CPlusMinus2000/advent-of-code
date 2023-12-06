use std::collections::HashMap;
use std::fs::File;
use std::io::{BufRead, BufReader};

pub fn part1() {
    let file = File::open("../data/day4.txt").unwrap();
    let reader = BufReader::new(file);

    let mut sum = 0;
    for line in reader.lines() {
        if let Ok(line) = line {
            let mut lsplit_1 = line.split(":");
            let card = lsplit_1.next().unwrap().trim();
            let _cnum = card.split(" ").last().unwrap().parse::<u32>().unwrap();
            let mut lsplit_2 = lsplit_1.next().unwrap().trim().split(" | ");

            let win_nums = lsplit_2.next().unwrap().trim().split(" ");
            let have_nums = lsplit_2.next().unwrap().trim().split(" ");

            // Convert win_nums into a set
            let mut win_nums_set = std::collections::HashSet::new();
            for num in win_nums {
                if num != "" {
                    win_nums_set.insert(num.parse::<u32>().unwrap());
                }
            }

            // How many wins do we have?
            let mut wins = 0;
            for num in have_nums {
                if num == "" {
                    continue;
                }

                let num_as_u32 = num.parse::<u32>().unwrap();
                if win_nums_set.contains(&num_as_u32) {
                    wins += 1;
                }
            }

            if wins > 0 {
                sum += u32::pow(2, wins - 1);
            }
        }
    }

    println!("Part 1: {}", sum);
}

pub fn part2() {
    let filename = "../data/day4.txt";
    let file = File::open(filename).unwrap();
    let mut reader = BufReader::new(file);

    // Make a copy of reader to count the number of lines
    let num_lines = reader.lines().count();

    let mut results = HashMap::new();
    for i in 0..num_lines {
        results.insert(i + 1, 1);
    }

    reader = BufReader::new(File::open(filename).unwrap());
    for line in reader.lines() {
        if let Ok(line) = line {
            let mut lsplit_1 = line.split(":");
            let card = lsplit_1.next().unwrap().trim();
            let cnum = card.split(" ").last().unwrap().parse::<u32>().unwrap();
            let mut lsplit_2 = lsplit_1.next().unwrap().trim().split(" | ");

            let win_nums = lsplit_2.next().unwrap().trim().split(" ");
            let have_nums = lsplit_2.next().unwrap().trim().split(" ");

            // Convert win_nums into a set
            let mut win_nums_set = std::collections::HashSet::new();
            for num in win_nums {
                if num != "" {
                    win_nums_set.insert(num.parse::<u32>().unwrap());
                }
            }

            // How many wins do we have?
            let mut wins = 0;
            for num in have_nums {
                if num == "" {
                    continue;
                }

                let num_as_u32 = num.parse::<u32>().unwrap();
                if win_nums_set.contains(&num_as_u32) {
                    wins += 1;
                }
            }

            if wins > 0 {
                for i in cnum + 1..cnum + wins + 1 {
                    if i <= num_lines as u32 {
                        results.insert(
                            i as usize,
                            results[&(i as usize)] + results[&(cnum as usize)],
                        );
                    }
                }
            }
        }
    }

    let sum = results.values().sum::<u32>();
    println!("Part 1: {}", sum);
}
