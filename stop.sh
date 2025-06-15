APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="$APP_DIR/app.pid"

if [ ! -f "$PID_FILE" ]; then
    echo "PID file not found. Application may not be running."
    exit 1
fi

PID=$(cat "$PID_FILE")

if ps -p $PID > /dev/null 2>&1; then
    echo "Stopping application (PID: $PID)..."
    kill $PID
    sleep 2
    
    # Force kill if still running
    if ps -p $PID > /dev/null 2>&1; then
        echo "Force stopping application..."
        kill -9 $PID
    fi
    
    rm -f "$PID_FILE"
    echo "Application stopped successfully."
else
    echo "Application with PID $PID is not running."
    rm -f "$PID_FILE"
fi
