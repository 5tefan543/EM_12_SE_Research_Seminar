use std::io;

fn select_elements(buffer: &[i32]) -> Vec<i32> {
    let mut input = String::new();

    println!("Enter indices (space-separated):");

    io::stdin()
        .read_line(&mut input)
        .expect("Failed to read input");

    input
        .split_whitespace()
        .filter_map(|s| s.parse::<usize>().ok()) // parse to usize safely
        .filter_map(|idx| buffer.get(idx).copied()) // safe indexing
        .collect()
}

fn main() {
    let buffer = vec![10, 20, 30, 40, 50];

    let selected = select_elements(&buffer);

    println!("Selected elements: {:?}", selected);
}