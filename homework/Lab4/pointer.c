#include <stdio.h>

int main(void) {
    int value = 10;
    int *p = &value;
    printf("before=%d\n", value);
    *p = 20;
    printf("after=%d\n", value);
    return 0;
}
