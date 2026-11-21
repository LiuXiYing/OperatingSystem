#!/bin/bash
cd ~/os-labs/Lab4

# Start memory in background
./memory > /tmp/mem.txt 2>&1 &
PARENT=$!
sleep 1

# Get child PID from output
CHILD=$(grep "child pid=" /tmp/mem.txt | sed 's/.*child pid=\([0-9]*\).*/\1/')
echo "CHILD_PID=$CHILD"
echo "PARENT_PID=$PARENT"
echo "=== OUTPUT ==="
cat /tmp/mem.txt
echo "=== MAPS memory ==="
grep "/memory$" /proc/$CHILD/maps
echo "=== MAPS stack ==="
grep -F "[stack]" /proc/$CHILD/maps
echo "=== MAPS heap ==="
grep -F "[heap]" /proc/$CHILD/maps
echo "=== DONE ==="

# Kill it since we got what we need
kill $PARENT 2>/dev/null
kill $CHILD 2>/dev/null
wait 2>/dev/null
