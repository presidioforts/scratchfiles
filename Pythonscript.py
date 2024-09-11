
import os
import subprocess
import sys

# Define your custom index URL
CUSTOM_INDEX_URL = "https://your-custom-index-url.com/simple"

# Define the path to your virtual environment activation script
VENV_PATH = "/apps/jenkins/pipeline-worker/workspace/jenkins-build15/1435414575/LADIS-ERCMS-WebAPI_develop_3.9/bin/activate"

# Step 1: Activate the virtual environment
if os.path.exists(VENV_PATH):
    print(f"[INFO] Activating virtual environment at {VENV_PATH}")
    activate_script = f"source {VENV_PATH}"
    activate_cmd = f"{activate_script} && exec $SHELL"
    subprocess.run(activate_cmd, shell=True, check=True, executable='/bin/bash')
else:
    print(f"[ERROR] Virtual environment activation script not found at {VENV_PATH}")
    sys.exit(1)

# Step 2: Upgrade pip, setuptools, and wheel
print("[INFO] Upgrading pip, setuptools, and wheel...")
try:
    subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip', 'setuptools', 'wheel'], check=True)
except subprocess.CalledProcessError:
    print("[ERROR] Failed to upgrade pip, setuptools, and wheel")
    sys.exit(1)

# Step 3: Unset any incorrect 'global.index-url'
print("[INFO] Checking for incorrect 'global.index-url' setting...")
try:
    subprocess.run([sys.executable, '-m', 'pip', 'config', 'unset', 'global.index-url'], check=True)
except subprocess.CalledProcessError:
    print("[INFO] 'global.index-url' is not set, skipping.")

# Step 4: Set the correct 'global.index-url'
print(f"[INFO] Setting 'global.index-url' to {CUSTOM_INDEX_URL}")
try:
    subprocess.run([sys.executable, '-m', 'pip', 'config', 'set', 'global.index-url', CUSTOM_INDEX_URL], check=True)
except subprocess.CalledProcessError as e:
    print(f"[ERROR] Failed to set 'global.index-url': {e}")
    sys.exit(1)

# Step 5: Verify the new configuration
print("[INFO] Verifying the configuration...")
try:
    subprocess.run([sys.executable, '-m', 'pip', 'config', 'list'], check=True)
except subprocess.CalledProcessError:
    print("[ERROR] Failed to verify the pip configuration")
    sys.exit(1)

# Step 6: Deactivate the virtual environment
print("[INFO] Deactivating the virtual environment")
try:
    subprocess.run(['deactivate'], shell=True)
except Exception:
    print("[INFO] Virtual environment deactivation failed or not active.")

print("[INFO] pip.conf configuration updated and virtual environment deactivated successfully.")
