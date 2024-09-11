bimport os
import subprocess
import sys

print("Upgrading setup tools...")

# Define the path to your virtual environment's pip
pip_path = "/apps/jenkins/pipeline-worker/workspace/jenkins-build15/1547520982/LADIS-ERCMS-WebAPI_develop_3.9/bin/pip"

# Run the upgrade command using subprocess
try:
    subprocess.run([pip_path, "install", "--upgrade", "pip"], check=True)
    subprocess.run([pip_path, "install", "--upgrade", "setuptools", "wheel"], check=True)
    print("pip, setuptools, and wheel successfully upgraded.")
except subprocess.CalledProcessError as e:
    print(f"Error during upgrade: {e}")
    sys.exit(1)



import os
import subprocess
import sys

print("Upgrading setup tools...")

# Define the path to your virtual environment's pip
pip_path = "/apps/jenkins/pipeline-worker/workspace/jenkins-build15/1547520982/LADIS-ERCMS-WebAPI_develop_3.9/bin/pip"

# Define the custom index URL
custom_index_url = "https://your-custom-index-url.com/simple"

# Step 1: Set the correct index URL using pip config
try:
    print(f"[INFO] Setting custom index URL to {custom_index_url}")
    subprocess.run([pip_path, 'config', 'set', 'global.index-url', custom_index_url], check=True)
except subprocess.CalledProcessError as e:
    print(f"[ERROR] Failed to set custom index URL: {e}")
    sys.exit(1)

# Step 2: Run the upgrade command using subprocess
try:
    subprocess.run([pip_path, "install", "--upgrade", "pip"], check=True)
    subprocess.run([pip_path, "install", "--upgrade", "setuptools", "wheel"], check=True)
    print("pip, setuptools, and wheel successfully upgraded.")
except subprocess.CalledProcessError as e:
    print(f"Error during upgrade: {e}")
    sys.exit(1)

# Step 3: Verify pip config settings
try:
    print("[INFO] Verifying pip config settings:")
    subprocess.run([pip_path, "config", "list"], check=True)
except subprocess.CalledProcessError as e:
    print(f"[ERROR] Failed to verify pip config: {e}")
    sys.exit(1)



    _________-_

    import os
import subprocess
import sys

print("Upgrading setup tools...")

# Define the path to your virtual environment's pip
pip_path = "/apps/jenkins/pipeline-worker/workspace/jenkins-build15/1547520982/LADIS-ERCMS-WebAPI_develop_3.9/bin/pip"

# Define the custom index URL
custom_index_url = "https://your-custom-index-url.com/simple"

# Step 1: Set the correct index URL using pip config
try:
    print(f"[INFO] Setting custom index URL to {custom_index_url}")
    subprocess.run([pip_path, 'config', 'set', 'global.index-url', custom_index_url], check=True)
except subprocess.CalledProcessError as e:
    print(f"[ERROR] Failed to set custom index URL: {e}")
    sys.exit(1)

# Step 2: Upgrade pip, setuptools, and wheel with version constraints
try:
    # Upgrade pip to the latest version
    subprocess.run([pip_path, "install", "--upgrade", "pip"], check=True)
    
    # Upgrade setuptools to version 66 and above (compatible with Python 3.9)
    subprocess.run([pip_path, "install", "--upgrade", "setuptools>=66"], check=True)
    
    # Upgrade wheel (you can also specify a version if needed)
    subprocess.run([pip_path, "install", "--upgrade", "wheel"], check=True)

    print("pip, setuptools (>=66), and wheel successfully upgraded.")
except subprocess.CalledProcessError as e:
    print(f"[ERROR] Failed to upgrade tools: {e}")
    sys.exit(1)

# Step 3: Verify pip config settings
try:
    print("[INFO] Verifying pip config settings:")
    subprocess.run([pip_path, "config", "list"], check=True)
except subprocess.CalledProcessError as e:
    print(f"[ERROR] Failed to verify pip config: {e}")
    sys.exit(1)
