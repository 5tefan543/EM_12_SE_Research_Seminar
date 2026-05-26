const char* select_buffer_element() {
    int choice;
    
    printf("Enter an index to access (0 to %d): ", BUFFER_SIZE - 1);

    // 1. Read the input and check if it's a valid integer
    if (scanf("%d", &choice) != 1) {
        printf("Invalid input. Please enter a number.\n");
        return NULL;
    }

    // 2. Bounds checking: ensure the index is within [0, BUFFER_SIZE - 1]
    if (choice >= 0 && choice < BUFFER_SIZE) {
        return items[choice];
    } else {
        printf("Error: Index %d is out of bounds.\n", choice);
        return NULL;
    }
}