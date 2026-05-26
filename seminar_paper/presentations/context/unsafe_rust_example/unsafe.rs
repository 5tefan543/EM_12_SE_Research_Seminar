use std::rc::Rc;

fn main() {
    let raw_ptr: *const String;

    {
        let secret = Rc::new(String::from("SECRET: database_password_123"));
        raw_ptr = Rc::as_ptr(&secret);
        
        println!("{}", secret);
    } // secret dropped here -> memory freed
    
    // println!("{}", data); prevented by Rust

    unsafe {
        // Undefined behavior: may print garbage / crash / or still look correct
        let data = Rc::from_raw(raw_ptr);
        println!("{}", data);
    }
}