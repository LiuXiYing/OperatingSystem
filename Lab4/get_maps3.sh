#!/bin/bash
cd ~/os-labs/Lab4

# Run memory under script to allocate pty
script -q -c "./memory" /tmp/mem.log &
sleep 2

# Find child memory process
CPID=$(pgrep -n memory)
echo "=== Child PID: $CPID ==="
echo ""
echo "=== Script log ==="
cat /tmp/mem.log
echo ""
if [ -n "$CPID" ]; then
    echo "=== Maps: memory executable ==="
    grep "/memory$" /proc/$CPID/maps
    echo ""
    echo "=== Maps: [stack] ==="
    grep -F "[stack]" /proc/$CPID/maps
    echo ""
    echo "=== Maps: [heap] ==="
    grep -F "[heap]" /proc/$CPID/maps
else
    echo "=== No memory process found ==="
fi
echo ""
echo "=== Killing ==="
pkill -f "script.*memory" 2>/dev/null
pkill memory 2>/dev/null
sleep 1
echo "=== Done ==="
