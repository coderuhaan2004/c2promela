#include <stdio.h>
#include <stdlib.h>

struct node {
    struct node *next;
    int value;
};

struct node *head = NULL;
struct node *tail = NULL;

void test(struct node *tmp) {
    tmp->next = NULL;
    if (tail == NULL) {
        // List is empty, initialize both head and tail
        head = tail = tmp;
    } else {
        // Append to the end of the list
        tail->next = tmp;
        tail = tmp;
    }
}

void print_list() {
    struct node *current = head;
    while (current != NULL) {
        printf("%d -> ", current->value);
        current = current->next;
    }
    printf("NULL\n");
}

int main() {
    // Create and add 3 nodes to the list
    for (int i = 1; i <= 3; i++) {
        struct node *new_node = (struct node *)malloc(sizeof(struct node));
        new_node->value = i;
        test(new_node);
    }

    print_list();  // Output: 1 -> 2 -> 3 -> NULL

    // Free allocated memory
    struct node *current = head;
    while (current != NULL) {
        struct node *next = current->next;
        free(current);
        current = next;
    }

    return 0;
}