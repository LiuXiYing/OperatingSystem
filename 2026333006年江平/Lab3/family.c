#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>

int main(void) {
    pid_t child = fork();
    if (child < 0) {
        perror("fork");
        return 1;
    }
    if (child == 0) {
        printf("child pid=%ld, parent=%ld\n", (long)getpid(), (long)getppid());
        return 0;
    }
    if (waitpid(child, NULL, 0) < 0) {
        perror("waitpid");
        return 1;
    }
    printf("parent pid=%ld: child finished\n", (long)getpid());
    return 0;
}
