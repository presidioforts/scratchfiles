

#!/bin/bash

# Find the PID of the process listening on port 8084
PID=$(lsof -t -i:8084)

# If a process was found, kill it
if [ -n "$PID" ]; then
    echo "Stopping process on port 8084 with PID $PID"
    kill "$PID"
    # If the process does not stop, uncomment the next line to force kill
    # kill -9 "$PID"
else
    echo "No process found on port 8084"
fi
