import os
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
