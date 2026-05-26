#include <stdio.h>
#include <stdlib.h>

#define BUFFER_SIZE 10

void process_elements(int *buffer, int size) {
    int index;

    printf("Enter an index (0-%d): ", size - 1);
    if (scanf("%d", &index) != 1) {
        printf("Invalid input.\n");
        return;
    }

    // ✅ Bounds checking
    if (index < 0 || index >= size) {
        printf("Index out of bounds.\n");
        return;
    }

    // Safe access
    printf("Selected element: %d\n", buffer[index]);

    // Example: use the selected element later
    int result = buffer[index] * 2;
    printf("Processed result: %d\n", result);
}

int main() {
    int buffer[BUFFER_SIZE] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9};

    process_elements(buffer, BUFFER_SIZE);

    return 0;
}