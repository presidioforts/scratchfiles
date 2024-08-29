import subprocess
import sys
import os
from setuptools import setup, find_packages

# Upgrade setuptools before proceeding
try:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "setuptools"])
except subprocess.CalledProcessError as e:
    print(f"Failed to upgrade setuptools: {e}")
    sys.exit(1)  # Exit if the upgrade fails

# Now you can safely run the setup function
setup(
    name="your_project_name",
    description="your_project_description",
    packages=find_packages(),
    version=os.environ.get('BUILDNUMBER', '0.1.0'),  # Default version if BUILDNUMBER is not set
    # other setup options
)
