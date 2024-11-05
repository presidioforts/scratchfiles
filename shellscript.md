
Certainly! I'd be happy to help you create a sample GitHub Actions workflow that runs shell scripts.

Sample GitHub Actions Workflow to Run Shell Scripts

Here's a basic example of a workflow file (.github/workflows/run-shell-script.yml) that runs shell scripts:

name: Run Shell Scripts

on:
  push:
    branches:
      - main  # Trigger the workflow on pushes to the main branch

jobs:
  execute-scripts:
    runs-on: ubuntu-latest  # Use 'self-hosted' if you're using a self-hosted runner
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v3  # Allowed action in your environment

      - name: Run Inline Shell Commands
        run: |
          echo "Running inline shell commands"
          ls -la
          pwd

      - name: Run Shell Script File
        run: |
          chmod +x ./scripts/my-script.sh
          ./scripts/my-script.sh

      - name: Run Shell Script with Arguments
        run: |
          ./scripts/another-script.sh arg1 arg2

      - name: Run Shell Script as Specific User
        run: |
          sudo -u username ./scripts/admin-script.sh

Explanation

Workflow Name (name): A descriptive name for your workflow, e.g., "Run Shell Scripts".

Trigger (on): Specifies when the workflow should run. This example triggers on a push to the main branch.

Jobs:

Job ID (execute-scripts): An identifier for the job.

Runs-on: Specifies the runner environment. Use ubuntu-latest or self-hosted, depending on your setup.


Steps:

Checkout Repository:

Uses actions/checkout@v3 to clone your repository into the runner.

Note: actions/checkout@v3 is allowed in your environment.


Run Inline Shell Commands:

Executes shell commands directly within the workflow.

Useful for quick commands or setting up the environment.


Run Shell Script File:

Executes a shell script located in your repository.

chmod +x ensures the script is executable.

Replace ./scripts/my-script.sh with the path to your script.


Run Shell Script with Arguments:

Demonstrates how to pass arguments to your shell script.


Run Shell Script as Specific User:

Shows how to run a script with sudo as another user (if permissions allow).




Creating Shell Scripts in Your Repository

Example: scripts/my-script.sh

#!/bin/bash

echo "Hello from my-script.sh!"
# Add your commands here

Example: scripts/another-script.sh

#!/bin/bash

echo "Script Name: $0"
echo "First Argument: $1"
echo "Second Argument: $2"

Making Scripts Executable

Ensure your shell scripts have execute permissions before committing:

chmod +x scripts/my-script.sh
chmod +x scripts/another-script.sh
git add scripts/my-script.sh scripts/another-script.sh
git commit -m "Add shell scripts with execute permissions"
git push

Running Shell Scripts Without chmod

Alternatively, you can invoke the script with the shell interpreter:

- name: Run Shell Script Without chmod
  run: |
    bash ./scripts/my-script.sh

Using Environment Variables

You can pass environment variables to your scripts:

- name: Run Script with Environment Variables
  run: |
    ./scripts/env-script.sh
  env:
    MY_VARIABLE: "Some Value"

In env-script.sh:

#!/bin/bash

echo "MY_VARIABLE is $MY_VARIABLE"

Error Handling in Shell Scripts

To make your script exit on errors, add set -e at the top:

#!/bin/bash
set -e

# Your commands here

Specifying the Shell Interpreter

You can specify which shell to use in your workflow:

- name: Run Script with Zsh
  shell: zsh
  run: |
    ./scripts/my-zsh-script.sh

Running Scripts on Different Operating Systems

If you need to run scripts on different operating systems:

jobs:
  execute-scripts:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v3

      - name: Run OS Specific Script
        run: |
          ./scripts/os-specific-script.sh

Using Allowed Actions

Given your environment's restrictions, you can use actions/github-script@v6 to run JavaScript if needed:

- name: Run JavaScript
  uses: actions/github-script@v6
  with:
    script: |
      console.log('Hello from GitHub Script');

Complete Workflow Example

Putting it all together:

name: Shell Script Execution Workflow

on:
  workflow_dispatch:
  push:
    branches:
      - main

jobs:
  execute-shell-scripts:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v3

      - name: List Files in Repository
        run: ls -la

      - name: Execute Hello World Script
        run: |
          echo "Running hello-world.sh"
          ./scripts/hello-world.sh

      - name: Execute Script with Parameters
        run: |
          echo "Running parameterized-script.sh with arguments"
          ./scripts/parameterized-script.sh arg1 arg2 arg3

      - name: Upload Script Output
        uses: actions/upload-artifact@v3
        with:
          name: script-output
          path: output/

Explanation of Additional Steps

Workflow Dispatch: Allows manual triggering of the workflow.

Upload Artifact:

Uses actions/upload-artifact@v3 to save files generated during the workflow.

Note: actions/upload-artifact@v3 is allowed in your environment.



Best Practices

Keep Scripts Modular: Break down complex tasks into smaller scripts.

Logging: Use echo to log important information and variables.

Error Handling: Use set -e and trap to handle errors gracefully.

Security: Be cautious with sensitive data. Avoid logging secrets or credentials.


Additional Resources

GitHub Actions Documentation

Workflow Syntax for GitHub Actions

Using Shell Scripts in Workflows



---

If you have any specific requirements or need further customization, feel free to ask!

