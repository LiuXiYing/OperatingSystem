#include <stdio.h>
#include <unistd.h>

int main(void) {
    printf("pid=%ld, parent=%ld\n", (long)getpid(), (long)getppid());
    printf("Press Enter to finish.\n");
    getchar();
    printf("Finished.\n");
    return 0;
}
