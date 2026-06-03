fn main() {
    let data = [10, 20, 30, 40, 50];

    let mut input = String::new();
    std::io::stdin().read_line(&mut input).unwrap();

    let index: usize = input.trim().parse().unwrap_or(0);

    let value = if index < data.len() {
        data[index]
    } else {
        0
    };

    println!("{}", value);
}