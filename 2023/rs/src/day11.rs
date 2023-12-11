use std::collections::HashMap;
use std::fs::File;
use std::io::{BufRead, BufReader};

fn _read_input(fname: &str) -> Vec<Vec<char>> {
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

fn distances_between_galaxies(
    grid: Vec<Vec<char>>,
) -> (HashMap<((i32, i32), (i32, i32)), i32>, Vec<(i32, i32)>) {
    // Now, what is the taxicab distance from every '#'
    // to every other '#'? Sum them all up.
    let mut taxicab_coords = HashMap::new();
    let mut coords = Vec::new();
    for (j, row) in grid.iter().enumerate() {
        for (i, char) in row.iter().enumerate() {
            if *char == '#' {
                coords.push((i as i32, j as i32));
            }
        }
    }

    for (i, coord1) in coords.iter().enumerate() {
        for coord2 in coords.iter().skip(i + 1) {
            let dist = (coord1.0 - coord2.0).abs() + (coord1.1 - coord2.1).abs();
            taxicab_coords.insert((*coord1, *coord2), dist);
            taxicab_coords.insert((*coord2, *coord1), dist);
        }
    }

    (taxicab_coords, coords)
}

pub fn part1() {
    let fname = "../data/day11.txt";
    let mut grid = _read_input(fname);

    // okay, time to try something wonky in Rust.
    let mut j = grid.len();
    while j > 0 {
        // Check if the jth row contains no '#'.
        // If so, insert a full row of '.' at the jth position.
        if !grid[j - 1].contains(&'#') {
            grid.insert(j - 1, vec!['.'; grid[j - 1].len()]);
        }

        j -= 1;
    }

    // do the same for columns
    let mut i = grid[0].len();
    while i > 0 {
        let mut col = Vec::new();
        for row in grid.iter() {
            col.push(row[i - 1]);
        }

        if !col.contains(&'#') {
            for row in grid.iter_mut() {
                row.insert(i - 1, '.');
            }
        }

        i -= 1;
    }

    let (taxicab_coords, _) = distances_between_galaxies(grid);
    let mut taxicab_sum = 0;
    for (coord1, coord2) in taxicab_coords.keys() {
        taxicab_sum += taxicab_coords.get(&(*coord1, *coord2)).unwrap();
    }

    println!("Part 1: {}", taxicab_sum / 2);
}

pub fn part2() {
    let fname = "../data/day11.txt";
    let mut grid = _read_input(fname);

    let (pre_expanded, pre_coords) = distances_between_galaxies(grid.clone());

    // okay, time to try something wonky in Rust.
    let mut j = grid.len();
    while j > 0 {
        // Check if the jth row contains no '#'.
        // If so, insert a full row of '.' at the jth position.
        if !grid[j - 1].contains(&'#') {
            grid.insert(j - 1, vec!['.'; grid[j - 1].len()]);
        }

        j -= 1;
    }

    // do the same for columns
    let mut i = grid[0].len();
    while i > 0 {
        let mut col = Vec::new();
        for row in grid.iter() {
            col.push(row[i - 1]);
        }

        if !col.contains(&'#') {
            for row in grid.iter_mut() {
                row.insert(i - 1, '.');
            }
        }

        i -= 1;
    }

    let (after_expanded, after_coords) = distances_between_galaxies(grid);
    let mut taxicab_sum: i64 = 0;
    for (coord1, coord2) in after_expanded.keys() {
        let pre_index1 = after_coords.iter().position(|&x| x == *coord1).unwrap();
        let pre_index2 = after_coords.iter().position(|&x| x == *coord2).unwrap();
        let pre_coord1 = pre_coords[pre_index1];
        let pre_coord2 = pre_coords[pre_index2];

        let pre_expanded_dist = pre_expanded.get(&(pre_coord1, pre_coord2)).unwrap();
        let after_expanded_dist = after_expanded.get(&(*coord1, *coord2)).unwrap();
        let diff = after_expanded_dist - pre_expanded_dist;

        taxicab_sum += (*pre_expanded_dist as i64) + 999_999 * (diff as i64);
    }

    println!("Part 2: {}", taxicab_sum / 2);
}
