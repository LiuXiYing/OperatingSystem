#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>

int main(void) {
    int value = 10;
    int *p = &value;
    pid_t child = fork();
    if (child < 0) {
        perror("fork");
        return 1;
    }
    if (child == 0) {
        *p = 20;
        printf("child pid=%ld: address=%p, value=%d\n", (long)getpid(), (void *)p, value);
        printf("Press Enter to finish the child.\n");
        getchar();
        return 0;
    }
    if (waitpid(child, NULL, 0) < 0) {
        perror("waitpid");
        return 1;
    }
    printf("parent pid=%ld: address=%p, value=%d\n", (long)getpid(), (void *)p, value);
    return 0;
}
