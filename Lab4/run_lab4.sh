#!/bin/bash
cd ~/os-labs/Lab4

# Run memory in background, capture output
./memory > /tmp/mem_out.txt 2>&1 &
PARENT_PID=$!
sleep 1

# Read child PID from output
CHILD_PID=$(grep "child pid=" /tmp/mem_out.txt | sed 's/.*child pid=\([0-9]*\).*/\1/')
echo "=== Child PID: $CHILD_PID ==="
echo "=== Parent PID: $PARENT_PID ==="

echo ""
echo "=== Current output ==="
cat /tmp/mem_out.txt

echo ""
echo "=== Memory executable mapping (r-xp) ==="
grep "/memory$" /proc/$CHILD_PID/maps

echo ""
echo "=== [stack] mapping ==="
grep -F "[stack]" /proc/$CHILD_PID/maps

echo ""
echo "=== [heap] mapping ==="
grep -F "[heap]" /proc/$CHILD_PID/maps

echo ""
echo "=== Sending Enter to finish child ==="
# Send Enter by writing to the process's stdin
echo "" > /proc/$PARENT_PID/fd/0 2>/dev/null || true
wait $PARENT_PID

echo ""
echo "=== Final output ==="
cat /tmp/mem_out.txt
echo ""
echo "=== Exit code: $? ==="
