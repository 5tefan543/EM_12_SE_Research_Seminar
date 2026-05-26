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

const char* select_buffer_element() {
    int choice;

    printf("Enter an index to access (0 to %d): ", BUFFER_SIZE - 1);

    // Read the user input and validate the choice
    if (scanf("%d", &choice) != 1) {
        // Input wasn't a valid integer
        printf("Invalid input.\n");
        return NULL;
    }

    if (choice < 0 || choice >= BUFFER_SIZE) {
        // Choice is out of bounds
        printf("Index out of bounds. Please enter a value between 0 and %d.\n", BUFFER_SIZE - 1);
        return NULL;
    }

    // Return the selected item
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