use std::cmp::max;
use std::collections::HashSet;
use std::fs::File;
use std::io::{BufRead, BufReader};

fn read_input(fname: &str) -> Vec<Vec<char>> {
    let file = File::open(fname).expect("Failed to open file");
    let reader = BufReader::new(file);
    let mut lines = reader.lines();
    let mut input = Vec::new();

    while let Some(line) = lines.next() {
        let mut chars = Vec::new();
        for char in line.unwrap().chars() {
            chars.push(char);
        }

        input.push(chars);
    }

    input
}

fn dfs(input: &Vec<Vec<char>>, start: (i32, i32), dir: (i32, i32)) -> usize {
    let height = input.len() as i32;
    let width = input[0].len() as i32;
    let mut visited_with_dir = HashSet::new();
    let mut stack: Vec<((i32, i32), (i32, i32))> = Vec::new();
    stack.push((start, dir));

    // DFS
    while let Some(((x, y), (dx, dy))) = stack.pop() {
        if visited_with_dir.contains(&((x, y), (dx, dy))) {
            continue;
        } else if x < 0 || y < 0 || x >= width || y >= height {
            continue;
        }

        visited_with_dir.insert(((x, y), (dx, dy)));
        match input[y as usize][x as usize] {
            '/' => {
                if dx != 0 {
                    stack.push(((x, y - dx), (0, -dx)));
                } else if dy != 0 {
                    stack.push(((x - dy, y), (-dy, 0)));
                }
            }
            '\\' => {
                if dx != 0 {
                    stack.push(((x, y + dx), (0, dx)));
                } else if dy != 0 {
                    stack.push(((x + dy, y), (dy, 0)));
                }
            }
            '-' => {
                if dy != 0 {
                    stack.push(((x - 1, y), (-1, 0)));
                    stack.push(((x + 1, y), (1, 0)));
                } else {
                    stack.push(((x + dx, y + dy), (dx, dy)))
                }
            }
            '|' => {
                if dx != 0 {
                    stack.push(((x, y - 1), (0, -1)));
                    stack.push(((x, y + 1), (0, 1)));
                } else {
                    stack.push(((x + dx, y + dy), (dx, dy)))
                }
            }
            _ => {
                stack.push(((x + dx, y + dy), (dx, dy)));
            }
        }
    }

    let mut energized = HashSet::new();
    for ((x, y), _) in visited_with_dir.iter() {
        energized.insert((x, y));
    }

    energized.len()
}

pub fn part1() {
    let fname = "../data/day16.txt";
    let input = read_input(fname);

    let num_energized = dfs(&input, (0, 0), (1, 0));
    println!("Part 1: {}", num_energized);
}

pub fn part2() {
    let fname = "../data/day16.txt";
    let input = read_input(fname);
    let height = input.len() as i32;
    let width = input[0].len() as i32;

    let mut best_energized = 0;
    for y in 0..input.len() {
        let left = ((0, y as i32), (1, 0));
        let right = ((width - 1, y as i32), (-1, 0));

        let (lstart, ldir) = left;
        best_energized = max(best_energized, dfs(&input, lstart, ldir));

        let (rstart, rdir) = right;
        best_energized = max(best_energized, dfs(&input, rstart, rdir));
    }

    for x in 0..input[0].len() {
        let top = ((x as i32, 0), (0, 1));
        let bottom = ((x as i32, height - 1), (0, -1));

        let (tstart, tdir) = top;
        best_energized = max(best_energized, dfs(&input, tstart, tdir));

        let (bstart, bdir) = bottom;
        best_energized = max(best_energized, dfs(&input, bstart, bdir));
    }

    println!("Part 2: {}", best_energized);
}
