use std::io::{self, Read};

fn main() {
    let mut input = String::new();
    let _ = io::stdin().read_to_string(&mut input);

    let idx: usize = input.trim().parse().unwrap_or(0);

    let buffer = [10, 20, 30, 40, 50];

    let value = buffer.get(idx).copied().unwrap_or(0);

    println!("{}", value);
}