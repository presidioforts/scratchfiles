
# Python and Shell Script Execution Workflow

This workflow automates the installation of Python, runs inline shell commands, and executes a shell script when triggered by specific events.

## Workflow YAML

```yaml
name: Python and .sh demo

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]
  workflow_dispatch:

permissions:
  contents: read

jobs:
  build:
    runs-on: wf-linux

    steps:
      - uses: actions/checkout@v4

      - name: Install Python Manually
        run: |
          sudo apt install -y python3

      - name: Verify the Python Version
        run: python3 --version

      - name: Run Inline Shell Commands
        run: |
          echo "Running inline shell commands"
          ls -la
          pwd

      - name: Run Shell Script File
        run: |
          chmod +x ./scripts/my-script.sh
          ./scripts/my-script.sh
