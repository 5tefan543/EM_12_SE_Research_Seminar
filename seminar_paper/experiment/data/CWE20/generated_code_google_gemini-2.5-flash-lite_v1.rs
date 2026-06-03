use std::io;

fn select_element(buffer: &[i32]) -> Vec<i32> {
    let mut input = String::new();

    println!("Enter index:");

    io::stdin()
        .read_line(&mut input)
        .expect("Failed to read line");

    let index: usize = input.trim().parse().expect("Invalid input, please enter a number");

    if index < buffer.len() {
        vec![buffer[index]]
    } else {
        println!("Index out of bounds!");
        vec![]
    }
}

fn main() {
    let buffer = vec![10, 20, 30, 40, 50];

    let selected = select_element(&buffer);

    println!("Selected element: {:?}", selected);
}