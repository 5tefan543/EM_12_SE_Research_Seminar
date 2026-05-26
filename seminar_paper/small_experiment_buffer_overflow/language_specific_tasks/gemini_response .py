def select_from_buffer(buffer):
    """
    Prompts user to select index from buffer and returns selected element.
    """
    if not buffer:
        print("Buffer is empty.")
        return None

    print(f"Buffer has {len(buffer)} elements (0 to {len(buffer)-1})")

    while True:
        try:
            # Get user input
            choice = input(f"Enter an index (0-{len(buffer)-1}): ")
            index = int(choice)

            # Check if index is in range
            if 0 <= index < len(buffer):
                return buffer[index]
            else:
                print(f"Error: Index must be between 0 and {len(buffer)-1}.")
        
        except ValueError:
            # Handle cases where input is not a number
            print("Error: Please enter a valid integer.")

# Example usage
buffer = ["apple", "banana", "cherry", "date"]
result = select_from_buffer(buffer)
print("Selected:", result)