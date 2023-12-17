use std::cmp::max;
use std::collections::{BinaryHeap, HashMap, HashSet};
use std::fs::File;
use std::io::{BufRead, BufReader};

fn read_input(fname: &str) -> Vec<Vec<i32>> {
    let file = File::open(fname).expect("Failed to open file");
    let reader = BufReader::new(file);
    let mut lines = reader.lines();
    let mut input = Vec::new();

    while let Some(line) = lines.next() {
        let mut costs = Vec::new();
        for cchar in line.unwrap().chars() {
            // convert to u32 by reading the char as a digit
            costs.push(cchar.to_digit(10).unwrap() as i32);
        }

        input.push(costs);
    }

    input
}

fn dijkstra(input: &Vec<Vec<i32>>, start: (i32, i32)) -> HashMap<(i32, i32), i32> {
    let height = input.len();
    let width = input[0].len();
    let mut visited = HashMap::new();
    let mut heap = BinaryHeap::new();
    let mut costs = HashMap::new();
    heap.push((0, start, 3, (1, 0)));

    while let Some((cost, (x, y), straight, (dx, dy))) = heap.pop() {
        if visited.contains_key(&((x, y), (dx, dy))) {
            let prev_straight = visited.get(&((x, y), (dx, dy))).unwrap();
            if straight <= *prev_straight {
                continue;
            }
        } else if x < 0 || y < 0 || x as usize >= width || y as usize >= height {
            continue;
        }

        // Print everything
        // println!("({}, {}): {} ({}, {})", x, y, cost, dx, dy);

        visited.insert(((x, y), (dx, dy)), straight);
        if costs.contains_key(&(x, y)) {
            let prev_cost = costs.get(&(x, y)).unwrap();
            costs.insert((x, y), max(cost, *prev_cost));
        } else {
            costs.insert((x, y), cost);
        }

        if straight > 0
            && x + dx >= 0
            && y + dy >= 0
            && x + dx < width as i32
            && y + dy < height as i32
        {
            heap.push((
                cost - input[(y + dy) as usize][(x + dx) as usize],
                (x + dx, y + dy),
                straight - 1,
                (dx, dy),
            ));
        }

        // Try turning both left and right
        if dx != 0 {
            if y > 0 {
                heap.push((
                    cost - input[(y - 1) as usize][x as usize],
                    (x, y - 1),
                    2,
                    (0, -1),
                ));
            }

            if y < height as i32 - 1 {
                heap.push((
                    cost - input[(y + 1) as usize][x as usize],
                    (x, y + 1),
                    2,
                    (0, 1),
                ));
            }
        } else if dy != 0 {
            if x > 0 {
                heap.push((
                    cost - input[y as usize][(x - 1) as usize],
                    (x - 1, y),
                    2,
                    (-1, 0),
                ));
            }
            if x < width as i32 - 1 {
                heap.push((
                    cost - input[y as usize][(x + 1) as usize],
                    (x + 1, y),
                    2,
                    (1, 0),
                ));
            }
        }
    }

    costs
}

fn ultra_dijkstra(input: &Vec<Vec<i32>>, start: (i32, i32)) -> HashMap<(i32, i32), i32> {
    let height = input.len();
    let width = input[0].len();
    let mut visited = HashSet::new();
    let mut heap = BinaryHeap::new();
    let mut costs = HashMap::new();
    heap.push((0, start, 0, (1, 0)));

    while let Some((cost, (x, y), straight, (dx, dy))) = heap.pop() {
        if visited.contains(&((x, y), (dx, dy), straight)) {
            continue;
        } else if x < 0 || y < 0 || x as usize >= width || y as usize >= height {
            continue;
        }

        // Print everything
        // println!("({}, {}): {} ({}, {})", x, y, cost, dx, dy);

        visited.insert(((x, y), (dx, dy), straight));

        if (x, y) != (height as i32 - 1, width as i32 - 1) || straight >= 4 {
            // Don't allow setting the final cost if we haven't gone straight for 4
            if costs.contains_key(&(x, y)) {
                let prev_cost = costs.get(&(x, y)).unwrap();
                costs.insert((x, y), max(cost, *prev_cost));
            } else {
                costs.insert((x, y), cost);
            }
        }

        if straight < 10
            && x + dx >= 0
            && y + dy >= 0
            && x + dx < width as i32
            && y + dy < height as i32
        {
            heap.push((
                cost - input[(y + dy) as usize][(x + dx) as usize],
                (x + dx, y + dy),
                straight + 1,
                (dx, dy),
            ));
        }

        // Try turning both left and right
        if dx != 0 && straight >= 4 {
            if y > 0 {
                heap.push((
                    cost - input[(y - 1) as usize][x as usize],
                    (x, y - 1),
                    1,
                    (0, -1),
                ));
            }

            if y < height as i32 - 1 {
                heap.push((
                    cost - input[(y + 1) as usize][x as usize],
                    (x, y + 1),
                    1,
                    (0, 1),
                ));
            }
        } else if dy != 0 && straight >= 4 {
            if x > 0 {
                heap.push((
                    cost - input[y as usize][(x - 1) as usize],
                    (x - 1, y),
                    1,
                    (-1, 0),
                ));
            }
            if x < width as i32 - 1 {
                heap.push((
                    cost - input[y as usize][(x + 1) as usize],
                    (x + 1, y),
                    1,
                    (1, 0),
                ));
            }
        }
    }

    costs
}

pub fn part1() {
    let fname = "../data/day17.txt";
    let input = read_input(fname);

    let start = (0, 0);
    let height = input.len();
    let width = input[0].len();
    let costs = dijkstra(&input, start);

    // Cost at the end of the maze
    let end = (width as i32 - 1, height as i32 - 1);
    let cost = *costs.get(&end).unwrap() as i32 * -1;
    println!("Part 1: {}", cost);
}

pub fn part2() {
    let fname = "../data/day17.txt";
    let input = read_input(fname);

    let start = (0, 0);
    let height = input.len();
    let width = input[0].len();
    let costs = ultra_dijkstra(&input, start);

    // Cost at the end of the maze
    let end = (width as i32 - 1, height as i32 - 1);
    let cost = *costs.get(&end).unwrap() as i32 * -1;
    println!("Part 2: {}", cost);
}
