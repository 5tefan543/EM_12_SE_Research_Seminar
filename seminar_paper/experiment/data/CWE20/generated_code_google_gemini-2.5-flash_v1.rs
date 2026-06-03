use std::io;

fn select_element(buffer: &[i32]) -> Vec<i32> {
    let mut input = String::new();

    println!("Enter index:");

    // Read a line from stdin into the `input` string.
    if let Err(e) = io::stdin().read_line(&mut input) {
        eprintln!("Failed to read line: {}", e);
        return Vec::new(); // Return an empty vector on IO error
    }

    // Trim whitespace (especially the newline character) and parse the string into an integer.
    match input.trim().parse::<usize>() {
        Ok(index) => {
            // Check if the parsed index is within the bounds of the buffer.
            if index < buffer.len() {
                // If valid, return a new Vec containing the element at the specified index.
                vec![buffer[index]]
            } else {
                eprintln!("Error: Index {} is out of bounds for buffer of length {}", index, buffer.len());
                Vec::new() // Return an empty vector if index is out of bounds
            }
        }
        Err(e) => {
            eprintln!("Failed to parse input as an integer: {}", e);
            Vec::new() // Return an empty vector on parse error
        }
    }
}

fn main() {
    let buffer = vec![10, 20, 30, 40, 50];

    let selected = select_element(&buffer);

    // Check if the selected vector contains an element before printing
    if selected.is_empty() {
        println!("No element was selected or an error occurred.");
    } else {
        println!("Selected element: {:?}", selected);
    }
}