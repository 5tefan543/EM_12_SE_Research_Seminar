def select_buffer_elements(buffer):
    """
    Takes a predefined buffer and returns a subset based on user input.
    """
    print(f"Current Buffer: {buffer}")
    print(f"Enter the indices (0 to {len(buffer) - 1}) you want to use, separated by spaces.")
    
    user_input = input("Indices: ")
    
    selected_elements = []
    
    # Split the input string into individual potential indices
    raw_indices = user_input.split()
    
    for item in raw_indices:
        try:
            # Convert input to integer
            index = int(item)
            
            # Check if the index is within the valid range of the list
            if 0 <= index < len(buffer):
                selected_elements.append(buffer[index])
            else:
                print(f"Warning: Index {index} is out of range and will be skipped.")
                
        except ValueError:
            # Handle cases where input is not a number (e.g., "a", "!", etc.)
            print(f"Warning: '{item}' is not a valid integer and will be skipped.")
            
    return selected_elements

# --- Example Usage ---
my_buffer = ["Processor", "Memory", "Disk", "Network", "GPU"]
subset = select_buffer_elements(my_buffer)

if subset:
    print(f"\nElements selected for later use: {subset}")
else:
    print("\nNo valid elements were selected.")