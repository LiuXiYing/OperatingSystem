#include <stdio.h>
#include <unistd.h>

int main(void) {
    printf("before exec: pid=%ld\n", (long)getpid());
    fflush(stdout);
    execl("/bin/echo", "echo", "new program is running", (char *)NULL);
    perror("execl");
    return 1;
}
