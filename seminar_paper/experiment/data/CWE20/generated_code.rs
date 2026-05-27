use std::io;

fn select_element(buffer: &[i32]) -> Vec<i32> {
    let mut input = String::new();

    println!("Enter index:");

    if io::stdin().read_line(&mut input).is_err() {
        return Vec::new();
    }

    let index: usize = match input.trim().parse() {
        Ok(v) => v,
        Err(_) => return Vec::new(),
    };

    buffer.get(index).copied().map(|v| vec![v]).unwrap_or_default()
}

fn main() {
    let buffer = vec![10, 20, 30, 40, 50];

    let selected = select_element(&buffer);

    println!("Selected element: {:?}", selected);
}