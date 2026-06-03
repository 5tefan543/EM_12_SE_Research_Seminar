use std::io::{self, Read};

fn main() {
    let mut input = String::new();
    let _ = io::stdin().read_to_string(&mut input);

    let choice = input.trim();

    let buffer = [10, 20, 30, 40, 50];

    let selected: Vec<i32> = match choice {
        "all" => buffer.to_vec(),
        "even" => buffer.iter().copied().step_by(2).collect(),
        "odd" => buffer.iter().copied().skip(1).step_by(2).collect(),
        "first" => buffer.first().copied().into_iter().collect(),
        "last" => buffer.last().copied().into_iter().collect(),
        _ => Vec::new(),
    };

    for value in selected {
        println!("{value}");
    }
}