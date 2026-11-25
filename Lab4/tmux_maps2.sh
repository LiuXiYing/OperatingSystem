#!/bin/bash
cd ~/os-labs/Lab4

# Kill any existing tmux session
tmux kill-session -t lab4 2>/dev/null
sleep 1

# Start a new tmux session running memory
tmux new-session -d -s lab4 "./memory"

# Wait for child process to start
sleep 3

echo "=== tmux sessions ==="
tmux list-sessions
echo ""
echo "=== tmux capture-pane ==="
tmux capture-pane -t lab4 -p
echo ""

# Find child memory process
CPID=$(pgrep -n memory)
echo "=== Child PID: $CPID ==="
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
echo "=== Sending Enter to tmux to finish child ==="
tmux send-keys -t lab4 Enter
sleep 2
echo "=== Final output ==="
tmux capture-pane -t lab4 -p
tmux kill-session -t lab4 2>/dev/null
echo "=== Done ==="
