#!/bin/bash
cd /home/sun/os-labs/Lab4
{
echo "=== pwd ==="
pwd
echo "=== ls ==="
ls
echo "=== gcc pointer ==="
gcc pointer.c -o pointer
echo "gcc_exit=$?"
echo "=== ./pointer ==="
./pointer
echo "run_exit=$?"
} > /tmp/lab4_result.txt 2>&1
chmod 644 /tmp/lab4_result.txt
