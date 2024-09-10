#!/bin/bash

# Define your custom index URL
CUSTOM_INDEX_URL="https://your-custom-index-url.com/simple"

# Define the path to your virtual environment activation script
VENV_PATH="/apps/jenkins/pipeline-worker/workspace/jenkins-build15/1435414575/LADIS-ERCMS-WebAPI_develop_3.9/bin/activate"

# Step 1: Activate the virtual environment
if [ -f "$VENV_PATH" ]; then
    echo "[INFO] Activating virtual environment at $VENV_PATH"
    source "$VENV_PATH"
else
    echo "[ERROR] Virtual environment activation script not found at $VENV_PATH"
    exit 1
fi

# Step 2: Upgrade pip, setuptools, and wheel
echo "[INFO] Upgrading pip, setuptools, and wheel..."
pip install --upgrade pip setuptools wheel || { echo "[ERROR] Failed to upgrade pip, setuptools, and wheel"; exit 1; }

# Step 3: Unset any incorrect 'global.index-url'
echo "[INFO] Checking for incorrect 'global.index-url' setting..."
pip config unset global.index-url || echo "[INFO] 'global.index-url' is not set, skipping."

# Step 4: Set the correct 'global.index-url'
echo "[INFO] Setting 'global.index-url' to $CUSTOM_INDEX_URL"
pip config set global.index-url $CUSTOM_INDEX_URL

# Step 5: Verify the new configuration
echo "[INFO] Verifying the configuration..."
pip config list

echo "[INFO] pip.conf configuration updated successfully."
