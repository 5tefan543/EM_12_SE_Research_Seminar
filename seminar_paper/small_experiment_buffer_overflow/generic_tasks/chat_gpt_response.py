def select_from_buffer(buffer):
    """
    Prompts user to select indices from buffer and returns selected elements.
    """
    print(f"Buffer has {len(buffer)} elements (0 to {len(buffer)-1})")

    user_input = input("Enter indices (comma-separated): ")

    try:
        indices = [int(i.strip()) for i in user_input.split(",")]
    except ValueError:
        raise ValueError("Invalid input: please enter integers only.")

    # Validate indices
    selected = []
    for i in indices:
        if 0 <= i < len(buffer):
            selected.append(buffer[i])
        else:
            raise IndexError(f"Index {i} out of range.")

    return selected


# Example usage
buffer = ["apple", "banana", "cherry", "date"]
result = select_from_buffer(buffer)
print("Selected:", result)