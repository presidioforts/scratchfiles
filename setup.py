import os
from setuptools import setup, find_packages

# Get the Jenkins BUILD_NUMBER environment variable; default to "0" if not set
build_number = os.environ.get("BUILD_NUMBER", "0")
version = f"2025.02.{build_number}"

setup(
    name="your_package_name",
    version=version,
    description="Your package description",
    author="Your Name",
    author_email="you@example.com",
    packages=find_packages(),
    # Include additional metadata or configurations as needed
)
