#!/bin/bash

# Define your custom index URL and trusted host
CUSTOM_INDEX_URL="https://your-custom-index-url.com/simple"
TRUSTED_HOST="artifactory.int.yourcompany.net"

# Define the path to your virtual environment activation script
VENV_PATH="/apps/jenkins/pipeline-worker/workspace/jenkins-build15/1435414575/LADIS-ERCMS-WebAPI_develop_3.9/bin/activate"

# Function to log messages
log_message() {
    echo "[INFO] $1"
}

# Step 1: Activate the virtual environment
if [ -f "$VENV_PATH" ]; then
    log_message "Activating virtual environment at $VENV_PATH"
    source "$VENV_PATH"
else
    log_message "ERROR: Virtual environment activation script not found at $VENV_PATH"
    exit 1
fi

# Step 2: Upgrade pip, setuptools, and wheel
log_message "Upgrading pip, setuptools, and wheel..."
pip install --upgrade pip setuptools wheel || { log_message "Failed to upgrade pip, setuptools, and wheel"; exit 1; }

# Step 3: Unset any incorrect 'global.index-url'
log_message "Checking for incorrect 'global.index-url' setting..."
pip config unset global.index-url || log_message "'global.index-url' is not set, skipping."

# Step 4: Set the correct 'global.index-url'
log_message "Setting 'global.index-url' to $CUSTOM_INDEX_URL"
pip config set global.index-url $CUSTOM_INDEX_URL

# Step 5: Set the trusted host
log_message "Setting 'global.trusted-host' to $TRUSTED_HOST"
pip config set global.trusted-host $TRUSTED_HOST

# Step 6: Verify the new configuration
log_message "Verifying the configuration..."
pip config list

log_message "pip.conf configuration updated successfully."
