#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>

int main()
{
    pid_t pid;
    printf("父进程，PID = %d\n", getpid());

    pid = fork();
    if (pid < 0)
    {
        perror("fork error");
        return 1;
    }
    else if (pid == 0)
    {
        printf("子进程，PID = %d，父进程PID = %d\n", getpid(), getppid());
    }
    else
    {
        printf("父进程等待子进程，子进程PID = %d\n", pid);
    }
    return 0;
}
