use std::cmp::max;
use std::collections::HashMap;
use std::fs::File;
use std::io::{BufRead, BufReader};

fn rgb_map() -> HashMap<String, u32> {
    let mut rgb_map = HashMap::new();
    rgb_map.insert(String::from("red"), 12);
    rgb_map.insert(String::from("green"), 13);
    rgb_map.insert(String::from("blue"), 14);

    rgb_map
}

fn rgb_map_all_zero() -> HashMap<String, u32> {
    let mut rgb_map = HashMap::new();
    rgb_map.insert(String::from("red"), 0);
    rgb_map.insert(String::from("green"), 0);
    rgb_map.insert(String::from("blue"), 0);

    rgb_map
}

pub fn part1() {
    let file_path = "../data/day2.txt";
    let file = File::open(file_path).expect("Failed to open file");
    let reader = BufReader::new(file);
    let rgb = rgb_map();

    let mut sum = 0;
    for line in reader.lines() {
        if let Ok(line) = line {
            // split the line into game index and games, split by :
            let mut split_line = line.split(":");
            let game_index = split_line
                .next()
                .unwrap()
                .split(" ")
                .last()
                .unwrap()
                .parse::<u32>()
                .unwrap();
            let rest_of_line = split_line.next().unwrap().split(";");
            let mut good = true;
            for game in rest_of_line {
                let draws = game.trim().split(",");
                for draw in draws {
                    let mut draw_parts = draw.trim().split(" ");
                    let balls = draw_parts.next().unwrap();
                    let colour = draw_parts.next().unwrap();
                    if balls.parse::<u32>().unwrap() > rgb[colour] {
                        good = false;
                        break;
                    }
                }

                if !good {
                    break;
                }
            }

            if good {
                sum += game_index;
            }
        }
    }

    println!("Sum of combined numbers: {}", sum);
}

pub fn part2() {
    let file_path = "../data/day2.txt";
    let file = File::open(file_path).expect("Failed to open file");
    let reader = BufReader::new(file);

    let mut sum = 0;
    for line in reader.lines() {
        let mut rgb = rgb_map_all_zero();
        if let Ok(line) = line {
            // split the line into game index and games, split by :
            let mut split_line = line.split(":");
            split_line.next();
            let rest_of_line = split_line.next().unwrap().split(";");
            for game in rest_of_line {
                let draws = game.trim().split(",");
                for draw in draws {
                    let mut draw_parts = draw.trim().split(" ");
                    let balls = draw_parts.next().unwrap().parse::<u32>().unwrap();
                    let colour = draw_parts.next().unwrap();
                    rgb.insert(colour.to_string(), max(rgb[colour], balls));
                }
            }

            sum += rgb["red"] * rgb["green"] * rgb["blue"];
        }
    }

    println!("Sum of combined numbers: {}", sum);
}
