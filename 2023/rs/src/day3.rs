use std::collections::HashMap;
use std::fs::File;
use std::io::{BufRead, BufReader};

fn is_symb(c: char) -> bool {
    c != '.' && !c.is_digit(10)
}

fn has_symb_adj(board: &Vec<Vec<char>>, i: usize, j: usize) -> bool {
    let mut has_adj = false;
    // Check all 8 adjacent squares to see if any of them are symbols
    if i > 0 {
        if j > 0 && is_symb(board[i - 1][j - 1]) {
            has_adj = true;
        }

        if is_symb(board[i - 1][j]) {
            has_adj = true;
        }

        if j < board[i].len() - 1 && is_symb(board[i - 1][j + 1]) {
            has_adj = true;
        }
    }

    if j > 0 && is_symb(board[i][j - 1]) {
        has_adj = true;
    }

    if j < board[i].len() - 1 && is_symb(board[i][j + 1]) {
        has_adj = true;
    }

    if i < board.len() - 1 {
        if j > 0 && is_symb(board[i + 1][j - 1]) {
            has_adj = true;
        }

        if is_symb(board[i + 1][j]) {
            has_adj = true;
        }

        if j < board[i].len() - 1 && is_symb(board[i + 1][j + 1]) {
            has_adj = true;
        }
    }

    has_adj
}

fn adj_star_coords(board: &Vec<Vec<char>>, i: usize, j: usize) -> Vec<(usize, usize)> {
    let mut coords = Vec::new();
    // Check all 8 adjacent squares to see if any of them are *
    if i > 0 {
        if j > 0 && board[i - 1][j - 1] == '*' {
            coords.push((i - 1, j - 1));
        }

        if board[i - 1][j] == '*' {
            coords.push((i - 1, j));
        }

        if j < board[i].len() - 1 && board[i - 1][j + 1] == '*' {
            coords.push((i - 1, j + 1));
        }
    }

    if j > 0 && board[i][j - 1] == '*' {
        coords.push((i, j - 1));
    }

    if j < board[i].len() - 1 && board[i][j + 1] == '*' {
        coords.push((i, j + 1));
    }

    if i < board.len() - 1 {
        if j > 0 && board[i + 1][j - 1] == '*' {
            coords.push((i + 1, j - 1));
        }

        if board[i + 1][j] == '*' {
            coords.push((i + 1, j));
        }

        if j < board[i].len() - 1 && board[i + 1][j + 1] == '*' {
            coords.push((i + 1, j + 1));
        }
    }

    coords
}

pub fn part1() {
    let file_path = "../data/day3.txt";
    let file = File::open(file_path).expect("Failed to open file");
    let reader = BufReader::new(file);

    let mut sum = 0;

    // Convert the entire file into a vector of vector of chars
    let mut lines: Vec<Vec<char>> = Vec::new();
    for line in reader.lines() {
        if let Ok(line) = line {
            let mut line_chars: Vec<char> = Vec::new();
            for c in line.chars() {
                line_chars.push(c);
            }
            lines.push(line_chars);
        }
    }

    // Iterate over the board, and iteratively build up numbers.
    // If any of the digits of the numbers has a symbol adjacent, then
    // by the time the number is complete, we can add it to the total.
    for i in 0..lines.len() {
        let mut j = 0;
        while j < lines[i].len() {
            if lines[i][j].is_digit(10) {
                let mut record = false;
                let mut num = 0;
                let mut k = j;
                while k < lines[i].len() && lines[i][k].is_digit(10) {
                    num = num * 10 + lines[i][k].to_digit(10).unwrap();
                    if has_symb_adj(&lines, i, k) {
                        record = true;
                    }

                    k += 1;
                }

                if record {
                    sum += num;
                }

                j = k;
            } else {
                j += 1;
            }
        }
    }

    println!("Sum of combined numbers: {}", sum);
}

pub fn part2() {
    let file_path = "../data/day3.txt";
    let file = File::open(file_path).expect("Failed to open file");
    let reader = BufReader::new(file);

    let mut sum = 0;
    let mut gear_map: HashMap<(usize, usize), Vec<u32>> = HashMap::new();

    // Convert the entire file into a vector of vector of chars
    let mut lines: Vec<Vec<char>> = Vec::new();
    for line in reader.lines() {
        if let Ok(line) = line {
            let mut line_chars: Vec<char> = Vec::new();
            for c in line.chars() {
                line_chars.push(c);
            }

            lines.push(line_chars);
        }
    }

    // Iterate over the board, and iteratively build up numbers.
    // If any of the digits of the numbers has a symbol adjacent, then
    // by the time the number is complete, we can add it to the total.
    for i in 0..lines.len() {
        let mut j = 0;
        while j < lines[i].len() {
            if lines[i][j].is_digit(10) {
                let mut num = 0;
                let mut k = j;
                let mut gear_map_curr: Vec<(usize, usize)> = Vec::new();
                while k < lines[i].len() && lines[i][k].is_digit(10) {
                    num = num * 10 + lines[i][k].to_digit(10).unwrap();
                    for (x, y) in adj_star_coords(&lines, i, k) {
                        if !gear_map_curr.contains(&(x, y)) {
                            gear_map_curr.push((x, y));
                        }
                    }

                    k += 1;
                }

                for (x, y) in gear_map_curr {
                    if !gear_map.contains_key(&(x, y)) {
                        gear_map.insert((x, y), Vec::new());
                    }

                    gear_map.get_mut(&(x, y)).unwrap().push(num);
                }

                j = k;
            } else {
                j += 1;
            }
        }
    }

    // Read the vectors, sum up the product of the numbers in those
    // which contain only two elements
    for (_, v) in gear_map {
        if v.len() == 2 {
            sum += v[0] * v[1];
        }
    }

    println!("Sum of combined numbers: {}", sum);
}
