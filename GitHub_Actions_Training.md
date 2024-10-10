
# GitHub Actions Training for Experienced Developers

## Introduction to GitHub Actions

**GitHub Actions** is a CI/CD platform that allows you to automate tasks within your software development lifecycle. With GitHub Actions, you can build, test, and deploy your code right from GitHub.

### Key Concepts:
1. **Workflows**: Automated processes that you can set up in your repository to build, test, and deploy your code.
2. **Jobs**: A set of steps that execute on the same runner.
3. **Steps**: Individual tasks performed in a job.
4. **Runners**: Servers that run the jobs. GitHub provides Linux, Windows, and macOS runners.
5. **Events**: Triggers that kick off workflows (e.g., `push`, `pull_request`).
6. **Actions**: Predefined or custom commands that automate software tasks.

### Simple GitHub Actions Workflow Example

```yaml
# .github/workflows/ci.yml
name: CI Workflow

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2
    - name: Set up Node.js
      uses: actions/setup-node@v2
      with:
        node-version: '14'
    - name: Install Dependencies
      run: npm install
    - name: Run Tests
      run: npm test
```

This simple workflow will run whenever code is pushed or a pull request is made. It checks out the code, sets up Node.js, installs dependencies, and runs the tests.

## Hands-On Activity: Creating a Custom GitHub Action

1. **Create a New GitHub Repository**

2. **Create a Basic Workflow**

Create a file called `.github/workflows/main.yml` in your repository with the following content:

```yaml
name: Custom Action Workflow

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2
    - name: Custom Action
      run: echo "Hello, World!"
```

3. **Create a Custom Action**

- In the root of your repository, create a new directory called `my-action`.
- Add the following files:

**action.yml**:
```yaml
name: "My Custom Action"
description: "An action to greet someone"
inputs:
  name:
    description: "The name of the person to greet"
    required: true
    default: "World"

runs:
  using: "node12"
  main: "index.js"
```

**index.js**:
```js
console.log(`Hello ${process.env.INPUT_NAME}`);
```

4. **Test the Custom Action**

Modify the workflow file to use your custom action:

```yaml
name: Custom Action Workflow

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2
    - name: Custom Action
      uses: ./my-action
      with:
        name: "Developer"
```

Now, every time you push changes to your repository, your custom action will run.

## Test Questions

1. **What is a GitHub Action?**
   - Answer: A GitHub Action is a custom command to automate tasks in your GitHub repository.

2. **What file format is used to define GitHub workflows?**
   - Answer: YAML (.yml or .yaml).

3. **What is the purpose of the `runs-on` key in a job?**
   - Answer: It specifies the runner on which the job will execute (e.g., `ubuntu-latest`).

4. **How do you trigger a workflow on a `push` event?**
   - Answer: Define `on: push` in the workflow file.

5. **What command is used to set up Node.js in a workflow?**
   - Answer: `actions/setup-node@v2`

## Answers:
1. GitHub Action is a custom command for automating tasks.
2. YAML format (.yml or .yaml).
3. The `runs-on` key defines the runner (e.g., Ubuntu).
4. Use `on: push` to trigger a workflow on a push event.
5. Use `actions/setup-node@v2` to set up Node.js.

