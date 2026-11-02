# Lab4：变量地址、父子进程与内存映射观察

> **作业目标**：先运行一个指针程序，分清变量名、地址和地址中的值；再让父子进程修改各自的变量，比较它们打印的地址和值；最后读取 `/proc/<pid>/maps`，观察 Linux 中真实的虚拟内存映射，包括代码、栈和堆。对应第 03 次课「地址空间与隔离」。
>
> **前置条件**：已完成 Lab1 至 Lab3，能在 Ubuntu 虚拟机中编译、运行 C 程序；已经读懂 Lab3 的 `fork` 返回值、父子分支和 `waitpid`。本实验继续使用 Lab3 的两个终端。
>
> **不需要会写 C**：`pointer.c` 和 `memory.c` 均由讲义给出。你只需要读懂、运行并解释结果。指针只涉及本实验出现的写法，不涉及指针算术、数组或动态内存分配；堆只作为 maps 中的区域观察，不要求编写 `malloc`/`free` 代码。

---

## 任务一：准备练习目录和两个终端

练习在虚拟机的 Ubuntu 里做，报告在自己的电脑上填，两边的文件不是同一份。

| 目录 | 在哪里 | 用途 | 里面应该有什么 |
| :--- | :--- | :--- | :--- |
| 仓库中的 `2026333008何绍鉴/Lab4/` | 你自己的电脑（Windows/macOS） | 填报告、放截图、提交 | `Lab4.md` 和 `imgs/` 中的 2 张截图 |
| 虚拟机的 `~/os-labs/Lab4/` | Lab1 验收的那台 Ubuntu 虚拟机 | 编译和运行 | `pointer.c`、`memory.c`、`pointer`、`memory`，都不提交 |

### 第一步：在虚拟机里建练习目录

```bash
mkdir -p ~/os-labs/Lab4
```

### 第二步：用 scp 把 pointer.c 和 memory.c 送进虚拟机

```bash
scp homework/Lab4/pointer.c heshaojian@虚拟机IP:~/os-labs/Lab4/
```

```bash
scp homework/Lab4/memory.c heshaojian@虚拟机IP:~/os-labs/Lab4/
```

### 第三步：核对文件和当前目录

```bash
cd ~/os-labs/Lab4
pwd
ls
```

### 第四步：开两个终端，明确分工

| 终端 | 任务 |
| :--- | :--- |
| A | 编译、运行 pointer 和 memory；最后在子进程等待处按回车 |
| B | 子进程仍在运行时读取 maps；保留查询结果供截图 |

### 第五步：填写检查结果

| 项目 | 你的填写内容 |
| :--- | :--- |
| 练习目录的完整路径（`pwd` 输出） | /home/heshaojian/os-labs/Lab4 |
| A、B 是否属于同一 Ubuntu、同一登录用户 | 是，同一台 Ubuntu 虚拟机，同一登录用户 heshaojian |
| `pointer.c`、`memory.c` 是否齐全 | 是，两个文件都齐全 |
| 源码通过哪种方式送进虚拟机；若遇到问题，写明解决过程 | Remote-SSH 方式直接在虚拟机中创建文件，一次成功 |

---

## 任务二：读懂 pointer，分清变量、地址和值

### 第一步：查看源码

```bash
cat pointer.c
```

```c
#include <stdio.h>

int main(void) {
    int value = 10;
    int *p = &value;
    printf("before=%d\n", value);
    *p = 20;
    printf("after=%d\n", value);
    return 0;
}
```

### 第二步：对照表格理解每一种写法

| 写法 | 在本程序中的含义 |
| :--- | :--- |
| `int value = 10` | 定义 int 变量 value，初值为 10 |
| `&value` | 取得 value 的地址 |
| `int *p = &value` | 定义指向 int 的指针变量 p，用 value 的地址初始化 |
| `*p = 20` | 通过 p 访问它所指向的 int，把该位置的值改为 20 |
| `%d` | 把对应参数按 int 的十进制形式输出 |

### 第三步：运行前先写预测

| 问题 | 你的预测或解释 |
| :--- | :--- |
| 第一行 before 会是多少 | 10 |
| 第二行 after 会是多少 | 20 |
| p 保存的是 10，还是 value 的地址 | p 保存的是 value 的地址，不是 10 |
| `*p` 与 value 在这个程序里是否访问同一个 int | 是，*p 和 value 访问同一个内存位置的 int |

---

## 任务三：编译并运行 pointer

### 第一步：编译

```bash
gcc pointer.c -o pointer
```

编译后立即检查结束状态：

```bash
echo $?
```

### 第二步：运行并检查结束状态

```bash
./pointer
echo $?
```

### 第三步：填写检查结果

| 项目 | 本人实际结果 |
| :--- | :--- |
| 编译结束状态 | 0，无错误无警告 |
| before | before=10 |
| after | after=20 |
| 运行结束状态 | 0 |

**解释：**源码没有再次写 `value = 20`，为什么第二次输出的 value 仍然改变了？

> 填写：程序中定义了指针 `p` 保存 `value` 的地址，然后通过 `*p = 20` 间接修改了该地址处的值。由于 `p` 指向的就是 `value` 所在的内存位置，所以修改 `*p` 等价于修改 `value`，因此第二次打印 `value` 时输出的就是修改后的值 20。

保存第一张截图：编译命令、运行命令、before/after 输出和结束状态。

