# Lab1 进程创建实验
学号：2026333034

## 一、实验目的
1. 理解fork()系统调用，掌握进程创建原理。
2. 区分父进程与子进程，观察PID变化。

## 二、实验原理
fork()调用会复制当前进程，创建一个新子进程。
- 返回值>0：父进程，返回值是子进程PID
- 返回值=0：子进程
- 返回值<0：创建失败

## 三、源代码
```c
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
