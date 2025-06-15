I'll modify the `start_app.sh` script to add those steps after the application starts successfully:

```bash:start_app.sh
#!/bin/bash

# start_app.sh - Script to start the AI DevOps Assistant Flask app as background process

set -e  # Exit on any error

# Configuration
APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$APP_DIR/venv"  # Adjust path if your venv is elsewhere
PYTHON_APP="$APP_DIR/app/main.py"
LOG_FILE="$APP_DIR/app.log"
PID_FILE="$APP_DIR/app.pid"

echo "Starting AI DevOps Assistant as background process..."
echo "App directory: $APP_DIR"

# Check if virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Error: Virtual environment not found at $VENV_DIR"
    echo "Please ensure your virtual environment is set up correctly."
    exit 1
fi

# Check if main.py exists
if [ ! -f "$PYTHON_APP" ]; then
    echo "Error: main.py not found at $PYTHON_APP"
    exit 1
fi

# Check if app is already running
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p $PID > /dev/null 2>&1; then
        echo "Error: Application is already running with PID $PID"
        echo "Use './stop_app.sh' to stop it first, or './restart_app.sh' to restart"
        exit 1
    else
        echo "Removing stale PID file..."
        rm -f "$PID_FILE"
    fi
fi

# Activate virtual environment
echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Navigate to app directory
cd "$APP_DIR"

# Start the Flask application as background process
echo "Starting Flask application in background..."
echo "Log file: $LOG_FILE"
echo "PID file: $PID_FILE"

nohup python app/main.py > "$LOG_FILE" 2>&1 &
APP_PID=$!

# Save PID to file
echo $APP_PID > "$PID_FILE"

echo "Application started successfully!"
echo "PID: $APP_PID"

# Wait a moment for the app to initialize
echo "Waiting for application to initialize..."
sleep 3

# Show recent logs
echo "========== Recent App Logs =========="
tail -n 10 "$LOG_FILE"
echo "====================================="

# Health check
echo "Performing health check..."
HEALTH_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/v1/health 2>/dev/null || echo "000")

if [ "$HEALTH_RESPONSE" = "200" ]; then
    echo "✅ Health check passed! App is running and healthy."
    curl -s http://localhost:8000/v1/health | python -c "import sys, json; print(json.dumps(json.load(sys.stdin), indent=2))" 2>/dev/null || echo "Response received but couldn't format JSON"
elif [ "$HEALTH_RESPONSE" = "503" ]; then
    echo "⚠️  App is running but model not loaded yet (HTTP 503)"
    echo "Check logs for model loading progress..."
else
    echo "❌ Health check failed (HTTP $HEALTH_RESPONSE)"
    echo "Check logs for errors..."
fi

echo ""
echo "Commands:"
echo "  View live logs: tail -f $LOG_FILE"
echo "  Health check:   curl http://localhost:8000/v1/health"
echo "  Stop app:       ./stop_app.sh"
echo "  Restart app:    ./restart_app.sh"
```

**Key additions:**

1. **Wait for initialization**: 3-second pause to let the app start up
2. **Show recent logs**: Displays last 10 lines of `app.log`
3. **Automatic health check**: Performs curl health check and shows status
4. **Status indicators**: Uses emoji indicators (✅, ⚠️, ❌) for easy status recognition
5. **Helpful commands**: Shows useful commands at the end

**What you'll see when running `./start_app.sh`:**
- Application startup messages
- Recent log entries
- Health check results with status
- Quick reference commands

This gives you immediate feedback on whether the app started successfully and if the model loaded properly.
