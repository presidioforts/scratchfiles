### EPL-X "Python" Buildpack

#### **1. pyproject.toml Configuration**

- Leverages Python’s de facto standard for managing dependencies, build tools, and configurations (e.g., linting, formatting, coverage).
- Aligns with open-source best practices, making it intuitive for Python developers to adopt.

Below is a sample `pyproject.toml` file showcasing how to configure dependencies, testing, coverage, and linting preferences for a Python project:

```toml
[project]
name = "dctrn-python-app"
version = "0.1.0"
description = "EPL-X reference Python app dctrn"
# Specify Python version requirement:
# requires-python = ">=3.11,<3.12"

# Application dependencies
dependencies = [
  "requests>=2.25,<3.0",
  "pytest>=7.0,<8.0",
  "pytest-cov>=3.0,<4.0"
]

[build-system]
# Defines how this project is built
requires = [
  "setuptools>=65.0.0",
  "wheel>=0.38.0",
  "pip>=23.0.1"
]
build-backend = "setuptools.build_meta"

[tool.pytest.ini_options]
# Configure pytest options
addopts = """
--cov=src
--cov-report=xml
--cov-report=html
--disable-warnings
"""

[tool.black]
# Black formatter settings
line-length = 88
target-version = ["py39"]

[tool.flake8]
# Flake8 linter rules
max-line-length = 88
exclude = [
  ".git",
  "__pycache__",
  "build",
  "dist"
]
ignore = ["E203", "W503"]
```

---

#### **2. EPL-X GITACT Python Workflows**

- Each repository’s workflow file specifies only essential details like release number and log level.
- Enterprise and Python-level configurations are handled automatically, minimizing repository-specific configurations.
- The SCP database provides centralized control over all remaining configurations required for Python builds, scans, and harness delivery.
- Developers can use the ELMA/IDB self-service EPL-X configuration tool to update and maintain Python buildpack configurations.
- Enables developers to fully manage pipeline configurations through an intuitive self-service interface, ELMA/IDB, to update and maintain configurations per component.

---

#### **3. EPL-X GITACT Auto-Discovery**

- Reads `pyproject.toml` to identify dependencies, test commands, coverage, and linting configurations.
- Retrieves the remaining configuration required for builds from the SCP database.
- Organizes the workflow configuration and executes the build, scan, and harness delivery.

---

#### **4. Python Tool Versions**

- The EPL-X Python buildpack must provide a pinned baseline for core Python tools (e.g., `pip`, `setuptools`, `wheel`) to ensure stability and security.
- Developers can override these versions in `pyproject.toml` to use specialized tooling if needed.

---

#### **5. Packaging Recommendation for Deployment**

##### **For VM Deployments**

1. If the VM has Python installed, use Wheels for packaging as it is an official and standard approach.
2. For environments requiring self-contained code, zip up a local virtual environment (venv), but ensure to exclude global `site-packages` to avoid conflicts.

##### **For Container Deployments**

1. Use multi-stage builds to keep images slim by installing dependencies in a builder stage and copying only what is needed to the final stage.
2. Include a `.dockerignore` file to prevent copying irrelevant files into the Docker build context.

