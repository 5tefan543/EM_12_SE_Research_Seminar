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

    // Implement function
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