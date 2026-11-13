#!/bin/bash
cd ~/os-labs/Lab4

# Run memory in background with nohup to keep it alive
nohup ./memory > /tmp/m.txt 2>&1 &
PARENT=$!
sleep 1

# Get child PID from output
CHILD=$(grep "child pid=" /tmp/m.txt | sed 's/.*child pid=\([0-9]*\).*/\1/')
echo "=== Child PID: $CHILD ==="
echo "=== Parent PID: $PARENT ==="
echo ""
echo "=== Output so far ==="
cat /tmp/m.txt
echo ""
echo "=== Maps: memory executable ==="
grep "/memory$" /proc/$CHILD/maps
echo ""
echo "=== Maps: [stack] ==="
grep -F "[stack]" /proc/$CHILD/maps
echo ""
echo "=== Maps: [heap] ==="
grep -F "[heap]" /proc/$CHILD/maps
echo ""
echo "=== Sending Enter to finish ==="
echo "" > /proc/$PARENT/fd/0 2>/dev/null
wait $PARENT
echo ""
echo "=== Final output ==="
cat /tmp/m.txt
echo ""
echo "=== Done ==="
