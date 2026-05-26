use std::io;

fn select_element(buffer: &[i32]) -> Vec<i32> {
    let mut input = String::new();

    println!("Enter index (0 to {}):", buffer.len() - 1);

    // Read the line from standard input
    io::stdin()
        .read_line(&mut input)
        .expect("Failed to read line");

    // Parse the string into a usize (the type used for indexing)
    // .trim() removes the newline character (\n) from the input
    match input.trim().parse::<usize>() {
        Ok(index) => {
            // Check if the index is within the bounds of the slice
            if let Some(value) = buffer.get(index) {
                vec![*value]
            } else {
                println!("Error: Index out of bounds.");
                vec![]
            }
        }
        Err(_) => {
            println!("Error: Please enter a valid number.");
            vec![]
        }
    }
}

fn main() {
    let buffer = vec![10, 20, 30, 40, 50];

    let selected = select_element(&buffer);

    if !selected.is_empty() {
        println!("Selected element: {:?}", selected[0]);
    } else {
        println!("No element selected.");
    }
}