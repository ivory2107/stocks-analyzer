#include <stdio.h>
#include <stdlib.h>
#include "request.h"

int main() {
    char *json = get_stock_data("IBM");
    if (json) {
        printf("%s\n", json);
        free(json);
    }
    return 0;
}