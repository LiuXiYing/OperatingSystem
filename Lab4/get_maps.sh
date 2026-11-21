#!/bin/bash
cd ~/os-labs/Lab4

# Use script to allocate pty so getchar() waits
script -qc "./memory" /dev/null &
SCRIPT_PID=$!
sleep 2

# Find child memory process
CPID=$(pgrep -n memory)
echo "=== Child PID: $CPID ==="
echo ""
echo "=== Current output ==="
cat /tmp/m.txt 2>/dev/null || echo "(no output file yet)"
echo ""
echo "=== Maps: memory executable ==="
grep "/memory$" /proc/$CPID/maps
echo ""
echo "=== Maps: [stack] ==="
grep -F "[stack]" /proc/$CPID/maps
echo ""
echo "=== Maps: [heap] ==="
grep -F "[heap]" /proc/$CPID/maps
echo ""
echo "=== Killing processes ==="
kill $CPID 2>/dev/null
kill $SCRIPT_PID 2>/dev/null
wait 2>/dev/null
echo "=== Done ==="
