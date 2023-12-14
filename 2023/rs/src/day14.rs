use std::collections::HashMap;
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

fn _print_grid(grid: Vec<Vec<char>>) {
    for row in grid.iter() {
        for char in row.iter() {
            print!("{}", char);
        }
        println!();
    }
}

fn move_all_rocks(grid: Vec<Vec<char>>, direction: (i32, i32)) -> Vec<Vec<char>> {
    let mut new_grid = grid.clone();
    let height = grid.len();
    let width = grid[0].len();
    loop {
        let mut moved = false;
        for j in 0..height {
            for i in 0..width {
                if new_grid[j][i] == 'O' {
                    let new_j = j as i32 + direction.1;
                    let new_i = i as i32 + direction.0;
                    let new_j_u = new_j as usize;
                    let new_i_u = new_i as usize;

                    if 0 <= new_j
                        && 0 <= new_i
                        && new_j_u < height
                        && new_i_u < width
                        && new_grid[new_j_u][new_i_u] == '.'
                    {
                        new_grid[j][i] = '.';
                        new_grid[new_j_u][new_i_u] = 'O';
                        moved = true;
                    }
                }
            }
        }

        if !moved {
            break;
        }
    }

    new_grid
}

fn calculate_load(grid: Vec<Vec<char>>) -> u32 {
    let mut load = 0;
    for (j, row) in grid.iter().rev().enumerate() {
        for char in row.iter() {
            if char == &'O' {
                load += j as u32 + 1;
            }
        }
    }

    load
}

pub fn part1() {
    let fname = "../data/day14.txt";
    let input = read_input(fname);
    let new_grid = move_all_rocks(input, (0, -1));
    let result = calculate_load(new_grid);

    println!("Result: {}", result);
}

pub fn part2() {
    let fname = "../data/day14.txt";
    let input = read_input(fname);
    let mut new_grid = input.clone();
    let mut seen_grids = HashMap::new();
    let mut cycles = 0;

    seen_grids.insert(new_grid.clone(), cycles);
    loop {
        new_grid = move_all_rocks(new_grid, (0, -1));
        new_grid = move_all_rocks(new_grid, (-1, 0));
        new_grid = move_all_rocks(new_grid, (0, 1));
        new_grid = move_all_rocks(new_grid, (1, 0));

        cycles += 1;

        if seen_grids.contains_key(&new_grid.clone()) {
            // We should have enough information to calculate
            break;
        }

        seen_grids.insert(new_grid.clone(), cycles);
    }

    let cycle_length = cycles - seen_grids.get(&new_grid).unwrap();
    let mut remaining_cycles = (1_000_000_000 - cycles) % cycle_length;
    while remaining_cycles > 0 {
        new_grid = move_all_rocks(new_grid, (0, -1));
        new_grid = move_all_rocks(new_grid, (-1, 0));
        new_grid = move_all_rocks(new_grid, (0, 1));
        new_grid = move_all_rocks(new_grid, (1, 0));

        remaining_cycles -= 1;
    }

    let result = calculate_load(new_grid);
    println!("Result: {}", result);
}
