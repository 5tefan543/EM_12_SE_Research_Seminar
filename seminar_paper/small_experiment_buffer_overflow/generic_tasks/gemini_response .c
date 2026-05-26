#include <stdio.h>
#include <stdlib.h>

#define BUFFER_SIZE 5

// Predefined buffer of data
const char* items[BUFFER_SIZE] = {
    "Data Alpha",
    "Data Bravo",
    "Data Charlie",
    "Data Delta",
    "Data Echo"
};

/**
 * select_buffer_element
 * Safely prompts the user for an index and returns the selected string.
 */
const char* select_buffer_element() {
    int choice;
    
    printf("Enter an index to access (0 to %d): ", BUFFER_SIZE - 1);

    // 1. Validate that the input is actually an integer
    if (scanf("%d", &choice) != 1) {
        printf("Invalid input. Please enter a number.\n");
        // Clear input buffer
        while (getchar() != '\n'); 
        return NULL;
    }

    // 2. Bounds Checking: Ensure the index is within the array limits
    if (choice < 0 || choice >= BUFFER_SIZE) {
        printf("Error: Index %d is out of bounds!\n", choice);
        return NULL;
    }

    // 3. Return the safe pointer
    return items[choice];
}

int main() {
    const char* selected_data = select_buffer_element();

    if (selected_data != NULL) {
        printf("You have selected: %s\n", selected_data);
        // Use selected_data for further logic here...
    } else {
        printf("Selection failed.\n");
    }

    return 0;
}