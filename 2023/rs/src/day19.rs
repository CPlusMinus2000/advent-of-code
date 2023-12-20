use std::collections::{HashMap, HashSet};
use std::fs::File;
use std::io::{BufRead, BufReader};

// Input returns a tuple containing two items:
// 1. A Hashmap of strings to workflows, where a workflow
//  is a function that takes a Part and returns a string.
// 2. A Vector of Parts, where a Part is a HashMap of strings to ints.
type Part = HashMap<String, u32>;
fn read_input(
    fname: &str,
) -> (
    HashMap<String, impl Fn(&Part) -> String>,
    HashMap<String, Vec<(String, char, u32, String)>>,
    Vec<Part>,
) {
    let file = File::open(fname).expect("Failed to open file");
    let reader = BufReader::new(file);
    let mut lines = reader.lines();
    let mut workflows = HashMap::new();
    let mut workflow_conditions = HashMap::new();
    let mut parts = Vec::new();

    while let Some(line) = lines.next() {
        let line = line.expect("ERROR: Could not read line");
        if line == "" {
            break;
        }

        // Start processing workflows
        // The name of a workflow is the first word in a line, up to the first {
        let line_parts = line.split("{").collect::<Vec<&str>>();
        let name = line_parts[0].trim().to_string();

        // The rest of the line is the workflow
        let mut conditions = Vec::new();
        let workflow = line_parts[1][..line_parts[1].len() - 1].trim();
        for branch in workflow.split(",") {
            let bsplit = branch.split(":").collect::<Vec<&str>>();
            let condition = bsplit[0].trim().to_string();
            if condition.contains(&">") {
                let csplit = condition.split(">").collect::<Vec<&str>>();
                conditions.push((
                    csplit[0].trim().to_string(),
                    '>',
                    csplit[1].trim().to_string().parse::<u32>().unwrap(),
                    bsplit[1].trim().to_string(),
                ));
            } else if condition.contains(&"<") {
                let csplit = condition.split("<").collect::<Vec<&str>>();
                conditions.push((
                    csplit[0].trim().to_string(),
                    '<',
                    csplit[1].trim().to_string().parse::<u32>().unwrap(),
                    bsplit[1].trim().to_string(),
                ));
            } else {
                conditions.push(("".to_string(), 'X', 0, bsplit[0].trim().to_string()));
            }
        }

        // Add the workflow to the workflows HashMap
        workflow_conditions.insert(name.clone(), conditions.clone());

        // Create a workflow function
        let workflow = move |part: &Part| -> String {
            for condition in conditions.clone() {
                let (key, op, val, res) = condition;
                if op == '<' && part[&key] < val {
                    return res;
                } else if op == '>' && part[&key] > val {
                    return res;
                } else if op == 'X' {
                    return res;
                }
            }

            // Raise an error if no conditions are met
            panic!("ERROR: No conditions met");
        };

        workflows.insert(name, workflow);
    }

    while let Some(line) = lines.next() {
        let line = line.expect("ERROR: Could not read line");
        let mut part = HashMap::new();
        let fields = line[1..line.len() - 1].split(",");
        for field in fields {
            let fsplit = field.split("=").collect::<Vec<&str>>();
            part.insert(
                fsplit[0].trim().to_string(),
                fsplit[1].trim().to_string().parse::<u32>().unwrap(),
            );
        }

        parts.push(part);
    }

    (workflows, workflow_conditions, parts)
}

pub fn part1() {
    let (workflows, _, parts) = read_input("../data/day19.txt");
    let mut total = 0;
    for part in parts {
        let mut res = workflows["in"](&part);
        while res != "A".to_string() && res != "R".to_string() {
            res = workflows[&res](&part);
        }

        if res == "A".to_string() {
            total += part.values().sum::<u32>();
        }
    }

    println!("Part 1: {}", total);
}

pub fn part2() {
    let (_, conditions, _) = read_input("../data/day19.txt");
    let mut accepted: u64 = 0;

    // The complicated part: we need to do a dfs on the conditions
    // in order to determine how many combinations of accepted parts
    // there will be. Essentially, each accepted combination is going to be some range
    // of each of the attributes a part can have. The dfs will narrow down the acceptable ranges,
    // and then it's just a matter of adding up how many combinations there are.
    let mut accepted_combinations: Vec<HashMap<String, Vec<u32>>> = Vec::new();
    let mut stack: Vec<(String, HashMap<String, Vec<u32>>, HashSet<String>)> = Vec::new();
    let mut base_ranges = HashMap::new();
    base_ranges.insert("x".to_string(), vec![0, 4001]);
    base_ranges.insert("m".to_string(), vec![0, 4001]);
    base_ranges.insert("a".to_string(), vec![0, 4001]);
    base_ranges.insert("s".to_string(), vec![0, 4001]);
    stack.push(("in".to_string(), base_ranges, HashSet::new()));
    while let Some((curr_flow, mut accepted_ranges, visited)) = stack.pop() {
        // If we've already visited this flow, skip it
        if visited.contains(&curr_flow) {
            continue;
        }

        let mut new_visited = visited.clone();
        new_visited.insert(curr_flow.clone());

        let condition_list = &conditions[&curr_flow];
        for condition in condition_list {
            let (key, op, val, res) = condition;
            let mut new_accepted_ranges = accepted_ranges.clone();

            // For each condition, make accepted ranges that both satisfy the condition
            // and do not satisfy the condition (branching paths)
            if *op == '<' {
                new_accepted_ranges
                    .entry(key.clone())
                    .and_modify(|e| e[1] = *val);

                accepted_ranges
                    .entry(key.clone())
                    .and_modify(|e| e[0] = *val - 1);
            } else if *op == '>' {
                new_accepted_ranges
                    .entry(key.clone())
                    .and_modify(|e| e[0] = *val);

                accepted_ranges
                    .entry(key.clone())
                    .and_modify(|e| e[1] = *val + 1);
            }

            // If the range is still valid, check the res
            if *op == 'X' || new_accepted_ranges[key][0] < new_accepted_ranges[key][1] - 1 {
                if *res == "A".to_string() {
                    // Accepted, add to accepted_combinations
                    accepted_combinations.push(new_accepted_ranges.clone());
                } else if *res != "R".to_string() {
                    // Not accepted, add to stack
                    stack.push((
                        res.clone(),
                        new_accepted_ranges.clone(),
                        new_visited.clone(),
                    ));
                }
            }

            // If accepted_ranges are no longer valid, break
            if *op != 'X' && accepted_ranges[key][0] >= accepted_ranges[key][1] - 1 {
                break;
            }
        }
    }

    // Now that we have all the accepted combinations, we need to find the number of combinations
    // for each attribute. We can do this by finding the number of combinations for each attribute
    // in each accepted combination, and then multiplying them together.
    for accepted_combination in accepted_combinations {
        let mut x_combinations: u64 = 0;
        let mut m_combinations: u64 = 0;
        let mut a_combinations: u64 = 0;
        let mut s_combinations: u64 = 0;
        println!("{:?}", accepted_combination);
        for (key, range) in accepted_combination {
            if key == "x" {
                x_combinations = (range[1] - range[0] - 1) as u64;
            } else if key == "m" {
                m_combinations = (range[1] - range[0] - 1) as u64;
            } else if key == "a" {
                a_combinations = (range[1] - range[0] - 1) as u64;
            } else if key == "s" {
                s_combinations = (range[1] - range[0] - 1) as u64;
            }
        }

        // Multiply the combinations together as u64s to avoid overflow
        accepted += x_combinations * m_combinations * a_combinations * s_combinations;
    }

    println!("Part 2: {}", accepted);
}
