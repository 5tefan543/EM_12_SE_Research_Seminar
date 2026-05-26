use std::io;

fn select_element(buffer: &[i32]) -> Vec<i32> {
    let mut input = String::new();

    println!("Enter index:");

    // Read user input
    io::stdin().read_line(&mut input).expect("Failed to read line");

    // Parse the input to an integer
    let index: usize = match input.trim().parse() {
        Ok(num) => num,
        Err(_) => {
            println!("Invalid input. Please enter a valid number.");
            return Vec::new(); // Return an empty vector if parsing fails
        }
    };

    // Check if the index is within bounds and return the selected element
    if index < buffer.len() {
        vec![buffer[index]]
    } else {
        println!("Index out of bounds.");
        Vec::new() // Return an empty vector if the index is out of bounds
    }
}

fn main() {
    let buffer = vec![10, 20, 30, 40, 50];

    let selected = select_element(&buffer);

    if !selected.is_empty() {
        println!("Selected element: {:?}", selected);
    } else {
        println!("No valid element selected.");
    }
}