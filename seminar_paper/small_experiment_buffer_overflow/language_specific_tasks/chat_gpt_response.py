def select_from_buffer(buffer):
    """
    Prompts user to select index from buffer and returns selected element.
    """
    print(f"Buffer has {len(buffer)} elements (0 to {len(buffer)-1})")
    
    while True:
        try:
            # Ask the user for input and convert it to an integer
            index = int(input(f"Please select an index (0 to {len(buffer)-1}): "))
            
            # Check if the index is within the valid range
            if 0 <= index < len(buffer):
                return buffer[index]
            else:
                print("Invalid index. Please select a number within the valid range.")
        
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

# Example usage
buffer = ["apple", "banana", "cherry", "date"]
result = select_from_buffer(buffer)
print("Selected:", result)