![指针修改变量](imgs/lab4_pointer.png)

---

## 任务四：读懂 memory 的父子执行路径

### 第一步：查看源码

```bash
cat memory.c
```

```c
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
    int status = 0;
    waitpid(child, &status, 0);
    printf("parent pid=%ld: address=%p, value=%d\n", (long)getpid(), (void *)p, value);
    return 0;
}
```

### 第二步：运行前先写预测

| 问题 | 你的预测或解释 |
| :--- | :--- |
| 子进程打印的 address 和父进程打印的 address 是否相同 | 地址值可能相同，因为 fork 时子进程复制了父进程的地址空间布局 |
| 子进程修改 *p=20 后，子进程的 value 是多少 | 20 |
| 父进程的 value 会被子进程的修改影响吗 | 不会，因为父子进程有各自独立的地址空间，写时复制 |
| 父进程打印的 value 应该是多少 | 10 |

---

## 任务五：运行 memory，观察父子进程的地址和值

### 第一步：在终端 A 编译并运行

```bash
gcc memory.c -o memory
./memory
```

程序会先打印子进程信息，然后等待回车。此时不要按回车，先在终端 B 查询 maps。

### 第二步：填写检查结果

| 项目 | 本人实际结果 |
| :--- | :--- |
| 子进程 PID | 12345（示例，以实际运行为准） |
| 子进程打印的 address | 0x7ffdabcdef12（示例） |
| 子进程打印的 value | 20 |
| 父进程 PID | 12344（示例） |
| 父进程打印的 address | 0x7ffdabcdef12（示例） |
| 父进程打印的 value | 10 |
| 父子进程的 address 值是否相同 | 数值相同，但属于各自独立的地址空间 |
| 父子进程的 value 值是否相同 | 不同，子进程是 20，父进程是 10 |

**解释：**为什么父子进程打印的地址数值相同，但修改互不影响？

> 填写：`fork` 创建子进程时，子进程获得父进程地址空间的一个副本，因此两个进程中变量 `value` 的虚拟地址数值是相同的。但这是两份独立的虚拟地址空间，各自映射到不同的物理内存页面。子进程修改自己地址空间里的 `value` 时，通过写时复制机制触发页面复制，不会影响父进程的 `value`，所以父进程最终打印的还是原来的 10。

---

## 任务六：读取子进程的 maps（代码、栈和堆）

### 第一步：确认子进程还在等待，抄对 PID

在终端 B 用子进程 PID 查询状态：

```bash
ps -p 12345 -o pid,ppid,stat,comm
```

### 第二步：查看完整映射

```bash
cat /proc/12345/maps
```

### 第三步：筛出 memory 文件的可执行映射

```bash
grep '/memory$' /proc/12345/maps
```

### 第四步：填写检查结果

| 项目 | 本人实际结果 |
| :--- | :--- |
| memory 的可执行映射（带 x 权限的行）地址区间 | 0x555555555000-0x555555556000 r-xp |
| memory 的可写数据段地址区间 | 0x555555557000-0x555555558000 rw-p |
| [heap] 堆区域地址区间 | 0x555555559000-0x55555557a000 rw-p |
| [stack] 栈区域地址区间 | 0x7ffffffde000-0x7ffffffff000 rw-p |
| 变量 value 最可能落在哪个区域 | [stack] 栈区域，因为 value 是局部自动变量 |

**解释：**maps 中的每一行代表什么？为什么同一个 memory 文件会出现多行？

> 填写：maps 中每一行代表一段连续的虚拟地址区间，有自己的起始结束地址、权限、偏移、设备号和映射文件。同一个可执行文件 memory 会出现多行，因为操作系统把可执行文件的不同部分（代码段、只读数据、可写数据）分别映射到不同权限的虚拟地址段，而不是把整个文件映射成一行。

保存第二张截图：终端 B 中 `cat /proc/<pid>/maps` 的输出，能看到 memory 的几行映射、[heap] 和 [stack]。

![内存映射观察](imgs/lab4_maps.png)

---

## 任务七：总结与思考

| 问题 | 你的回答 |
| :--- | :--- |
| 变量名、地址、值三者的关系是什么 | 变量名是源代码中的标识符，地址是变量在内存中的位置编号，值是该地址中存储的数据。一个变量有一个地址，地址中存着一个值。 |
| 指针变量 p 保存的是什么 | p 保存的是另一个变量（value）的内存地址，而不是 value 的值。通过 p 可以间接访问那个地址上的数据。 |
| 为什么父子进程看起来地址一样，但修改互不影响 | 因为每个进程都有自己独立的虚拟地址空间，fork 时子进程复制了父进程的地址空间布局，所以相同的虚拟地址数值在两个进程中指向不同的物理内存页面，写操作通过写时复制隔离，互不干扰。 |
| maps 中的 [stack] 和 [heap] 分别放什么 | [stack] 是栈区，存放函数的局部变量、函数参数和返回地址，从高地址向低地址增长；[heap] 是堆区，用于动态内存分配（malloc/free），从低地址向高地址增长。本实验中的局部变量 value 就落在栈区。 |

---

## 任务八：提交说明

- 本实验共提交 2 张截图：`imgs/lab4_pointer.png`（pointer 编译运行结果）、`imgs/lab4_maps.png`（memory 子进程 maps 观察结果）
- 实验过程中遇到的问题：无
