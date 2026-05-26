use std::io::{self, Write};

fn get_element_from_buffer(buffer: &[i32]) -> Option<&i32> {
    print!("Enter the index of the element you'd like to use (0-{}): ", buffer.len() - 1);
    io::stdout().flush().unwrap();

    let mut input = String::new();
    
    // Read user input from the terminal
    io::stdin()
        .read_line(&mut input)
        .expect("Failed to read line");

    // Parse the string into a usize (the type used for indexing)
    let index: usize = match input.trim().parse() {
        Ok(num) => num,
        Err(_) => {
            println!("Please enter a valid non-negative integer.");
            return None;
        }
    };

    // .get() returns Some(&value) if in bounds, or None if out of bounds
    buffer.get(index)
}

fn main() {
    let my_buffer = vec![10, 20, 30, 40, 50];

    match get_element_from_buffer(&my_buffer) {
        Some(value) => println!("You selected the value: {}", value),
        None => println!("Invalid selection. No element was retrieved."),
    }
}